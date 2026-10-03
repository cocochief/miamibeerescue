#!/usr/bin/env python3
"""Static site generator for miamibeerescue.com.

    python3 build.py      # regenerates public/ from content/ and assets/

Layout of the source:
    content/catalog.py    every URL on the site, plus link-token resolution
    content/core.py       copy for the homepage, hubs, cost, answers, about,
                          request, 404, llms.txt and the shared page chrome
    content/county.py     the county hub
    content/cities/       one module per place page
    content/services/     one module per removal page
    content/guides/       one module per field guide article
    assets/               style.css, main.js, logo PNGs, og.jpg

Output: folder URLs (public/<path>/index.html). Files in public/assets/ get
content-hashed names so the server can cache them for a year.
"""
import datetime, glob, hashlib, html, importlib, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
sys.path.insert(0, ROOT)

from content import catalog as CAT  # noqa: E402
from content.core import CORE  # noqa: E402
from content.es.core_es import CORE_ES  # noqa: E402

# ---------------------------------------------------------------- settings
BRAND = "Miami Bee Rescue"
SITE = "https://miamibeerescue.com"
PHONE = "(786) 442-2496"
DIAL = "+17864422496"
EMAIL = "removal@miamibeerescue.com"
COUNTY_NAME = "Miami-Dade County"
GTAG_ID = ""   # Google Analytics 4 measurement ID, e.g. "G-XXXXXXX"; blank = no tracking tag
W3F_KEY = ""   # optional Web3Forms access key used only if /api/leads fails
SOCIAL = {"google": "", "facebook": "", "instagram": "", "nextdoor": "", "yelp": ""}
TODAY = datetime.date.today()

PROBLEMS = []          # build stops if anything lands here
SITEMAP = []           # (path, priority)
MAINS = {}             # path -> <main> html, for lastmod hashing
SEEN_TITLES, SEEN_DESCS = {}, {}


def fail(msg):
    PROBLEMS.append(msg)


# ---------------------------------------------------------------- assets
ASSET_MAP = {}


def stage_assets():
    """Copy assets/ into public/assets/ with content-hashed names."""
    src_dir = os.path.join(ROOT, "assets")
    dst_dir = os.path.join(OUT, "assets")
    os.makedirs(dst_dir, exist_ok=True)
    for src in sorted(glob.glob(os.path.join(src_dir, "**", "*"), recursive=True)):
        if not os.path.isfile(src):
            continue
        name = os.path.relpath(src, src_dir).replace(os.sep, "/")   # e.g. "style.css", "photos/x-800.jpg"
        with open(src, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()[:10]
        stem, ext = os.path.splitext(name)
        hashed = f"{stem}.{digest}{ext}"
        os.makedirs(os.path.dirname(os.path.join(dst_dir, hashed)), exist_ok=True)
        shutil.copyfile(src, os.path.join(dst_dir, hashed))
        ASSET_MAP[name] = "/assets/" + hashed
    # stable-name copies for things requested by path
    for plain, target in (("favicon.png", "mark-48.png"), ("apple-touch-icon.png", "mark-apple.png")):
        if os.path.exists(os.path.join(src_dir, target)):
            shutil.copyfile(os.path.join(src_dir, target), os.path.join(OUT, plain))


def asset(name):
    if name not in ASSET_MAP:
        fail(f"missing asset {name}")
        return "/assets/" + name
    return ASSET_MAP[name]


# ---------------------------------------------------------------- content loading
def _load(pkg, mod, var):
    try:
        m = importlib.import_module(f"content.{pkg}.{mod}" if pkg else f"content.{mod}")
    except ModuleNotFoundError:
        return None
    return getattr(m, var, None)


SVC = {s: d for s, d in ((s, _load("services", s.replace("-", "_"), "SERVICE")) for s, _, _ in CAT.SERVICES) if d}
CITY = {k: d for k, d in ((k, _load("cities", k.replace("-", "_"), "CITY")) for k, *_ in CAT.CITIES) if d}
GUIDE = {g: d for g, d in ((g, _load("guides", g.replace("-", "_"), "GUIDE")) for g, _ in CAT.GUIDES) if d}
COUNTY = _load("", "county", "COUNTY")
ES_SVC = {s: d for s, d in ((s, _load("es.servicios", s.replace("-", "_"), "SERVICIO")) for s, _, _ in CAT.ES_SERVICES) if d}
ES_ZONA = {k: d for k, d in ((k, _load("es.zonas", k.replace("-", "_"), "ZONA")) for k in CAT.ES_PLACES) if d}


# ---------------------------------------------------------------- text helpers
def esc(s):
    return html.escape(str(s), quote=True)


TOKEN = re.compile(r"\[\[(city|svc|guide|page|es):([a-z0-9-]+)(?:\|([^\]]*))?\]\]")


def link_html(kind, ref, label=None):
    try:
        path, default = CAT.resolve(kind, ref)
    except KeyError:
        fail(f"unknown link [[{kind}:{ref}]]")
        return esc(label or ref)
    if kind == "city" and ref not in CITY:
        fail(f"link to unbuilt place page {ref}")
    if kind == "svc" and ref not in SVC:
        fail(f"link to unbuilt removal page {ref}")
    if kind == "guide" and ref not in GUIDE:
        fail(f"link to unbuilt guide {ref}")
    if kind == "es" and ((ref.startswith("svc-") and ref[4:] not in ES_SVC) or (ref.startswith("zona-") and ref[5:] not in ES_ZONA)):
        fail(f"link to unbuilt Spanish page {ref}")
    return f'<a href="{path}">{esc(label or default)}</a>'


def inline(s):
    """Escape a copy string and turn link tokens into anchors."""
    out, pos = [], 0
    for m in TOKEN.finditer(s):
        out.append(esc(s[pos:m.start()]))
        out.append(link_html(m.group(1), m.group(2), m.group(3)))
        pos = m.end()
    out.append(esc(s[pos:]))
    return "".join(out)


def plain(s):
    """Copy string with tokens reduced to their labels (for schema and meta)."""
    return TOKEN.sub(lambda m: m.group(3) or m.group(2), s)


def prose(s):
    """Paragraphs split on blank lines; runs of '- ' lines become lists."""
    blocks = []
    for para in [p.strip() for p in s.split("\n\n") if p.strip()]:
        lines = para.split("\n")
        buf, items = [], []
        for ln in lines:
            if ln.startswith("- "):
                if buf:
                    blocks.append("<p>" + inline(" ".join(buf)) + "</p>")
                    buf = []
                items.append("<li>" + inline(ln[2:].strip()) + "</li>")
            else:
                if items:
                    blocks.append('<ul class="ticks">' + "".join(items) + "</ul>")
                    items = []
                buf.append(ln.strip())
        if buf:
            blocks.append("<p>" + inline(" ".join(buf)) + "</p>")
        if items:
            blocks.append('<ul class="ticks">' + "".join(items) + "</ul>")
    return "".join(blocks)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", plain(s).lower()).strip("-")[:60]


def ld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")


# ---------------------------------------------------------------- icons (24px line icons)
def icon(name, cls="i"):
    paths = {
        "phone": '<path d="M5 3.5h3.2l1.6 4.2-2.1 1.5a12 12 0 0 0 7.1 7.1l1.5-2.1 4.2 1.6V19a1.8 1.8 0 0 1-1.9 1.8C10.4 20.3 3.7 13.6 3.2 5.4A1.8 1.8 0 0 1 5 3.5Z"/>',
        "chat": '<path d="M4 4.5h16v11H9.5L5 19.5v-4H4Z"/><circle cx="9" cy="10" r="1.6"/><path d="M12.5 13l2.2-2.6 2.3 2.6"/>',
        "form": '<path d="M6 3.5h9l3.5 3.5v13.5H6Z"/><path d="M14.5 3.5V7.5h4"/><path d="M9 11.5h6M9 15h6M9 18h3.5"/>',
        "alert": '<path d="M12 3.5 21.5 20h-19Z"/><path d="M12 9.5v5"/><circle cx="12" cy="17.3" r=".6"/>',
        "check": '<path d="M4.5 12.5 9.5 17.5 19.5 6.5"/>',
        "pin": '<path d="M12 21s-6.5-6.3-6.5-11a6.5 6.5 0 0 1 13 0c0 4.7-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/>',
        "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5.3l3.4 2.1"/>',
        "shield": '<path d="M12 3.2 19.5 6v5.6c0 4.4-3.1 8-7.5 9.2-4.4-1.2-7.5-4.8-7.5-9.2V6Z"/><path d="M8.8 12.2 11.2 14.5 15.5 9.7"/>',
        "heat": '<path d="M10 4.5a2 2 0 0 1 4 0v9.2a4 4 0 1 1-4 0Z"/><path d="M12 9v7"/>',
        "home": '<path d="M3.5 11.5 12 4l8.5 7.5"/><path d="M6 10v10h12V10"/><path d="M10 20v-5.5h4V20"/>',
        "tower": '<path d="M7 21V5.5L13 3v18"/><path d="M13 8.5h4.5V21"/><path d="M9.5 8h1M9.5 11.5h1M9.5 15h1M15 12h1M15 15.5h1"/><path d="M4.5 21h15"/>',
        "boat": '<path d="M3.5 15.5h17l-2.5 4h-12Z"/><path d="M12 3.5v12M12 4.5l6 8.5h-6"/>',
        "leaf": '<path d="M5 19c0-8 5-13.5 14-14 .2 9-5.5 14-14 14Z"/><path d="M5 19 13 11"/>',
        "arrow": '<path d="M5 12h13.5M13.5 6.5 19 12l-5.5 5.5"/>',
        "bee": '<ellipse cx="12" cy="13.5" rx="4" ry="5.5"/><path d="M8.3 12h7.4M8.6 15.3h6.8"/><path d="M10.5 8.3C8 5.5 5 6 5 8.2s3.4 2.5 5.6 1.2M13.5 8.3C16 5.5 19 6 19 8.2s-3.4 2.5-5.6 1.2"/>',
    }
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            f'{paths[name]}</svg>')


MARK_SVG = (
    '<svg class="mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
    '<rect width="64" height="64" fill="#1B1D21"/>'
    '<path d="M8 56V34a24 24 0 0 1 48 0v22" fill="none" stroke="#F5B700" stroke-width="4"/>'
    '<path d="M16 56V35a16 16 0 0 1 32 0v21" fill="none" stroke="#F5B700" stroke-width="2.5"/>'
    '<path d="M32 10v6M15 17l4 4.5M49 17l-4 4.5" stroke="#F5B700" stroke-width="2.5"/>'
    '<ellipse cx="32" cy="41" rx="7" ry="9.5" fill="#F5B700"/>'
    '<path d="M25.4 38h13.2M25.6 43.5h12.8M27 48.6h10" stroke="#1B1D21" stroke-width="2.4"/>'
    '<ellipse cx="25" cy="31" rx="6.5" ry="4" fill="#F7F3EA" transform="rotate(-28 25 31)"/>'
    '<ellipse cx="39" cy="31" rx="6.5" ry="4" fill="#F7F3EA" transform="rotate(28 39 31)"/>'
    '</svg>'
)


# ---------------------------------------------------------------- schema
BUSINESS_ID = SITE + "/#business"


def business_schema():
    served = [{"@type": "AdministrativeArea", "name": "Miami-Dade County, Florida"}]
    served += [{"@type": "City" if CAT.CITY_KIND[k] in ("city", "town", "village") else "Place",
                "name": f"{n}, Florida"} for k, n, *_ in CAT.CITIES]
    data = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "PestControl"],
        "@id": BUSINESS_ID,
        "name": BRAND,
        "url": SITE + "/",
        "telephone": DIAL,
        "email": EMAIL,
        "logo": SITE + asset("mark-512.png"),
        "image": SITE + asset("og.jpg"),
        "description": CORE["schema_description"],
        "areaServed": served,
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59"}],
        "knowsAbout": ["Live honey bee removal", "Beehive removal", "Bee swarm removal", "Honeycomb removal",
                       "Bee colony relocation"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Bee removal services",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {
                                "@type": "Service", "name": n, "url": SITE + CAT.svc_path(s)}}
                                for s, n, _ in CAT.SERVICES if s in SVC]},
    }
    links = [u for u in SOCIAL.values() if u]
    if links:
        data["sameAs"] = links
    return data


def crumbs_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
                                for i, (path, name) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": plain(q),
                            "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]}


def service_schema(name, path, desc, area):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "url": SITE + path,
            "description": desc, "serviceType": "Live honey bee removal",
            "provider": {"@id": BUSINESS_ID}, "areaServed": area}


def itemlist_schema(name, rows):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name,
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + p}
                                for i, (p, n) in enumerate(rows)]}


def county_area():
    return {"@type": "AdministrativeArea", "name": "Miami-Dade County, Florida"}


def place_area(key):
    return {"@type": "City" if CAT.CITY_KIND[key] in ("city", "town", "village") else "Place",
            "name": f"{CAT.CITY_NAME[key]}, Florida",
            "containedInPlace": county_area()}


# ---------------------------------------------------------------- shared pieces
C = CORE["chrome"]
CE = CORE_ES["chrome"]
LANG = {"es": False}      # set per page by the builders


def T():
    """Chrome text for the language of the page being built."""
    return CE if LANG["es"] else C


def FORM():
    return CORE_ES["form"] if LANG["es"] else CORE["form"]


def quote_page():
    return "/es/solicitar/" if LANG["es"] else "/request-removal/"


def btns(spot, quote_href="#request", size=""):
    s = f" btn--{size}" if size else ""
    return (f'<div class="acts">'
            f'<a class="btn btn--call{s}" data-spot="{spot}" href="tel:{DIAL}">{icon("phone")}<span>{esc(T()["call"])} {PHONE}</span></a>'
            f'<a class="btn btn--text{s}" data-spot="{spot}" href="sms:{DIAL}">{icon("chat")}<span>{esc(T()["text"])}</span></a>'
            f'<a class="btn btn--quote{s}" data-spot="{spot}" href="{quote_href}">{icon("form")}<span>{esc(T()["quote"])}</span></a>'
            f'</div>')


def quick_box(text):
    return (f'<aside class="quick" aria-label="{esc(T()["quick_label"])}"><p class="label">{esc(T()["quick_label"])}</p>'
            f'<p>{inline(text)}</p></aside>')


def alarm_box(text):
    return (f'<aside class="alarm" aria-label="{esc(T()["alarm_title"])}">{icon("alert")}<div>'
            f'<p class="alarm__title">{esc(T()["alarm_title"])}</p><p>{inline(text)}</p>'
            f'<a class="btn btn--call btn--sm" data-spot="alarm" href="tel:{DIAL}">{icon("phone")}<span>{PHONE}</span></a>'
            f'</div></aside>')


def band(pair, quote_href="#request"):
    head, line = pair
    return (f'<section class="band"><div class="wrap band__in"><div><p class="band__head">{inline(head)}</p>'
            f'<p>{inline(line)}</p></div>{btns("band", quote_href)}</div></section>')


def faq_block(faqs, heading):
    items = "".join(f'<details class="qa"><summary>{inline(q)}</summary><div>{prose(a)}</div></details>'
                    for q, a in faqs)
    return f'<section class="sect" id="questions"><h2>{esc(heading)}</h2><div class="qas">{items}</div></section>'


def crumbs_html(trail):
    parts = []
    for i, (path, name) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            parts.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def hero(kicker, h1, lede, trail=None, extra="", quote_href="#request"):
    crumb = crumbs_html(trail) if trail else ""
    return (f'<section class="hero"><div class="wrap">{crumb}<p class="kicker">{inline(kicker)}</p>'
            f'<h1>{esc(h1)}</h1><p class="lede">{inline(lede)}</p>{btns("hero", quote_href, "lg")}{extra}</div></section>')


def leadform(heading=None, place=None, fid="request"):
    F = FORM()
    spots = "".join(f'<option>{esc(o)}</option>' for o in F["spot_options"])
    urg = "".join(f'<option value="{esc(v)}">{esc(lbl)}</option>' for v, lbl in F["urgency_options"])
    loc = f' value="{esc(place)}"' if place else ""
    key = f' data-spare-key="{esc(W3F_KEY)}"' if W3F_KEY else ""
    L, P = F["labels"], F["placeholders"]
    return f'''<section class="leadbox" id="{fid}" data-leadbox><div class="leadbox__copy">
<h2>{esc(heading or F["heading"])}</h2><p>{inline(F["intro"])}</p>
<ul class="leadbox__alt"><li>{icon("phone")}<a href="tel:{DIAL}" data-spot="form-side">{PHONE}</a></li>
<li>{icon("chat")}<a href="sms:{DIAL}" data-spot="form-side">{esc(F["text_line"])}</a></li>
<li>{icon("clock")}<span>{esc(F["hours_line"])}</span></li></ul></div>
<form class="leadform" data-leadform action="/api/leads" method="post" novalidate{key}>
<div class="row2"><label>{esc(L["name"])} <b aria-hidden="true">*</b><input name="name" autocomplete="name" required placeholder="{esc(P["name"])}"></label>
<label>{esc(L["phone"])} <b aria-hidden="true">*</b><input name="phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="{esc(P["phone"])}"></label></div>
<label>{esc(L["location"])} <b aria-hidden="true">*</b><input name="location" autocomplete="address-level2" required placeholder="{esc(P["location"])}"{loc}></label>
<label>{esc(L["email"])} <i>{esc(F["optional"])}</i><input name="email" type="email" autocomplete="email" placeholder="{esc(P["email"])}"></label>
<div class="row2"><label>{esc(L["spot"])}<select name="spot"><option value="">{esc(F["choose"])}</option>{spots}</select></label>
<label>{esc(L["urgency"])}<select name="urgency">{urg}</select></label></div>
<label>{esc(L["notes"])} <i>{esc(F["optional"])}</i><textarea name="notes" rows="3" placeholder="{esc(P["notes"])}"></textarea></label>
<div class="trap" aria-hidden="true"><label>Company site<input name="company_url" tabindex="-1" autocomplete="off"></label>
<label><input type="checkbox" name="not_human" value="1" tabindex="-1"> Tick if you are a robot</label></div>
<p class="leadform__note" data-form-note role="alert" hidden></p>
<button class="btn btn--quote btn--lg" type="submit">{esc(F["submit"])}</button>
<p class="leadform__fine">{inline(F["fine"])}</p></form></section>'''


def section(h2, body, cls="sect", hid=None):
    i = f' id="{hid}"' if hid else ""
    return f'<section class="{cls}"{i}><h2>{inline(h2)}</h2>{prose(body)}</section>'


# ---------------------------------------------------------------- page shell
NAV = [("/removal/", "Removal"), ("/miami-dade/", "Areas"), ("/cost/", "Cost"),
       ("/field-guide/", "Field guide"), ("/answers/", "Answers"), ("/who-we-are/", "Who we are")]
NAV_ES = [("/es/#servicios", "Servicios"), ("/es/#zonas", "Zonas"), ("/es/precios/", "Precios"),
          ("/es/solicitar/", "Solicitar")]
EN_TO_ES = CAT.hreflang_pairs()
ES_TO_EN = {v: k for k, v in EN_TO_ES.items()}


def alternates(path):
    """(english path, spanish path) when both versions exist and are built, else None."""
    en, es = (ES_TO_EN.get(path), path) if path.startswith("/es/") else (path, EN_TO_ES.get(path))
    if not en or not es:
        return None
    if es.startswith("/es/servicios/") and es.split("/")[3] not in ES_SVC:
        return None
    if es.startswith("/es/zonas/") and es.split("/")[3] not in ES_ZONA:
        return None
    return en, es


def head(title, desc, path, schema, og_type="website", noindex=False):
    if title in SEEN_TITLES:
        fail(f"duplicate title on {path} and {SEEN_TITLES[title]}: {title}")
    if desc in SEEN_DESCS:
        fail(f"duplicate description on {path} and {SEEN_DESCS[desc]}")
    SEEN_TITLES[title], SEEN_DESCS[desc] = path, path
    if len(title) > 60:
        fail(f"title over 60 chars on {path}: {title}")
    if not 110 <= len(desc) <= 160:
        fail(f"description length {len(desc)} on {path}")
    url = SITE + path
    g = ""
    if GTAG_ID:
        g = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>'
             f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}"
             f"gtag('js',new Date());gtag('config','{GTAG_ID}');</script>")
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    canon = "" if noindex else f'<link rel="canonical" href="{url}">'
    es = LANG["es"]
    pair = None if noindex else alternates(path)
    hreflang = ""
    if pair:
        hreflang = (f'<link rel="alternate" hreflang="en-US" href="{SITE}{pair[0]}">\n'
                    f'<link rel="alternate" hreflang="es-US" href="{SITE}{pair[1]}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{SITE}{pair[0]}">')
    if es:
        switch = f'<a class="langswitch" href="{pair[0] if pair else "/"}" hreflang="en" lang="en">English</a>'
    else:
        switch = f'<a class="langswitch" href="{pair[1] if pair else "/es/"}" hreflang="es" lang="es">Español</a>'
    nav = NAV_ES if es else NAV
    home = "/es/" if es else "/"
    return f'''<!doctype html>
<html lang="{"es-US" if es else "en-US"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
{canon}
{hreflang}
<meta name="theme-color" content="#1B1D21">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{asset("og.jpg")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(T()["og_alt"])}">
<meta property="og:locale" content="{"es_US" if es else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{asset("mark-32.png")}">
<link rel="icon" type="image/png" sizes="48x48" href="{asset("mark-48.png")}">
<link rel="apple-touch-icon" href="{asset("mark-apple.png")}">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="{asset("style.css")}">
{g}{schema}
</head>
<body>
<a class="skip" href="#main">{esc(T()["skip"])}</a>
<div class="topline"><div class="wrap topline__in"><p>{icon("clock")}<span>{esc(T()["topline"])}</span></p>
<a href="tel:{DIAL}" data-spot="topline">{icon("phone")}<span>{PHONE}</span></a></div></div>
<header class="masthead"><div class="wrap masthead__in">
<a class="logo" href="{home}" aria-label="{BRAND} {"inicio" if es else "home"}">{MARK_SVG}<span class="logo__words"><b>Miami</b> Bee Rescue</span></a>
<nav id="site-menu" class="menu" aria-label="{"Principal" if es else "Main"}">{"".join(f'<a href="{p}">{esc(n)}</a>' for p, n in nav)}
<a class="menu__quote" href="{quote_page()}">{esc(T()["quote"])}</a>{switch}</nav>
<a class="btn btn--call btn--head" data-spot="header" href="tel:{DIAL}" aria-label="{esc(T()["call"])} {PHONE}">{icon("phone")}<span class="hide-s">{PHONE}</span><span class="show-s">{esc(T()["call"])}</span></a>
<button class="menubtn" type="button" data-menu-button aria-controls="site-menu" aria-expanded="false"><span></span><span></span><span></span><b class="sr">{esc(T()["menu"])}</b></button>
</div></header>
'''


def foot():
    F = T()["footer"]
    if LANG["es"]:
        svc_links = "".join(f'<li><a href="{CAT.es_svc_path(s)}">{esc(n)}</a></li>' for s, n, _ in CAT.ES_SERVICES if s in ES_SVC)
        city_links = "".join(f'<li><a href="{CAT.es_place_path(k)}">{esc(CAT.CITY_NAME[k])}</a></li>' for k in CAT.ES_PLACES if k in ES_ZONA)
        core_links = "".join(f'<li><a href="{p}">{esc(n)}</a></li>' for p, n, _ in CAT.ES_CORE.values())
        core_links += f'<li><a href="/" hreflang="en" lang="en">{esc(F["en_link"])}</a></li>'
        return _foot_html(F, svc_links, city_links, core_links, "/es/")
    svc_links = "".join(f'<li><a href="{CAT.svc_path(s)}">{esc(n)}</a></li>' for s, n, _ in CAT.SERVICES if s in SVC)
    city_links = "".join(f'<li><a href="{CAT.city_path(k)}">{esc(n)}</a></li>' for k, n, *_ in CAT.CITIES if k in CITY)
    core_links = "".join(f'<li><a href="{p}">{esc(n)}</a></li>' for p, n in
                         [CAT.CORE_PAGES[k] for k in ("cost", "answers", "guides", "who", "quote", "county")])
    core_links += '<li><a href="/es/" hreflang="es" lang="es">Español</a></li>'
    return _foot_html(F, svc_links, city_links, core_links, "/")


def _foot_html(F, svc_links, city_links, core_links, home):
    return f'''<footer class="foot"><div class="wrap">
<div class="foot__top"><div class="foot__brand"><a class="logo logo--foot" href="{home}">{MARK_SVG}<span class="logo__words"><b>Miami</b> Bee Rescue</span></a>
<p>{inline(F["about"])}</p><p class="foot__area">{icon("pin")}<span>{inline(F["area"])}</span></p>
<p class="foot__contact"><a href="tel:{DIAL}" data-spot="footer">{PHONE}</a><a href="sms:{DIAL}" data-spot="footer">{esc(T()["text"])}</a><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div class="foot__col"><p class="foot__h">{esc(F["h_removal"])}</p><ul>{svc_links}</ul></div>
<div class="foot__col foot__col--wide"><p class="foot__h">{esc(F["h_places"])}</p><ul class="cols2">{city_links}</ul></div>
<div class="foot__col"><p class="foot__h">{esc(F["h_company"])}</p><ul>{core_links}</ul></div></div>
<p class="foot__fine">&copy; {TODAY.year} {BRAND}. {esc(F["fine"])}</p></div></footer>
<nav class="dock" aria-label="{esc(T()["dock_label"])}">
<a class="dock__call" href="tel:{DIAL}" data-spot="dock">{icon("phone")}<span>{esc(T().get("dock_call", T()["call"]))}</span></a>
<a class="dock__text" href="sms:{DIAL}" data-spot="dock">{icon("chat")}<span>{esc(T()["dock_text"])}</span></a>
<a class="dock__quote" href="{quote_page()}" data-spot="dock">{icon("form")}<span>{esc(T()["dock_quote"])}</span></a></nav>
<script src="{asset("main.js")}" defer></script>
</body>
</html>
'''


def publish(path, title, desc, main_html, schemas=(), og_type="website", priority="0.7", noindex=False, filename=None):
    if main_html.count("<h1") != 1:
        fail(f"{path} has {main_html.count('<h1')} h1 tags")
    schema = "\n".join(ld(s) for s in schemas)
    page = head(title, desc, path, schema, og_type, noindex) + f'<main id="main">{main_html}</main>\n' + foot()
    rel = filename or (os.path.join(path.strip("/"), "index.html") if path.strip("/") else "index.html")
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(page)
    if not noindex:
        SITEMAP.append((path, priority))
        MAINS[path] = main_html


# ---------------------------------------------------------------- homepage
HOUSE_SPOTS = [
    # (service slug, x, y) on the 640x400 drawing
    ("roofs", 318, 78), ("soffits-eaves", 470, 150), ("walls", 250, 245),
    ("utility-boxes", 120, 360), ("trees-palms", 585, 120), ("pool-enclosures", 560, 318),
]


def house_svg():
    marks = []
    for i, (slug, x, y) in enumerate(HOUSE_SPOTS, 1):
        marks.append(f'<a href="{CAT.svc_path(slug)}" aria-label="{esc(CAT.SVC_NAME[slug])}">'
                     f'<circle cx="{x}" cy="{y}" r="17" class="hot"/><text x="{x}" y="{y + 6}" class="hotn">{i}</text></a>')
    return f'''<svg class="house" viewBox="0 0 640 400" role="img" aria-labelledby="house-t">
<title id="house-t">{esc(CORE["home"]["map_alt"])}</title>
<rect x="0" y="372" width="640" height="28" class="ground"/>
<path d="M150 170 318 62 486 170Z" class="roof"/>
<path d="M150 170h336" class="eave"/>
<path d="M168 178h300v194H168Z" class="wallp"/>
<path d="M168 178h300v10H168Z" class="soffit"/>
<g class="tiles">{"".join(f'<path d="M{190 + i * 22} {170 - (i if i < 7 else 14 - i) * 14}q11 -8 22 0"/>' for i in range(14))}</g>
<rect x="200" y="215" width="70" height="60" class="win"/><rect x="366" y="215" width="70" height="60" class="win"/>
<rect x="290" y="290" width="56" height="82" class="door"/>
<g class="block">{"".join(f'<path d="M{176 + (j % 2) * 18 + k * 36} {300 + j * 18}h30"/>' for j in range(4) for k in range(3))}</g>
<rect x="96" y="346" width="48" height="26" class="box"/><path d="M96 352h48" class="boxlid"/>
<path d="M585 372V150" class="trunk"/>
<g class="fronds"><path d="M585 150q-40-20-70 10"/><path d="M585 150q40-22 72 6"/><path d="M585 150q-20-38-58-40"/><path d="M585 150q18-40 54-44"/><path d="M585 150q-6-36 4-58"/></g>
<path d="M498 372V262h124v110" class="cage"/><path d="M498 262l62-30 62 30M529 247v125M560 232v140M591 247v125" class="cage"/>
<path d="M506 372q54-22 108 0" class="pool"/>
{"".join(marks)}
</svg>'''


def build_home():
    H = CORE["home"]
    tiles = "".join(
        f'<a class="tile tile--{t["tone"]}" href="{t["href"]}">{icon(t["icon"])}<span class="tile__h">{esc(t["head"])}</span>'
        f'<span>{esc(t["text"])}</span><span class="tile__go">{esc(t["go"])} {icon("arrow", "i i--s")}</span></a>'
        for t in H["triage"])
    legend = "".join(f'<li><span class="num">{i}</span><a href="{CAT.svc_path(s)}">{esc(CAT.SVC_NAME[s])}</a>'
                     f'<span>{esc(H["map_notes"][s])}</span></li>' for i, (s, *_r) in enumerate(HOUSE_SPOTS, 1))
    steps = "".join(f'<li><p class="step__h">{esc(h)}</p><p>{inline(t)}</p></li>' for h, t in H["steps"])
    props = "".join(f'<a class="prop" href="{CAT.svc_path(s)}">{icon(ic)}<span class="prop__h">{esc(h)}</span>'
                    f'<span>{esc(t)}</span></a>' for s, ic, h, t in H["properties"])
    regions = []
    for rid, rname in CAT.REGIONS:
        links = "".join(f'<li><a href="{CAT.city_path(k)}">{esc(n)}</a></li>'
                        for k, n, _, r, _ in CAT.CITIES if r == rid and k in CITY)
        regions.append(f'<div class="region"><h3>{esc(rname)}</h3><ul>{links}</ul></div>')
    guides = "".join(f'<a class="card" href="{CAT.guide_path(g)}"><span class="card__h">{esc(GUIDE[g]["h1"])}</span>'
                     f'<span>{esc(plain(GUIDE[g]["card"]))}</span></a>' for g, _ in CAT.GUIDES[:4] if g in GUIDE)
    trust = "".join(f'<li>{icon(ic)}<span>{esc(t)}</span></li>' for ic, t in H["trust"])
    main = (
        f'<section class="hero hero--home"><div class="wrap hero__grid"><div>'
        f'<p class="kicker">{esc(H["kicker"])}</p><h1>{esc(H["h1"])}</h1><p class="lede">{inline(H["lede"])}</p>'
        f'{btns("hero", "#request", "lg")}</div><ul class="trust">{trust}</ul></div></section>'
        f'<div class="wrap">{quick_box(H["quick"])}</div>'
        f'<section class="sect wrap"><h2>{esc(H["triage_h"])}</h2><p class="sub">{inline(H["triage_sub"])}</p><div class="tiles">{tiles}</div></section>'
        f'<section class="sect sect--tint"><div class="wrap map"><div><h2>{esc(H["map_h"])}</h2><p>{inline(H["map_sub"])}</p>'
        f'<ol class="legend">{legend}</ol></div>{house_svg()}</div></section>'
        f'<section class="sect wrap"><h2>{esc(H["steps_h"])}</h2><ol class="steps">{steps}</ol></section>'
        f'<section class="price"><div class="wrap price__in"><div><p class="kicker kicker--dark">{esc(H["price_kicker"])}</p>'
        f'<h2>{esc(H["price_h"])}</h2>{prose(H["price"])}<a class="more" href="/cost/">{esc(H["price_more"])} {icon("arrow", "i i--s")}</a></div>'
        f'<div class="price__figs"><p><b>$300–$400</b><span>{esc(H["fig_low"])}</span></p>'
        f'<p><b>{esc(H["fig_high_b"])}</b><span>{esc(H["fig_high"])}</span></p></div></div></section>'
        f'<section class="sect wrap"><h2>{esc(H["props_h"])}</h2><p class="sub">{inline(H["props_sub"])}</p><div class="props">{props}</div></section>'
        f'<section class="sect sect--tint"><div class="wrap"><h2>{esc(H["regions_h"])}</h2><p class="sub">{inline(H["regions_sub"])}</p>'
        f'<div class="regions">{"".join(regions)}</div><a class="more" href="/miami-dade/">{esc(H["regions_more"])} {icon("arrow", "i i--s")}</a></div></section>'
        f'<section class="sect wrap"><h2>{esc(H["guides_h"])}</h2><div class="cards">{guides}</div>'
        f'<a class="more" href="/field-guide/">{esc(H["guides_more"])} {icon("arrow", "i i--s")}</a></section>'
        f'<div class="wrap">{faq_block(H["faqs"], H["faqs_h"])}</div>'
        f'<div class="wrap">{leadform(H["form_h"])}</div>'
    )
    site_schema = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE + "/",
                   "publisher": {"@id": BUSINESS_ID}}
    publish("/", H["title"], H["desc"], main,
            [business_schema(), site_schema, faq_schema(H["faqs"]),
             itemlist_schema(H["regions_h"], [(CAT.city_path(k), n) for k, n, *_ in CAT.CITIES if k in CITY])],
            priority="1.0")


# ---------------------------------------------------------------- removal hub + pages
def build_removal_hub():
    R = CORE["removal_hub"]
    trail = [("/", "Home"), ("/removal/", CAT.CORE_PAGES["removal"][1])]
    groups = []
    for gid, gname in CAT.SERVICE_GROUPS:
        cards = "".join(f'<a class="card" href="{CAT.svc_path(s)}"><span class="card__h">{esc(n)}</span>'
                        f'<span>{esc(plain(SVC[s]["card"]))}</span></a>'
                        for s, n, g in CAT.SERVICES if g == gid and s in SVC)
        groups.append(f'<section class="sect"><h2>{esc(gname)}</h2><p class="sub">{inline(R["groups"][gid])}</p>'
                      f'<div class="cards">{cards}</div></section>')
    main = (hero(R["kicker"], R["h1"], R["lede"], trail) + f'<div class="wrap">{quick_box(R["quick"])}'
            + "".join(groups[:2]) + f'</div>{band(R["band"])}<div class="wrap">' + "".join(groups[2:])
            + section(R["after_h"], R["after"]) + leadform() + '</div>')
    publish("/removal/", R["title"], R["desc"], main,
            [crumbs_schema(trail), itemlist_schema(R["h1"], [(CAT.svc_path(s), n) for s, n, _ in CAT.SERVICES if s in SVC])],
            priority="0.9")


def build_service(slug):
    d = SVC[slug]
    path = CAT.svc_path(slug)
    name = CAT.SVC_NAME[slug]
    trail = [("/", "Home"), ("/removal/", CAT.CORE_PAGES["removal"][1]), (path, name)]
    seeing = "".join(f'<li>{icon("check")}<span>{inline(x)}</span></li>' for x in d["seeing"])
    take = "".join(f'<li><p class="step__h">{inline(h)}</p><p>{inline(t)}</p></li>' for h, t in d["takeout"])
    factors = "".join(f"<li>{inline(x)}</li>" for x in d["price_factors"])
    local = "".join(f'<li><a href="{CAT.city_path(k)}">{esc(CAT.CITY_NAME[k])}</a><p>{inline(t)}</p></li>'
                    for k, t in d["miami"] if k in CITY)
    rel = "".join(f'<a class="chip" href="{CAT.svc_path(s)}">{esc(CAT.SVC_NAME[s])}</a>' for s in d["related"] if s in SVC)
    body = "".join(section(h, t) for h, t in d["body"])
    main = (
        hero(d["kicker"], d["h1"], d["lede"], trail)
        + f'<div class="wrap"><div class="pair">{quick_box(d["quick"])}{alarm_box(d["alarm"])}</div>'
        + f'<section class="sect"><h2>{inline(d["seeing_h"])}</h2><ul class="seeing">{seeing}</ul></section>'
        + section(C["behind_h"], d["behind"]) + body + "</div>"
        + band(d["band"])
        + f'<div class="wrap"><section class="sect"><h2>{inline(d["takeout_h"])}</h2><ol class="steps">{take}</ol></section>'
        + section(C["putback_h"], d["putback"])
        + f'<section class="costbox"><h2>{esc(C["cost_h"])}</h2>{prose(d["price"])}<ul class="ticks">{factors}</ul>'
          f'<a class="more" href="/cost/">{esc(C["cost_more"])} {icon("arrow", "i i--s")}</a></section>'
        + f'<section class="sect"><h2>{inline(d["miami_h"])}</h2><ul class="local">{local}</ul></section>'
        + faq_block(d["faqs"], C["faq_h"])
        + f'<section class="sect"><h2>{esc(C["related_h"])}</h2><div class="chips">{rel}</div></section>'
        + f'<div class="closing"><p class="closing__h">{inline(d["close"][0])}</p><p>{inline(d["close"][1])}</p></div>'
        + leadform() + "</div>"
    )
    publish(path, d["title"], d["desc"], main,
            [crumbs_schema(trail), service_schema(name, path, d["desc"], county_area()), faq_schema(d["faqs"])],
            priority="0.8")


# ---------------------------------------------------------------- county hub + place pages
def build_county():
    d = COUNTY
    trail = [("/", "Home"), ("/miami-dade/", CAT.CORE_PAGES["county"][1])]
    regions = []
    for rid, rname in CAT.REGIONS:
        cards = "".join(f'<a class="card card--place" href="{CAT.city_path(k)}"><span class="card__h">{esc(n)}</span>'
                        f'<span class="card__kind">{esc(C["kinds"][CAT.CITY_KIND[k]])}</span>'
                        f'<span>{esc(plain(CITY[k]["card"]))}</span></a>'
                        for k, n, _, r, _ in CAT.CITIES if r == rid and k in CITY)
        others = CAT.OTHER_PLACES.get(rid, [])
        also = f'<p class="also"><b>{esc(C["also_served"])}</b> {esc(", ".join(others))}.</p>' if others else ""
        regions.append(f'<section class="region-block" id="{rid}"><h2>{esc(rname)}</h2>{prose(d["regions"][rid])}'
                       f'<div class="cards">{cards}</div>{also}</section>')
    allothers = sorted(p for v in CAT.OTHER_PLACES.values() for p in v)
    body = "".join(section(h, t) for h, t in d["body"])
    main = (
        hero(d["kicker"], d["h1"], d["lede"], trail)
        + f'<div class="wrap"><div class="pair">{quick_box(d["quick"])}{alarm_box(d["alarm"])}</div>'
        + f'<section class="sect">{prose(d["opening"])}</section>'
        + f'<nav class="jump" aria-label="{esc(C["jump_label"])}">'
        + "".join(f'<a href="#{rid}">{esc(rn)}</a>' for rid, rn in CAT.REGIONS) + "</nav>"
        + "".join(regions[:3]) + "</div>" + band(d["band"]) + '<div class="wrap">' + "".join(regions[3:])
        + f'<section class="sect"><h2>{inline(d["others_h"])}</h2>{prose(d["others"])}'
          f'<ul class="plainlist">{"".join(f"<li>{esc(p)}</li>" for p in allothers)}</ul></section>'
        + body + faq_block(d["faqs"], C["faq_h"])
        + f'<div class="closing"><p class="closing__h">{inline(d["close"][0])}</p><p>{inline(d["close"][1])}</p></div>'
        + leadform() + "</div>"
    )
    publish("/miami-dade/", d["title"], d["desc"], main,
            [crumbs_schema(trail), service_schema("Live honey bee removal in Miami-Dade County", "/miami-dade/", d["desc"], county_area()),
             faq_schema(d["faqs"]), itemlist_schema(d["h1"], [(CAT.city_path(k), n) for k, n, *_ in CAT.CITIES if k in CITY])],
            priority="0.9")


def build_city(key):
    d = CITY[key]
    name = CAT.CITY_NAME[key]
    path = CAT.city_path(key)
    trail = [("/", "Home"), ("/miami-dade/", CAT.CORE_PAGES["county"][1]), (path, name)]
    glance = "".join(f'<li><span class="glance__k">{inline(k)}</span><span class="glance__v">{inline(v)}</span></li>'
                     for k, v in d["glance"])
    spots = "".join(f'<div class="spot">{icon("bee")}<p class="spot__h">{inline(h)}</p><p>{inline(t)}</p></div>'
                    for h, t in d["hotspots"])
    streets = "".join(f'<li><p class="street__h">{inline(h)}</p><p>{inline(t)}</p></li>' for h, t in d["streets"])
    visit = "".join(f'<li><p class="step__h">{inline(h)}</p><p>{inline(t)}</p></li>' for h, t in d["visit"])
    svcs = "".join(f'<a class="card" href="{CAT.svc_path(s)}"><span class="card__h">{esc(CAT.SVC_NAME[s])}</span>'
                   f'<span>{esc(plain(t))}</span></a>' for s, t in d["services"] if s in SVC)
    near = "".join(f'<a class="chip" href="{CAT.city_path(k)}">{esc(CAT.CITY_NAME[k])}</a>' for k in d["nearby"] if k in CITY)
    body = "".join(section(h, t) for h, t in d["body"])
    region = CAT.CITY_REGION[key]
    main = (
        hero(d["kicker"], d["h1"], d["lede"], trail)
        + f'<div class="wrap"><div class="pair">{quick_box(d["quick"])}{alarm_box(d["alarm"])}</div>'
        + f'<section class="glance" aria-label="{esc(C["glance_label"])} {esc(name)}"><p class="label">{esc(C["glance_label"])} {esc(name)}</p><ul>{glance}</ul></section>'
        + f'<section class="sect">{prose(d["opening"])}</section>'
        + f'<section class="sect"><h2>{inline(d["hotspots_h"])}</h2><div class="spots">{spots}</div></section></div>'
        + band(d["band"])
        + f'<div class="wrap"><section class="sect"><h2>{inline(d["streets_h"])}</h2><ul class="streets">{streets}</ul></section>'
        + body
        + f'<section class="sect"><h2>{inline(d["visit_h"])}</h2><ol class="steps">{visit}</ol></section>'
        + f'<section class="sect"><h2>{esc(C["fits_h"])}</h2><div class="cards">{svcs}</div></section>'
        + faq_block(d["faqs"], C["faq_h"])
        + f'<section class="sect"><h2>{esc(C["near_h"])}</h2><div class="chips">{near}'
          f'<a class="chip chip--all" href="/miami-dade/#{region}">{esc(CAT.REGION_NAME[region])}</a></div></section>'
        + f'<div class="closing"><p class="closing__h">{inline(d["close"][0])}</p><p>{inline(d["close"][1])}</p></div>'
        + leadform(place=name) + "</div>"
    )
    publish(path, d["title"], d["desc"], main,
            [crumbs_schema(trail), service_schema(f"Live bee removal in {name}", path, d["desc"], place_area(key)),
             faq_schema(d["faqs"])],
            priority="0.9" if CAT.CITY_TIER[key] == "primary" else "0.8")


# ---------------------------------------------------------------- guides
def build_guides_hub():
    G = CORE["guides_hub"]
    trail = [("/", "Home"), ("/field-guide/", CAT.CORE_PAGES["guides"][1])]
    cards = "".join(f'<a class="card card--guide" href="{CAT.guide_path(g)}"><span class="card__h">{esc(GUIDE[g]["h1"])}</span>'
                    f'<span>{esc(plain(GUIDE[g]["card"]))}</span><span class="card__go">{esc(G["read"])} {icon("arrow", "i i--s")}</span></a>'
                    for g, _ in CAT.GUIDES if g in GUIDE)
    main = (hero(G["kicker"], G["h1"], G["lede"], trail) + f'<div class="wrap">{quick_box(G["quick"])}'
            + f'<section class="sect"><h2>{esc(G["list_h"])}</h2><div class="cards">{cards}</div></section>'
            + section(G["note_h"], G["note"]) + leadform() + "</div>")
    publish("/field-guide/", G["title"], G["desc"], main,
            [crumbs_schema(trail), itemlist_schema(G["h1"], [(CAT.guide_path(g), GUIDE[g]["h1"]) for g, _ in CAT.GUIDES if g in GUIDE])],
            priority="0.7")


def build_guide(slug):
    d = GUIDE[slug]
    path = CAT.guide_path(slug)
    trail = [("/", "Home"), ("/field-guide/", CAT.CORE_PAGES["guides"][1]), (path, CAT.GUIDE_NAME[slug])]
    ids = [slugify(h) for h, _ in d["body"]]
    toc = "".join(f'<li><a href="#{i}">{esc(plain(h))}</a></li>' for i, (h, _) in zip(ids, d["body"]))
    parts = []
    check = "".join(f"<li>{inline(x)}</li>" for x in d["checklist"])
    checkbox = f'<aside class="checklist"><h2>{inline(d["checklist_h"])}</h2><ol>{check}</ol></aside>'
    for n, ((h, t), i) in enumerate(zip(d["body"], ids), 1):
        parts.append(section(h, t, hid=i))
        if n == 3:
            parts.append("</div>" + band(d["band"]) + '<div class="wrap wrap--read">')
        if n == min(5, len(d["body"])):
            parts.append(checkbox)
    svcs = "".join(f'<a class="chip" href="{CAT.svc_path(s)}">{esc(CAT.SVC_NAME[s])}</a>' for s in d["services"] if s in SVC)
    places = "".join(f'<a class="chip" href="{CAT.city_path(k)}">{esc(CAT.CITY_NAME[k])}</a>' for k in d["places"] if k in CITY)
    stamp = datetime.date.fromisoformat(d["date"])
    dated = f'<p class="dated">{esc(C["updated"])} <time datetime="{d["date"]}">{stamp.strftime("%B")} {stamp.day}, {stamp.year}</time></p>'
    main = (
        hero(d["kicker"], d["h1"], d["lede"], trail, extra=dated)
        + f'<div class="wrap wrap--read">{quick_box(d["quick"])}'
        + f'<nav class="toc" aria-label="{esc(C["toc"])}"><p class="label">{esc(C["toc"])}</p><ol>{toc}</ol></nav>'
        + "".join(parts)
        + faq_block(d["faqs"], C["faq_h"])
        + f'<section class="sect"><h2>{esc(C["guide_svcs_h"])}</h2><div class="chips">{svcs}</div>'
          f'<h3 class="h3gap">{esc(C["guide_places_h"])}</h3><div class="chips">{places}</div></section></div>'
        + f'<div class="wrap">{leadform()}</div>'
    )
    article = {"@context": "https://schema.org", "@type": "Article", "headline": d["h1"], "description": d["desc"],
               "datePublished": d["date"], "dateModified": d["date"], "mainEntityOfPage": SITE + path,
               "image": SITE + asset("og.jpg"),
               "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
               "publisher": {"@id": BUSINESS_ID}}
    publish(path, d["title"], d["desc"], main, [crumbs_schema(trail), article, faq_schema(d["faqs"])],
            og_type="article", priority="0.6")


# ---------------------------------------------------------------- core pages
def build_cost():
    P = CORE["cost"]
    trail = [("/", "Home"), ("/cost/", CAT.CORE_PAGES["cost"][1])]
    tiers = "".join(f'<div class="tier"><p class="tier__fig">{esc(f)}</p><p class="tier__h">{esc(h)}</p>{prose(t)}</div>'
                    for f, h, t in P["tiers"])
    drivers = "".join(f'<li><p class="street__h">{esc(h)}</p><p>{inline(t)}</p></li>' for h, t in P["drivers"])
    main = (hero(P["kicker"], P["h1"], P["lede"], trail) + f'<div class="wrap">{quick_box(P["quick"])}'
            + f'<section class="sect"><h2>{esc(P["tiers_h"])}</h2><div class="tiers">{tiers}</div></section>'
            + f'<section class="sect"><h2>{esc(P["drivers_h"])}</h2><ul class="streets">{drivers}</ul></section></div>'
            + band(P["band"]) + '<div class="wrap">'
            + "".join(section(h, t) for h, t in P["body"])
            + faq_block(P["faqs"], C["faq_h"]) + leadform(P["form_h"]) + "</div>")
    publish("/cost/", P["title"], P["desc"], main,
            [crumbs_schema(trail), service_schema("Bee removal quote and pricing", "/cost/", P["desc"], county_area()),
             faq_schema(P["faqs"])], priority="0.8")


def build_answers():
    A = CORE["answers"]
    trail = [("/", "Home"), ("/answers/", CAT.CORE_PAGES["answers"][1])]
    blocks, allq = [], []
    for gh, items in A["groups"]:
        allq += items
        qs = "".join(f'<details class="qa"><summary>{inline(q)}</summary><div>{prose(a)}</div></details>' for q, a in items)
        blocks.append(f'<section class="sect" id="{slugify(gh)}"><h2>{esc(gh)}</h2><div class="qas">{qs}</div></section>')
    jump = "".join(f'<a href="#{slugify(gh)}">{esc(gh)}</a>' for gh, _ in A["groups"])
    main = (hero(A["kicker"], A["h1"], A["lede"], trail) + f'<div class="wrap">{quick_box(A["quick"])}'
            + f'<nav class="jump" aria-label="{esc(C["jump_label"])}">{jump}</nav>'
            + "".join(blocks[:2]) + "</div>" + band(A["band"]) + '<div class="wrap">' + "".join(blocks[2:])
            + leadform() + "</div>")
    publish("/answers/", A["title"], A["desc"], main, [crumbs_schema(trail), faq_schema(allq)], priority="0.7")


def build_who():
    W = CORE["who"]
    trail = [("/", "Home"), ("/who-we-are/", CAT.CORE_PAGES["who"][1])]
    commits = "".join(f'<li>{icon(ic)}<div><p class="street__h">{esc(h)}</p><p>{inline(t)}</p></div></li>'
                      for ic, h, t in W["commitments"])
    main = (hero(W["kicker"], W["h1"], W["lede"], trail) + f'<div class="wrap">{quick_box(W["quick"])}'
            + "".join(section(h, t) for h, t in W["body"][:2])
            + f'<section class="sect"><h2>{esc(W["commit_h"])}</h2><ul class="commits">{commits}</ul></section></div>'
            + band(W["band"]) + '<div class="wrap">' + "".join(section(h, t) for h, t in W["body"][2:])
            + leadform() + "</div>")
    about = {"@context": "https://schema.org", "@type": "AboutPage", "name": W["h1"], "url": SITE + "/who-we-are/",
             "about": {"@id": BUSINESS_ID}}
    publish("/who-we-are/", W["title"], W["desc"], main, [crumbs_schema(trail), about, business_schema()], priority="0.5")


def build_request():
    Q = CORE["request"]
    trail = [("/", "Home"), ("/request-removal/", CAT.CORE_PAGES["quote"][1])]
    ways = "".join(f'<li>{icon(ic)}<div><p class="street__h">{esc(h)}</p><p>{inline(t)}</p></div></li>' for ic, h, t in Q["ways"])
    main = (hero(Q["kicker"], Q["h1"], Q["lede"], trail) + f'<div class="wrap"><div class="pair">{quick_box(Q["quick"])}{alarm_box(Q["alarm"])}</div>'
            + leadform(Q["form_h"])
            + f'<section class="sect"><h2>{esc(Q["ways_h"])}</h2><ul class="commits">{ways}</ul></section>'
            + "".join(section(h, t) for h, t in Q["body"]) + "</div>")
    contact = {"@context": "https://schema.org", "@type": "ContactPage", "name": Q["h1"], "url": SITE + "/request-removal/",
               "about": {"@id": BUSINESS_ID}}
    publish("/request-removal/", Q["title"], Q["desc"], main, [crumbs_schema(trail), contact], priority="0.8")


def build_404():
    N = CORE["notfound"]
    links = "".join(f'<li><a href="{p}">{esc(t)}</a></li>' for p, t in N["links"])
    main = (f'<section class="hero"><div class="wrap"><p class="kicker">{esc(N["kicker"])}</p><h1>{esc(N["h1"])}</h1>'
            f'<p class="lede">{inline(N["lede"])}</p>{btns("404", "/request-removal/", "lg")}</div></section>'
            f'<div class="wrap"><section class="sect"><h2>{esc(N["links_h"])}</h2><ul class="plainlist plainlist--links">{links}</ul></section></div>')
    publish("/404.html", N["title"], N["desc"], main, noindex=True, filename="404.html")


# ---------------------------------------------------------------- Spanish section (/es/)
def spanish(fn):
    """Run a builder with Spanish chrome, form text and links."""
    def run(*a):
        LANG["es"] = True
        try:
            fn(*a)
        finally:
            LANG["es"] = False
    return run


def es_service_schema(name, path, desc, area):
    d = service_schema(name, path, desc, area)
    d["inLanguage"] = "es"
    return d


@spanish
def build_es_home():
    H = CORE_ES["home"]
    tiles = "".join(
        f'<a class="tile tile--{t["tone"]}" href="{t["href"]}">{icon(t["icon"])}<span class="tile__h">{esc(t["head"])}</span>'
        f'<span>{esc(t["text"])}</span><span class="tile__go">{esc(t["go"])} {icon("arrow", "i i--s")}</span></a>'
        for t in H["triage"])
    steps = "".join(f'<li><p class="step__h">{esc(h)}</p><p>{inline(t)}</p></li>' for h, t in H["steps"])
    trust = "".join(f'<li>{icon(ic)}<span>{esc(t)}</span></li>' for ic, t in H["trust"])
    svcs = "".join(f'<a class="card" href="{CAT.es_svc_path(sl)}"><span class="card__h">{esc(n)}</span>'
                   f'<span>{esc(plain(ES_SVC[sl]["card"]))}</span></a>' for sl, n, _ in CAT.ES_SERVICES if sl in ES_SVC)
    places = "".join(f'<a class="card card--place" href="{CAT.es_place_path(k)}"><span class="card__h">{esc(CAT.CITY_NAME[k])}</span>'
                     f'<span class="card__kind">{esc(CE["kinds"][CAT.CITY_KIND[k]])}</span>'
                     f'<span>{esc(plain(ES_ZONA[k]["card"]))}</span></a>' for k in CAT.ES_PLACES if k in ES_ZONA)
    main = (
        f'<section class="hero hero--home"><div class="wrap hero__grid"><div>'
        f'<p class="kicker">{esc(H["kicker"])}</p><h1>{esc(H["h1"])}</h1><p class="lede">{inline(H["lede"])}</p>'
        f'{btns("hero", "#request", "lg")}</div><ul class="trust">{trust}</ul></div></section>'
        f'<div class="wrap">{quick_box(H["quick"])}</div>'
        f'<section class="sect wrap"><h2>{esc(H["triage_h"])}</h2><p class="sub">{inline(H["triage_sub"])}</p><div class="tiles">{tiles}</div></section>'
        f'<section class="sect sect--tint" id="servicios"><div class="wrap"><h2>{esc(H["svcs_h"])}</h2><p class="sub">{inline(H["svcs_sub"])}</p>'
        f'<div class="cards">{svcs}</div></div></section>'
        f'<section class="sect wrap"><h2>{esc(H["steps_h"])}</h2><ol class="steps">{steps}</ol></section>'
        f'<section class="price"><div class="wrap price__in"><div><p class="kicker kicker--dark">{esc(H["price_kicker"])}</p>'
        f'<h2>{esc(H["price_h"])}</h2>{prose(H["price"])}<a class="more" href="/es/precios/">{esc(H["price_more"])} {icon("arrow", "i i--s")}</a></div>'
        f'<div class="price__figs"><p><b>$300–$400</b><span>{esc(H["fig_low"])}</span></p>'
        f'<p><b>{esc(H["fig_high_b"])}</b><span>{esc(H["fig_high"])}</span></p></div></div></section>'
        f'<section class="sect wrap" id="zonas"><h2>{esc(H["places_h"])}</h2><p class="sub">{inline(H["places_sub"])}</p><div class="cards">{places}</div></section>'
        f'<div class="wrap">{faq_block(H["faqs"], H["faqs_h"])}</div>'
        f'<div class="wrap">{leadform(H["form_h"])}</div>'
    )
    site_schema = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE + "/es/",
                   "inLanguage": "es", "publisher": {"@id": BUSINESS_ID}}
    publish("/es/", H["title"], H["desc"], main,
            [business_schema(), site_schema, faq_schema(H["faqs"]),
             itemlist_schema(H["places_h"], [(CAT.es_place_path(k), CAT.CITY_NAME[k]) for k in CAT.ES_PLACES if k in ES_ZONA])],
            priority="0.9")


@spanish
def build_es_service(slug):
    d = ES_SVC[slug]
    path = CAT.es_svc_path(slug)
    name = CAT.ES_SVC_NAME[slug]
    trail = [("/es/", CE["home_crumb"]), (path, name)]
    seeing = "".join(f'<li>{icon("check")}<span>{inline(x)}</span></li>' for x in d["seeing"])
    take = "".join(f'<li><p class="step__h">{inline(h)}</p><p>{inline(t)}</p></li>' for h, t in d["takeout"])
    factors = "".join(f"<li>{inline(x)}</li>" for x in d["price_factors"])
    local = "".join(f'<li><a href="{CAT.es_place_path(k)}">{esc(CAT.CITY_NAME[k])}</a><p>{inline(t)}</p></li>'
                    for k, t in d["zonas"] if k in ES_ZONA)
    rel = "".join(f'<a class="chip" href="{CAT.es_svc_path(x)}">{esc(CAT.ES_SVC_NAME[x])}</a>' for x in d["relacionados"] if x in ES_SVC)
    main = (
        hero(d["kicker"], d["h1"], d["lede"], trail)
        + f'<div class="wrap"><div class="pair">{quick_box(d["quick"])}{alarm_box(d["alarm"])}</div>'
        + f'<section class="sect"><h2>{inline(d["seeing_h"])}</h2><ul class="seeing">{seeing}</ul></section>'
        + section(CE["behind_h"], d["behind"]) + "".join(section(h, t) for h, t in d["body"]) + "</div>"
        + band(d["band"])
        + f'<div class="wrap"><section class="sect"><h2>{inline(d["takeout_h"])}</h2><ol class="steps">{take}</ol></section>'
        + section(CE["putback_h"], d["putback"])
        + f'<section class="costbox"><h2>{esc(CE["cost_h"])}</h2>{prose(d["price"])}<ul class="ticks">{factors}</ul>'
          f'<a class="more" href="/es/precios/">{esc(CE["cost_more"])} {icon("arrow", "i i--s")}</a></section>'
        + f'<section class="sect"><h2>{inline(d["zonas_h"])}</h2><ul class="local">{local}</ul></section>'
        + faq_block(d["faqs"], CE["faq_h"])
        + f'<section class="sect"><h2>{esc(CE["related_h"])}</h2><div class="chips">{rel}</div></section>'
        + f'<div class="closing"><p class="closing__h">{inline(d["close"][0])}</p><p>{inline(d["close"][1])}</p></div>'
        + leadform() + "</div>"
    )
    publish(path, d["title"], d["desc"], main,
            [crumbs_schema(trail), es_service_schema(name, path, d["desc"], county_area()), faq_schema(d["faqs"])],
            priority="0.7")


@spanish
def build_es_place(key):
    d = ES_ZONA[key]
    name = CAT.CITY_NAME[key]
    path = CAT.es_place_path(key)
    trail = [("/es/", CE["home_crumb"]), (path, name)]
    glance = "".join(f'<li><span class="glance__k">{inline(k)}</span><span class="glance__v">{inline(v)}</span></li>' for k, v in d["glance"])
    spots = "".join(f'<div class="spot">{icon("bee")}<p class="spot__h">{inline(h)}</p><p>{inline(t)}</p></div>' for h, t in d["hotspots"])
    streets = "".join(f'<li><p class="street__h">{inline(h)}</p><p>{inline(t)}</p></li>' for h, t in d["streets"])
    visit = "".join(f'<li><p class="step__h">{inline(h)}</p><p>{inline(t)}</p></li>' for h, t in d["visit"])
    svcs = "".join(f'<a class="card" href="{CAT.es_svc_path(sl)}"><span class="card__h">{esc(CAT.ES_SVC_NAME[sl])}</span>'
                   f'<span>{esc(plain(t))}</span></a>' for sl, t in d["servicios"] if sl in ES_SVC)
    near = "".join(f'<a class="chip" href="{CAT.es_place_path(k)}">{esc(CAT.CITY_NAME[k])}</a>' for k in d["cercanos"] if k in ES_ZONA)
    main = (
        hero(d["kicker"], d["h1"], d["lede"], trail)
        + f'<div class="wrap"><div class="pair">{quick_box(d["quick"])}{alarm_box(d["alarm"])}</div>'
        + f'<section class="glance" aria-label="{esc(CE["glance_label"])} {esc(name)}"><p class="label">{esc(CE["glance_label"])} {esc(name)}</p><ul>{glance}</ul></section>'
        + f'<section class="sect">{prose(d["opening"])}</section>'
        + f'<section class="sect"><h2>{inline(d["hotspots_h"])}</h2><div class="spots">{spots}</div></section></div>'
        + band(d["band"])
        + f'<div class="wrap"><section class="sect"><h2>{inline(d["streets_h"])}</h2><ul class="streets">{streets}</ul></section>'
        + "".join(section(h, t) for h, t in d["body"])
        + f'<section class="sect"><h2>{inline(d["visit_h"])}</h2><ol class="steps">{visit}</ol></section>'
        + f'<section class="sect"><h2>{esc(CE["fits_h"])}</h2><div class="cards">{svcs}</div></section>'
        + faq_block(d["faqs"], CE["faq_h"])
        + f'<section class="sect"><h2>{esc(CE["near_h"])}</h2><div class="chips">{near}'
          f'<a class="chip chip--all" href="/es/#zonas">{esc(CORE_ES["home"]["places_h"])}</a></div></section>'
        + f'<div class="closing"><p class="closing__h">{inline(d["close"][0])}</p><p>{inline(d["close"][1])}</p></div>'
        + leadform(place=name) + "</div>"
    )
    area = place_area(key)
    publish(path, d["title"], d["desc"], main,
            [crumbs_schema(trail), es_service_schema(f"Remoción de abejas en {name}", path, d["desc"], area), faq_schema(d["faqs"])],
            priority="0.8")


@spanish
def build_es_precios():
    P = CORE_ES["precios"]
    trail = [("/es/", CE["home_crumb"]), ("/es/precios/", CAT.ES_CORE["precios"][1])]
    tiers = "".join(f'<div class="tier"><p class="tier__fig">{esc(f)}</p><p class="tier__h">{esc(h)}</p>{prose(t)}</div>' for f, h, t in P["tiers"])
    drivers = "".join(f'<li><p class="street__h">{esc(h)}</p><p>{inline(t)}</p></li>' for h, t in P["drivers"])
    main = (hero(P["kicker"], P["h1"], P["lede"], trail) + f'<div class="wrap">{quick_box(P["quick"])}'
            + f'<section class="sect"><h2>{esc(P["tiers_h"])}</h2><div class="tiers">{tiers}</div></section>'
            + f'<section class="sect"><h2>{esc(P["drivers_h"])}</h2><ul class="streets">{drivers}</ul></section></div>'
            + band(P["band"]) + '<div class="wrap">' + "".join(section(h, t) for h, t in P["body"])
            + faq_block(P["faqs"], CE["faq_h"]) + leadform(P["form_h"]) + "</div>")
    publish("/es/precios/", P["title"], P["desc"], main,
            [crumbs_schema(trail), es_service_schema("Rangos de costo para sacar abejas", "/es/precios/", P["desc"], county_area()),
             faq_schema(P["faqs"])], priority="0.7")


@spanish
def build_es_solicitar():
    Q = CORE_ES["solicitar"]
    trail = [("/es/", CE["home_crumb"]), ("/es/solicitar/", CAT.ES_CORE["solicitar"][1])]
    ways = "".join(f'<li>{icon(ic)}<div><p class="street__h">{esc(h)}</p><p>{inline(t)}</p></div></li>' for ic, h, t in Q["ways"])
    main = (hero(Q["kicker"], Q["h1"], Q["lede"], trail) + f'<div class="wrap"><div class="pair">{quick_box(Q["quick"])}{alarm_box(Q["alarm"])}</div>'
            + leadform(Q["form_h"])
            + f'<section class="sect"><h2>{esc(Q["ways_h"])}</h2><ul class="commits">{ways}</ul></section>'
            + "".join(section(h, t) for h, t in Q["body"]) + "</div>")
    contact = {"@context": "https://schema.org", "@type": "ContactPage", "name": Q["h1"], "url": SITE + "/es/solicitar/",
               "inLanguage": "es", "about": {"@id": BUSINESS_ID}}
    publish("/es/solicitar/", Q["title"], Q["desc"], main, [crumbs_schema(trail), contact], priority="0.7")


# ---------------------------------------------------------------- sitemap, robots, llms, manifest
def build_meta_files():
    state_path = os.path.join(ROOT, ".lastmod.json")
    try:
        with open(state_path, encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        state = {}
    fresh = {}
    for path, _ in SITEMAP:
        digest = hashlib.sha256(MAINS[path].encode("utf-8")).hexdigest()[:16]
        prev = state.get(path)
        fresh[path] = prev if prev and prev.get("hash") == digest else {"hash": digest, "date": TODAY.isoformat()}
    with open(state_path, "w", encoding="utf-8") as fh:
        json.dump(fresh, fh, indent=1, sort_keys=True)
        fh.write("\n")
    rows = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{fresh[p]['date']}</lastmod><priority>{pr}</priority></url>\n"
                   for p, pr in SITEMAP)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + rows + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
    L = CORE["llms"]
    out = [f"# {BRAND}", "", f"> {L['summary']}", "", L["intro"], "", "## Contact", "",
           f"- Phone and text: {PHONE} (tel:{DIAL})", f"- Email: {EMAIL}", f"- {L['area']}", f"- {L['hours']}", "",
           "## What we offer", ""]
    out += [f"- {x}" for x in L["facts"]]
    out += ["", "## Removal pages", ""]
    out += [f"- [{n}]({SITE}{CAT.svc_path(s)}): {plain(SVC[s]['card'])}" for s, n, _ in CAT.SERVICES if s in SVC]
    out += ["", "## Place pages", ""]
    out += [f"- [{n}]({SITE}{CAT.city_path(k)}): {plain(CITY[k]['card'])}" for k, n, *_ in CAT.CITIES if k in CITY]
    out += ["", "## Field guide", ""]
    out += [f"- [{GUIDE[g]['h1']}]({SITE}{CAT.guide_path(g)}): {plain(GUIDE[g]['card'])}" for g, _ in CAT.GUIDES if g in GUIDE]
    LE = CORE_ES["llms"]
    out += ["", f"## {LE['heading']}", "", LE["intro"], ""]
    out += [f"- [{n}]({SITE}{p})" for p, n, _ in CAT.ES_CORE.values()]
    out += [f"- [{CAT.ES_SVC_NAME[x]}]({SITE}{CAT.es_svc_path(x)}): {plain(ES_SVC[x]['card'])}" for x, _, _ in CAT.ES_SERVICES if x in ES_SVC]
    out += [f"- [{CAT.CITY_NAME[k]}]({SITE}{CAT.es_place_path(k)}): {plain(ES_ZONA[k]['card'])}" for k in CAT.ES_PLACES if k in ES_ZONA]
    out += ["", "## Other pages", ""]
    out += [f"- [{n}]({SITE}{p})" for p, n in CAT.CORE_PAGES.values()]
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    manifest = {"name": BRAND, "short_name": "Bee Rescue", "start_url": "/", "display": "browser",
                "background_color": "#F7F3EA", "theme_color": "#1B1D21",
                "icons": [{"src": asset("mark-192.png"), "sizes": "192x192", "type": "image/png"},
                          {"src": asset("mark-512.png"), "sizes": "512x512", "type": "image/png"}]}
    with open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)


# ---------------------------------------------------------------- main
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    stage_assets()
    build_home()
    build_removal_hub()
    for s, _, _ in CAT.SERVICES:
        if s in SVC:
            build_service(s)
    if COUNTY:
        build_county()
    for k, *_ in CAT.CITIES:
        if k in CITY:
            build_city(k)
    build_guides_hub()
    for g, _ in CAT.GUIDES:
        if g in GUIDE:
            build_guide(g)
    build_cost()
    build_answers()
    build_who()
    build_request()
    build_es_home()
    for x, _, _ in CAT.ES_SERVICES:
        if x in ES_SVC:
            build_es_service(x)
    for k in CAT.ES_PLACES:
        if k in ES_ZONA:
            build_es_place(k)
    build_es_precios()
    build_es_solicitar()
    build_404()
    build_meta_files()
    missing = ([s for s, *_ in CAT.SERVICES if s not in SVC] + [k for k, *_ in CAT.CITIES if k not in CITY]
               + [g for g, _ in CAT.GUIDES if g not in GUIDE] + ([] if COUNTY else ["county"])
               + ["es/" + x for x, _, _ in CAT.ES_SERVICES if x not in ES_SVC] + ["es/" + k for k in CAT.ES_PLACES if k not in ES_ZONA])
    print(f"{len(SITEMAP)} indexed pages + 404 written to public/")
    if missing:
        print(f"{len(missing)} module(s) not written yet: {', '.join(missing)}")
    if PROBLEMS:
        print(f"{len(PROBLEMS)} problem(s):")
        for p in PROBLEMS:
            print("  -", p)
        sys.exit(1)


if __name__ == "__main__":
    main()
