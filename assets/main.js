/* Miami Bee Rescue site script: menu, call/text tracking, quote form. */
(function () {
  "use strict";

  var PHONE = { label: "(786) 442-2496", dial: "+17864422496" };
  var INBOX = "removal@miamibeerescue.com";
  var API = "/api/leads";
  var SPARE_API = "https://api.web3forms.com/submit";
  var TRAPS = ["company_url", "not_human"];

  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }

  function safe(text) {
    return String(text == null ? "" : text).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- menu */
  var menuBtn = document.querySelector("[data-menu-button]");
  var menu = document.getElementById("site-menu");
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () {
      var open = !menu.classList.contains("open");
      menu.classList.toggle("open", open);
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.addEventListener("click", function (e) {
      if (!e.target.closest("a")) return;
      menu.classList.remove("open");
      menuBtn.setAttribute("aria-expanded", "false");
    });
  }

  /* ---------- call and text taps */
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="tel:"], a[href^="sms:"]');
    if (!a) return;
    var sms = a.getAttribute("href").slice(0, 4) === "sms:";
    track(sms ? "text_tap" : "call_tap", { page_path: location.pathname, spot: a.getAttribute("data-spot") || "" });
  });

  /* ---------- quote form */
  function collect(form) {
    var out = {};
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.type === "submit" || el.type === "button") return;
      // an unchecked box (including the hidden trap) is simply not sent
      if ((el.type === "checkbox" || el.type === "radio") && !el.checked) return;
      out[el.name] = typeof el.value === "string" ? el.value.trim() : el.value;
    });
    out.page = location.pathname;
    return out;
  }

  function spareSend(form, data) {
    var key = form.getAttribute("data-spare-key");
    if (!key) return Promise.resolve(false);
    var fd = new FormData();
    fd.append("access_key", key);
    fd.append("subject", "New Miami Bee Rescue Lead: " + data.name + " (" + data.location + ")");
    fd.append("from_name", "miamibeerescue.com form");
    Object.keys(data).forEach(function (k) {
      if (TRAPS.indexOf(k) === -1) fd.append(k, data[k]);
    });
    if (data.email) fd.append("replyto", data.email);
    return fetch(SPARE_API, { method: "POST", headers: { Accept: "application/json" }, body: fd })
      .then(function (r) { return r.json(); })
      .then(function (j) { return !!(j && j.success); })
      .catch(function () { return false; });
  }

  function mailLink(data) {
    var body = [
      "Name: " + data.name,
      "Phone: " + data.phone,
      "City or neighborhood: " + data.location,
      "Email: " + (data.email || "-"),
      "Where the bees are: " + (data.spot || "-"),
      "How urgent: " + (data.urgency || "-"),
      "Notes: " + (data.notes || "-")
    ].join("\n");
    return "mailto:" + INBOX + "?subject=" + encodeURIComponent("Bee removal request from " + data.name) +
      "&body=" + encodeURIComponent(body);
  }

  function showResult(form, data, ok) {
    var wrap = form.closest("[data-leadbox]") || form.parentNode;
    var first = safe((data.name || "").split(/\s+/)[0]);
    var head, para;
    if (ok) {
      head = first ? "Got it, " + first + "." : "Got it.";
      para = "Your request is in. When we call back, it will be from " + PHONE.label +
        ", so please pick up if you see that number. If the bees are near people right now, call instead of waiting.";
    } else {
      head = "That didn't send.";
      para = "Something on our side blocked the form, and nothing you typed was lost. Reach us one of these ways: tap Call, " +
        'tap Text a Photo, or <a href="' + mailLink(data) + '">open a pre-filled email to ' + INBOX + "</a>.";
    }
    wrap.innerHTML =
      '<div class="sent" role="status" tabindex="-1">' +
      "<p class=\"sent__head\">" + head + "</p>" +
      "<p>" + para + "</p>" +
      "<p>A clear photo of where the bees go in and out helps us plan the visit.</p>" +
      '<div class="sent__acts">' +
      '<a class="btn btn--call" data-spot="form-result" href="tel:' + PHONE.dial + '">Call ' + PHONE.label + "</a>" +
      '<a class="btn btn--text" data-spot="form-result" href="sms:' + PHONE.dial + '">Text a Photo</a>' +
      "</div></div>";
    var box = wrap.querySelector(".sent");
    if (box) {
      box.focus({ preventScroll: true });
      if (box.scrollIntoView) box.scrollIntoView({ block: "center", behavior: "smooth" });
    }
  }

  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form.matches || !form.matches("form[data-leadform]")) return;
    e.preventDefault();
    var data = collect(form);
    var note = form.querySelector("[data-form-note]");
    if (!data.name || !data.phone || !data.location) {
      if (note) {
        note.hidden = false;
        note.textContent = "Please fill in your name, a phone number, and the city or neighborhood where the bees are.";
      }
      return;
    }
    if (note) note.hidden = true;
    var btn = form.querySelector("button[type=submit]");
    if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }

    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json(); })
      .catch(function () { return null; })
      .then(function (res) {
        if (res && res.ok && res.delivered) return true;
        return spareSend(form, data);
      })
      .then(function (ok) {
        if (ok) track("generate_lead", { page_path: location.pathname, urgency: data.urgency || "" });
        showResult(form, data, ok);
      });
  });
})();
