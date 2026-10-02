// miamibeerescue.com server
//
// - Serves the generated site in public/ with gzip. Fingerprinted files in
//   /assets/ are cached for a year; HTML is revalidated on every visit.
// - POST /api/leads receives the quote form and emails it to LEAD_NOTIFY_EMAIL
//   from a Gmail account (GMAIL_USER + GMAIL_APP_PASSWORD).
//   Subject: "New Miami Bee Rescue Lead: <name> (<city>)", prefixed with
//   [EMERGENCY] when the visitor picked the stinging-now option.
//   Every lead is also appended to leads.log as a backup.
// - www.miamibeerescue.com redirects (301) to the bare domain.
// - MAIL_DRY_RUN=1 builds each email and logs it instead of sending.
import express from "express";
import compression from "compression";
import nodemailer from "nodemailer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SITE_DIR = path.join(HERE, "public");
const LEAD_LOG = path.join(HERE, "leads.log");

const BRAND = "Miami Bee Rescue";
const HOST = "miamibeerescue.com";
const REDIRECT_HOSTS = new Set(["www.miamibeerescue.com"]);

const port = Number(process.env.PORT) || 3000;
const inbox = process.env.LEAD_NOTIFY_EMAIL || "removal@miamibeerescue.com";
const gmailUser = process.env.GMAIL_USER || "";
const gmailPass = process.env.GMAIL_APP_PASSWORD || "";
const dryRun = process.env.MAIL_DRY_RUN === "1";

let transport = null;
if (dryRun) transport = nodemailer.createTransport({ jsonTransport: true });
else if (gmailUser && gmailPass)
  transport = nodemailer.createTransport({ service: "gmail", auth: { user: gmailUser, pass: gmailPass } });

const app = express();
app.disable("x-powered-by");
app.set("trust proxy", true);
app.use(compression());

app.use((req, res, next) => {
  const host = String(req.headers.host || "").toLowerCase().split(":")[0];
  if (REDIRECT_HOSTS.has(host)) return res.redirect(301, "https://" + HOST + req.originalUrl);
  return next();
});

app.use(express.json({ limit: "20kb" }));
app.use(express.urlencoded({ extended: false, limit: "20kb" }));

// ---------------------------------------------------------------- leads
const FIELDS = [
  // [form field, label in the email, max length]
  ["name", "Name", 120],
  ["phone", "Phone", 40],
  ["location", "City or neighborhood", 200],
  ["email", "Email", 160],
  ["spot", "Where the bees are", 100],
  ["urgency", "How urgent", 100],
  ["notes", "Notes", 2000],
  ["page", "Sent from page", 200],
];

function pickLead(body) {
  const lead = {};
  for (const [key, , max] of FIELDS) lead[key] = String(body[key] ?? "").trim().slice(0, max);
  return lead;
}

const escapeHtml = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

const urgent = (lead) => /sting|emergency/i.test(lead.urgency);

function subjectLine(lead) {
  const base = `New ${BRAND} Lead: ${lead.name} (${lead.location})`;
  return urgent(lead) ? `[EMERGENCY] ${base}` : base;
}

function emailHtml(lead) {
  const rows = FIELDS.map(([key, label]) => {
    const value = lead[key] ? escapeHtml(lead[key]).replace(/\n/g, "<br>") : '<span style="color:#8A8578">not given</span>';
    return (
      `<tr><td style="padding:8px 14px;background:#F7F3EA;border-bottom:1px solid #E4DCC8;font-weight:bold;width:34%">${label}</td>` +
      `<td style="padding:8px 14px;border-bottom:1px solid #E4DCC8">${value}</td></tr>`
    );
  }).join("");
  const alert = urgent(lead)
    ? '<div style="background:#C8102E;color:#fff;padding:10px 14px;font-weight:bold;margin-bottom:12px">' +
      "Marked as stinging right now. Call this person first.</div>"
    : "";
  const callLink = lead.phone
    ? `<p style="margin:14px 0 0"><a href="tel:${escapeHtml(lead.phone.replace(/[^\d+]/g, ""))}" ` +
      'style="background:#1B1D21;color:#F5B700;padding:10px 16px;text-decoration:none;font-weight:bold">' +
      `Call ${escapeHtml(lead.name || "them")} back</a></p>`
    : "";
  return (
    '<div style="font-family:Helvetica,Arial,sans-serif;color:#1B1D21;max-width:640px">' +
    `<div style="background:#1B1D21;color:#F5B700;padding:12px 14px;font-size:18px;font-weight:bold">Quote request via ${HOST}</div>` +
    `<div style="padding:14px 0">${alert}<table style="border-collapse:collapse;width:100%;font-size:15px">${rows}</table>${callLink}` +
    '<p style="color:#6B675E;font-size:13px;margin-top:16px">Hitting Reply goes straight to the visitor when they left an email address.</p></div></div>'
  );
}

async function deliver(lead) {
  if (!transport) return { sent: false, reason: "GMAIL_USER / GMAIL_APP_PASSWORD missing" };
  try {
    const info = await transport.sendMail({
      from: `"${BRAND} website" <${gmailUser || "dry-run@localhost"}>`,
      to: inbox,
      replyTo: lead.email || undefined,
      subject: subjectLine(lead),
      html: emailHtml(lead),
    });
    if (dryRun) {
      const msg = JSON.parse(info.message);
      console.log(`[dry-run] would send to ${inbox}: "${msg.subject}"`);
    }
    return { sent: true };
  } catch (err) {
    return { sent: false, reason: err && err.message ? err.message : "unknown mail error" };
  }
}

app.post("/api/leads", async (req, res) => {
  const body = req.body || {};
  // Honeypots: a hidden text box and a hidden checkbox no person sees.
  if (body.company_url || body.not_human) return res.json({ ok: true, delivered: true });

  const lead = pickLead(body);
  if (!lead.name || !lead.phone || !lead.location) {
    return res.status(400).json({ ok: false, message: "Name, phone and the city or neighborhood are needed to send this." });
  }
  try {
    fs.appendFileSync(LEAD_LOG, JSON.stringify({ received: new Date().toISOString(), ip: req.ip, ...lead }) + "\n");
  } catch {
    // the log is only a safety copy; a write failure must not block the lead
  }
  const outcome = await deliver(lead);
  console.log(`[lead] ${lead.name} | ${lead.phone} | ${lead.location} | sent=${outcome.sent}${outcome.reason ? " | " + outcome.reason : ""}`);
  return res.json({ ok: true, delivered: outcome.sent });
});

app.get("/healthz", (_req, res) => {
  res.json({ status: "up", mail: dryRun ? "dry-run" : transport ? "gmail" : "not configured", inbox });
});

// ---------------------------------------------------------------- static files
app.use(
  express.static(SITE_DIR, {
    extensions: ["html"],
    setHeaders(res, filePath) {
      if (filePath.includes(path.sep + "assets" + path.sep)) {
        res.setHeader("Cache-Control", "public, max-age=31536000, immutable");
      } else if (filePath.endsWith(".html")) {
        res.setHeader("Cache-Control", "no-cache");
      } else {
        res.setHeader("Cache-Control", "public, max-age=3600");
      }
      res.setHeader("X-Content-Type-Options", "nosniff");
      res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
    },
  })
);

app.use((_req, res) => res.status(404).sendFile(path.join(SITE_DIR, "404.html")));

app.listen(port, () => {
  const mail = dryRun ? "dry run (logged, not sent)" : transport ? `sending to ${inbox}` : "OFF until GMAIL_USER and GMAIL_APP_PASSWORD are set";
  console.log(`${BRAND} up on port ${port}; lead mail ${mail}`);
});
