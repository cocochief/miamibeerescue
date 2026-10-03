# -*- coding: utf-8 -*-
"""Every page on miamibeerescue.com, listed once.

Copy modules never write raw URLs. They link with tokens that build.py
resolves against this catalog, so a mistyped slug stops the build:

    [[city:coral-gables|Coral Gables]]     place pages
    [[svc:walls|hives inside a wall]]      removal pages
    [[guide:scout-bees|scout bees]]        field guide articles
    [[page:cost|what removal costs]]       core pages (keys in CORE_PAGES)

Address scheme
    /miami-dade/                 county hub
    /miami-dade/<place>/         one page per city, town, village or area
    /removal/  /removal/<what>/  removal hub and removal pages
    /field-guide/  /field-guide/<topic>/
    /cost/  /answers/  /who-we-are/  /request-removal/
"""

# (slug, label, group)
SERVICES = [
    ("emergency",         "24-Hour Emergency Bee Removal",       "now"),
    ("swarms",            "Swarm Pickup & Removal",              "now"),
    ("walls",             "Bees in Block & Frame Walls",         "inside"),
    ("roofs",             "Tile & Flat Roof Hives",              "inside"),
    ("soffits-eaves",     "Soffit, Fascia & Eave Hives",         "inside"),
    ("utility-boxes",     "Meter, Valve & Irrigation Boxes",     "inside"),
    ("trees-palms",       "Palm & Tree Colonies",                "outside"),
    ("sheds-garages",     "Sheds, Garages & Outbuildings",       "outside"),
    ("nurseries-groves",  "Nurseries, Groves & Farms",           "outside"),
    ("condos-high-rises", "Condo & High-Rise Buildings",         "building"),
    ("hoa-commercial",    "HOA, Commercial & Property Managers", "building"),
    ("waterfront-boats",  "Docks, Seawalls & Boats",             "building"),
    ("pool-enclosures",   "Pool Enclosures & Equipment",         "building"),
    ("live-honey-bees",   "Live Honey Bee Removal",              "method"),
    ("beehives",          "Humane Beehive Removal",              "method"),
    ("relocation",        "Colony Relocation to Beekeepers",     "method"),
    ("honeycomb-cleanup", "Comb & Honey Cleanup",                "method"),
    ("repairs",           "Repairs After Removal",               "method"),
]

SERVICE_GROUPS = [
    ("now",      "Bees that need handling now"),
    ("inside",   "Inside the structure"),
    ("outside",  "Yards, trees and land"),
    ("building", "By type of property"),
    ("method",   "How the colony is handled"),
]

# (key, name, kind, region, tier)
#   kind: city | town | village | unincorporated | neighborhood | area
#   tier: primary (deepest pages) | estate | local
CITIES = [
    ("miami",             "Miami",             "city",           "core",    "primary"),
    ("coral-gables",      "Coral Gables",      "city",           "core",    "primary"),
    ("coconut-grove",     "Coconut Grove",     "neighborhood",   "core",    "estate"),
    ("south-miami",       "South Miami",       "city",           "core",    "local"),
    ("westchester",       "Westchester",       "unincorporated", "core",    "local"),
    ("miami-beach",       "Miami Beach",       "city",           "beaches", "estate"),
    ("key-biscayne",      "Key Biscayne",      "village",        "beaches", "estate"),
    ("fisher-island",     "Fisher Island",     "unincorporated", "beaches", "estate"),
    ("bal-harbour",       "Bal Harbour",       "village",        "beaches", "estate"),
    ("surfside",          "Surfside",          "town",           "beaches", "local"),
    ("bay-harbor-islands", "Bay Harbor Islands", "town",         "beaches", "local"),
    ("golden-beach",      "Golden Beach",      "town",           "north",   "estate"),
    ("miami-shores",      "Miami Shores",      "village",        "north",   "estate"),
    ("aventura",          "Aventura",          "city",           "north",   "local"),
    ("sunny-isles-beach", "Sunny Isles Beach", "city",           "north",   "local"),
    ("north-miami",       "North Miami",       "city",           "north",   "local"),
    ("north-miami-beach", "North Miami Beach", "city",           "north",   "local"),
    ("miami-gardens",     "Miami Gardens",     "city",           "north",   "local"),
    ("hialeah",           "Hialeah",           "city",           "west",    "local"),
    ("hialeah-gardens",   "Hialeah Gardens",   "city",           "west",    "local"),
    ("miami-lakes",       "Miami Lakes",       "town",           "west",    "local"),
    ("miami-springs",     "Miami Springs",     "city",           "west",    "local"),
    ("doral",             "Doral",             "city",           "west",    "local"),
    ("west-kendall",      "West Kendall",      "area",           "west",    "local"),
    ("pinecrest",         "Pinecrest",         "village",        "south",   "estate"),
    ("palmetto-bay",      "Palmetto Bay",      "village",        "south",   "estate"),
    ("kendall",           "Kendall",           "unincorporated", "south",   "local"),
    ("cutler-bay",        "Cutler Bay",        "town",           "south",   "local"),
    ("homestead",         "Homestead",         "city",           "south",   "local"),
    ("florida-city",      "Florida City",      "city",           "south",   "local"),
    ("redland",           "Redland",           "area",           "south",   "local"),
]

# (id, label) in display order
REGIONS = [
    ("core",    "Miami, the Grove and the Gables"),
    ("beaches", "The beaches and the islands"),
    ("north",   "North Dade"),
    ("west",    "Hialeah, Doral and the west side"),
    ("south",   "Kendall and South Dade"),
]

# Places we serve that have no page of their own, by region.
OTHER_PLACES = {
    "core":    ["West Miami", "Coral Terrace", "Glenvar Heights", "Brownsville", "Gladeview"],
    "beaches": ["North Bay Village", "Indian Creek"],
    "north":   ["Biscayne Park", "El Portal", "Opa-locka", "Golden Glades", "Ojus", "Ives Estates",
                "Westview", "West Little River", "Pinewood"],
    "west":    ["Medley", "Virginia Gardens", "Sweetwater", "Fontainebleau", "Tamiami", "University Park",
                "Olympia Heights", "Westwood Lakes", "Kendale Lakes", "The Hammocks", "Kendall West",
                "The Crossings", "Country Walk", "Three Lakes", "Country Club"],
    "south":   ["Richmond Heights", "Palmetto Estates", "South Miami Heights", "Goulds", "Princeton",
                "Naranja", "Leisure City", "Sunset"],
}

PRIMARY_CITIES = [k for k, _, _, _, t in CITIES if t == "primary"]

# (slug, label)
GUIDES = [
    ("scout-bees",            "Scout bees checking out the house"),
    ("second-home",           "Bees at a seasonal home while you are away"),
    ("renters-and-landlords", "Renting with bees: tenant or landlord?"),
    ("home-sale-inspection",  "Bees found during a home sale or inspection"),
    ("after-a-storm",         "Bee colonies exposed after a storm"),
    ("thermal-imaging",       "What thermal imaging shows about a hive"),
    ("why-bees-come-back",    "Repeat colonies in a sealed gap"),
]

# id -> (path, label)
CORE_PAGES = {
    "home":    ("/",                 "Home"),
    "county":  ("/miami-dade/",      "Areas we serve"),
    "removal": ("/removal/",         "Removal services"),
    "guides":  ("/field-guide/",     "Field guide"),
    "cost":    ("/cost/",            "Cost"),
    "answers": ("/answers/",         "Answers"),
    "who":     ("/who-we-are/",      "Who we are"),
    "quote":   ("/request-removal/", "Request removal"),
}

SVC_NAME = {s: n for s, n, _ in SERVICES}
SVC_GROUP = {s: g for s, _, g in SERVICES}
CITY_NAME = {k: n for k, n, _, _, _ in CITIES}
CITY_KIND = {k: c for k, _, c, _, _ in CITIES}
CITY_REGION = {k: r for k, _, _, r, _ in CITIES}
CITY_TIER = {k: t for k, _, _, _, t in CITIES}
GUIDE_NAME = dict(GUIDES)
REGION_NAME = dict(REGIONS)


def city_path(key):
    return f"/miami-dade/{key}/"


def svc_path(slug):
    return f"/removal/{slug}/"


def guide_path(slug):
    return f"/field-guide/{slug}/"


def resolve(kind, ref):
    """Return (path, default label) for a link token, or raise KeyError."""
    if kind == "city":
        return city_path(ref), CITY_NAME[ref]
    if kind == "svc":
        return svc_path(ref), SVC_NAME[ref]
    if kind == "guide":
        return guide_path(ref), GUIDE_NAME[ref]
    if kind == "page":
        return CORE_PAGES[ref]
    if kind == "es":
        return es_resolve(ref)
    raise KeyError(kind)


# ---------------------------------------------------------------- Spanish section (/es/)
# Written fresh in Spanish, not translated. Each page names the English page
# that covers the same topic, for hreflang. Spanish copy links only to other
# Spanish pages, with tokens like [[es:svc-enjambres|enjambres]].
#
#   /es/                         inicio
#   /es/servicios/<slug>/        removal pages
#   /es/zonas/<key>/             place pages (same keys as CITIES)
#   /es/precios/  /es/solicitar/

# (slug, label, English service slug)
ES_SERVICES = [
    ("emergencias",          "Emergencias con abejas 24 horas",  "emergency"),
    ("enjambres",            "Enjambres de abejas",              "swarms"),
    ("abejas-en-paredes",    "Abejas dentro de paredes",         "walls"),
    ("abejas-en-techos",     "Abejas en techos y tejas",         "roofs"),
    ("panales-y-colmenas",   "Quitar panales y colmenas",        "beehives"),
    ("remocion-sin-matarlas", "Remoción de abejas sin matarlas", "live-honey-bees"),
    ("contador-de-agua",     "Abejas en el contador de agua",    "utility-boxes"),
]

# place keys (must exist in CITIES)
ES_PLACES = ["miami", "hialeah", "hialeah-gardens", "doral", "kendall", "west-kendall", "westchester", "homestead"]

# id -> (path, label, English path for hreflang)
ES_CORE = {
    "inicio":    ("/es/",           "Inicio",            "/"),
    "precios":   ("/es/precios/",   "Precios",           "/cost/"),
    "solicitar": ("/es/solicitar/", "Solicitar servicio", "/request-removal/"),
}

ES_SVC_NAME = {s: n for s, n, _ in ES_SERVICES}
ES_SVC_EN = {s: e for s, _, e in ES_SERVICES}


def es_svc_path(slug):
    return f"/es/servicios/{slug}/"


def es_place_path(key):
    return f"/es/zonas/{key}/"


def es_resolve(ref):
    """[[es:<ref>|label]] where ref is inicio | precios | solicitar | svc-<slug> | zona-<key>."""
    if ref in ES_CORE:
        return ES_CORE[ref][:2]
    if ref.startswith("svc-") and ref[4:] in ES_SVC_NAME:
        return es_svc_path(ref[4:]), ES_SVC_NAME[ref[4:]]
    if ref.startswith("zona-") and ref[5:] in ES_PLACES:
        return es_place_path(ref[5:]), CITY_NAME[ref[5:]]
    raise KeyError(ref)


def hreflang_pairs():
    """English path -> Spanish path for every page that has both."""
    pairs = {en: path for path, _, en in ES_CORE.values()}
    pairs.update({svc_path(e): es_svc_path(s) for s, _, e in ES_SERVICES})
    pairs.update({city_path(k): es_place_path(k) for k in ES_PLACES})
    return pairs
