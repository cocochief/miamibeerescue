# Launch checklist: miamibeerescue.com

Work through this top to bottom before telling anyone the site is live.
Everything the code needs is already in the repo; what is left are
account settings only you can change.

## 1. GitHub

- [ ] In the repo settings, make `claude/awesome-ritchie-k60o5c` the default
      branch (the repo has no `main`). If you later rename or merge into a
      different branch, change `branch:` in `.do/app.yaml` to match.

## 2. DigitalOcean App Platform

- [ ] Create the app from this repo (Apps > Create App > GitHub >
      `cocochief/miamibeerescue`), or upload `.do/app.yaml` as the app spec.
      It is a single Node service: build `npm ci --omit=dev`, run
      `node server.js`, port 8080, health check `/healthz`.
- [ ] Under the `web` component > Environment Variables, add and tick
      **Encrypt** for each:
  - `GMAIL_USER`: the Gmail address that sends lead emails
  - `GMAIL_APP_PASSWORD`: a 16-character App Password for that account
    (Google Account > Security > 2-Step Verification must be on > App passwords)
  - `LEAD_NOTIFY_EMAIL` is already set to `removal@miamibeerescue.com` in the
    spec; change it only if leads should go elsewhere.
- [ ] Do not set `MAIL_DRY_RUN` in production (it stops real sending).
- [ ] After the deploy, open `https://<app-url>/healthz`. It should show
      `"mail":"gmail"`. `"not configured"` means a Gmail variable is missing.
- [ ] Send one test lead through the form and one with "Emergency: someone
      is being stung now". Check that both arrive at removal@miamibeerescue.com
      with these subjects:
  - `New Miami Bee Rescue Lead: <name> (<city>)`
  - `[EMERGENCY] New Miami Bee Rescue Lead: <name> (<city>)`

  Delete the test entries from your inbox afterward.

## 3. Domain and DNS

- [ ] In the app's Settings > Domains, add `miamibeerescue.com` (primary) and
      `www.miamibeerescue.com` (alias). Both are already listed in the spec.
- [ ] At your registrar, either point the nameservers to DigitalOcean or add
      the records DigitalOcean shows (an `A`/`ALIAS` for the root, a `CNAME`
      for `www`).
- [ ] Wait for the certificate to show "Active", then check that:
  - `https://miamibeerescue.com` loads
  - `https://www.miamibeerescue.com/cost/` redirects (301) to `https://miamibeerescue.com/cost/`
- [ ] Set up the `removal@miamibeerescue.com` mailbox (Google Workspace or your
      email host) and add its MX, SPF and DKIM records, so lead emails and
      replies don't land in spam.

## 4. Phone and texting

- [ ] Call (786) 442-2496 from a mobile phone and confirm it rings through at
      night and on weekends. Every page promises phones answered 24/7.
- [ ] Text a photo to (786) 442-2496 and confirm it arrives. Every page has
      "Text a Photo" buttons. If the number is a landline or a VoIP line
      without MMS, turn on texting with the carrier first, or the buttons will fail.
- [ ] Use this number only for this brand, so calls can be tracked and
      the Google listing stays consistent.

## 5. Google Search Console

- [ ] Add a **Domain** property for `miamibeerescue.com` and verify it with the
      DNS TXT record Google gives you.
- [ ] Submit `https://miamibeerescue.com/sitemap.xml`.
- [ ] Use URL Inspection on the homepage, `/miami-dade/miami/` and
      `/miami-dade/coral-gables/` and request indexing.
- [ ] Optional: create a GA4 property and paste its measurement ID into
      `GTAG_ID` in `build.py`, then run `python3 build.py` and commit. Call taps,
      text taps and form leads are already sent as events (`call_tap`,
      `text_tap`, `generate_lead`) once the tag is present.

## 6. Google Business Profile (new, separate)

- [ ] Create a **new** profile for Miami Bee Rescue. Don't add it to an
      existing profile or business group, and don't reuse photos, descriptions
      or categories copied from another listing.
- [ ] Choose **service-area business** and **hide the address**. The site has
      no street address anywhere and the schema has none, so keep it that way.
- [ ] Service areas: Miami-Dade County and the main places (Miami, Coral Gables,
      Miami Beach, Hialeah, Kendall, Doral, Homestead, Pinecrest, Key Biscayne,
      Aventura and others). Don't add places outside the county.
- [ ] Primary category: Pest control service (or the closest bee removal
      category offered); add Wildlife and animal control service only if it fits.
- [ ] Hours: open 24 hours, matching "phones answered 24/7".
- [ ] Phone (786) 442-2496, website `https://miamibeerescue.com`.
- [ ] Write the description fresh. Don't paste text from this website or from
      any other listing.
- [ ] Once the profile is verified, paste its URL into
      `SOCIAL["google"]` in `build.py`, rebuild and commit, so it appears in
      the business schema's `sameAs`. Do the same for any Facebook, Instagram,
      Nextdoor or Yelp pages you create for this brand.

## 7. Photos

The site ships with no photographs. The logo and share image (`assets/og.jpg`)
are drawn from shapes by `tools/brand_images.py`.

- [ ] Take your own photos on Miami-Dade jobs: comb in a wall cavity, a
      swarm cluster, the thermal camera view, a finished repair. Never use
      stock photos or photos from another business or website.
- [ ] Remove location data (EXIF GPS) before using them. `tools/prep_photos.py`
      resizes, strips metadata and writes web-ready copies.
- [ ] Ask homeowners before photographing anything that shows a house number,
      a face or a car plate.
- [ ] Add the best ones to the Google Business Profile as they come in.

## 8. Final checks after go-live

- [ ] Open the site on a phone. The Call / Text / Quote bar sits at the
      bottom of every page; tap each one.
- [ ] Turn off Wi-Fi and data briefly and submit the form. The page should
      offer call, text and a pre-filled email instead of losing the request.
- [ ] Check `https://miamibeerescue.com/robots.txt`, `/sitemap.xml` and `/llms.txt`.
- [ ] Run the Rich Results Test on the homepage, a place page, a removal page
      and a field guide article (LocalBusiness, Service, FAQPage, Article,
      BreadcrumbList should all show without errors).

## Editing the site later

- Copy lives in `content/` (one module per page; `content/core.py` for the
  homepage, hubs and shared text). Links between pages use tokens like
  `[[city:doral|Doral]]`, so a typo stops the build instead of shipping a dead link.
- Run `python3 build.py`, check the output, and commit both the source and the
  regenerated `public/` folder. DigitalOcean serves `public/` as committed.
- Don't commit `leads.log`, `.env` or `__pycache__/` (they are git-ignored).
- Business claims are deliberately narrow: live removal only, licensed and
  insured, 24/7 answering with a 24-hour response guarantee, our own repair
  crews, thermal imaging, warrantied workmanship, free quotes, higher
  night/weekend rates, photos and invoices on request, and the $300–$400 /
  "into the thousands" price ranges. Don't add reviews, ratings, years in
  business, certifications or other prices unless they are true and you
  decide to.
