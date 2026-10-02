# -*- coding: utf-8 -*-
"""Copy for the homepage, hub pages, cost, answers, about, request and 404
pages, plus the shared page chrome, form text and llms.txt."""

CORE = {
    "schema_description": (
        "Removes wild honey bee colonies alive from houses, condo towers, HOA grounds, farms and shops throughout Miami-Dade County. "
        "Colonies are taken out alive and handed to beekeepers. The phone line never closes, "
        "and a reply reaches every caller inside of 24 hours."
    ),

    # ------------------------------------------------------------ chrome
    "chrome": {
        "call": "Call",
        "text": "Text a Photo",
        "quote": "Free Quote",
        "quick_label": "Quick answer",
        "alarm_title": "If anyone is being stung",
        "skip": "Jump to the page content",
        "topline": "The line is staffed every hour of every day, with a response guaranteed inside 24 hours",
        "menu": "Open the menu",
        "og_alt": "Miami Bee Rescue logo: a bee under a gold Art Deco arch",
        "dock_label": "Contact shortcuts",
        "dock_text": "Text",
        "dock_quote": "Quote",
        "behind_h": "What is going on behind it",
        "putback_h": "What we put back afterward",
        "cost_h": "What moves the price on this job",
        "cost_more": "How pricing works overall",
        "faq_h": "Questions people ask us",
        "related_h": "Related removal work",
        "kinds": {"city": "City", "town": "Town", "village": "Village", "unincorporated": "Unincorporated area",
                  "neighborhood": "City of Miami neighborhood", "area": "Area"},
        "also_served": "Also covered here:",
        "jump_label": "Sections on this page",
        "glance_label": "Around",
        "fits_h": "Removal work that comes up in",
        "near_h": "Places next door",
        "updated": "Updated",
        "toc": "In this article",
        "guide_svcs_h": "Removal pages that go with this article",
        "guide_places_h": "Where in Miami-Dade this comes up",
        "footer": {
            "about": ("Honey bee colonies taken out alive from houses, towers, yards and farmland, then rehomed with "
                      "beekeepers. We carry a license and insurance, and a COI can be issued to any board or company that asks."),
            "area": ("Miami-Dade County only, from the beaches to the farm roads of the Redland and up to the county line. "
                     "No storefront: we come to you."),
            "h_removal": "Removal",
            "h_places": "Places",
            "h_company": "Company",
            "fine": "Colonies are never exterminated. Prices quoted before work begins.",
        },
    },

    # ------------------------------------------------------------ form
    "form": {
        "heading": "Tell us where the bees are",
        "intro": ("Three fields are enough to start: your name, a number we can reach, and the city or neighborhood. "
                  "Anything else you add saves a question on the callback."),
        "text_line": "Prefer texting? Send a picture",
        "hours_line": "Someone picks up day and night",
        "labels": {"name": "Your name", "phone": "Best phone number", "location": "City or neighborhood",
                   "email": "Email", "spot": "Where you see them", "urgency": "How urgent is it",
                   "notes": "Anything we should know"},
        "placeholders": {"name": "First and last", "phone": "So we can call you back",
                         "location": "For example: Kendall, Brickell, Homestead",
                         "email": "For a written quote", "notes": "Gate code, floor number, pets, allergies, how long they have been there"},
        "optional": "(optional)",
        "choose": "Pick the closest match",
        "spot_options": ["Wall or stucco", "Roof tile or attic", "Soffit or eave", "Palm or other tree",
                         "Meter, valve or irrigation box", "Shed, garage or outbuilding", "Pool enclosure or pool equipment",
                         "Balcony, planter or condo common area", "Dock, seawall or boat", "Nursery, grove or farm building",
                         "A swarm hanging in the open", "Not sure yet"],
        "urgency_options": [("Planning ahead", "No rush, I am planning ahead"),
                            ("This week", "Soon, ideally this week"),
                            ("Bees getting inside", "Bees are getting into the living space"),
                            ("Emergency: stinging now", "Emergency: someone is being stung now")],
        "submit": "Send my request",
        "fine": ("We only use these details to reply about your bees. Nobody is put on a mailing list. "
                 "For a medical emergency from a sting, call 911 first."),
    },

    # ------------------------------------------------------------ home
    "home": {
        "title": "Live Bee Removal in Miami-Dade, Phones Open 24/7",
        "desc": ("Honey bees in a wall, roof, palm or meter box anywhere in Miami-Dade? We take colonies out alive, "
                 "rehome them with beekeepers and repair the spot."),
        "kicker": "Miami-Dade honey bee removal",
        "h1": "Live Bee Removal Across Miami-Dade County",
        "lede": ("Comb behind stucco, under roof tile or down inside a palm? Reach us whichever way is easiest. "
                 "Every colony we take out ends up with a beekeeper instead of a can of poison."),
        "trust": [("clock", "Calls answered around the clock; a 24-hour response guarantee"),
                  ("bee", "Never exterminated: colonies go to beekeepers"),
                  ("shield", "Licensed and insured, COIs on request"),
                  ("home", "Our own contractors close up and repair")],
        "quick": ("Honey bees that have settled inside a building rarely leave by themselves, and spraying them usually "
                  "leaves rotting comb behind. The fix is to open the spot, lift the colony out comb and all, "
                  "move the colony to a beekeeper, and seal the gap. Plan on roughly $300 to $400 when the bees sit low and shallow. "
                  "Work high up or behind finishes that need rebuilding costs more."),
        "triage_h": "What are you looking at right now?",
        "triage_sub": "Pick the closest match. Each one goes to the page that explains what happens next.",
        "triage": [
            {"tone": "red", "href": "/removal/emergency/", "icon": "alert", "head": "Someone is getting stung",
             "text": "Get people and pets indoors and shut the windows, then phone. Active stings jump ahead of every other job.",
             "go": "Emergency steps"},
            {"tone": "gold", "href": "/removal/swarms/", "icon": "bee", "head": "A clump of bees is hanging off something",
             "text": "Hanging from a branch, fence, mailbox or car bumper, with no comb in sight. Those bees are between homes.",
             "go": "About swarms"},
            {"tone": "ink", "href": "/removal/walls/", "icon": "home", "head": "Bees keep flying into one gap in the house",
             "text": "Traffic streaming through one crack, vent or tile edge all day says comb is being built behind it.",
             "go": "Hives in walls"},
            {"tone": "sand", "href": "/request-removal/", "icon": "chat", "head": "I honestly can't tell",
             "text": "Text us a photo from a safe distance. A picture of the entrance usually answers it.",
             "go": "Send a photo"},
        ],
        "map_h": "Six doorways bees use on a typical Miami-Dade home",
        "map_sub": ("Bees want a dry, dark cavity with a small doorway. Florida homes offer plenty of them. Tap a number "
                    "to see how that spot gets opened, cleared and closed."),
        "map_alt": "Drawing of a stucco house with a tile roof, a palm, a meter box and a pool cage, numbered where bees nest",
        "map_notes": {
            "roofs": "Gaps under barrel and flat tile lead to the deck and attic.",
            "soffits-eaves": "Vented panels and loose fascia corners.",
            "walls": "Hollow block cells and frame wall bays behind the stucco.",
            "utility-boxes": "Water meter, valve and irrigation boxes at ground level.",
            "trees-palms": "Hollow trunks and the boots left where fronds were cut.",
            "pool-enclosures": "Hollow aluminum framing and pump or heater housings.",
        },
        "steps_h": "How a removal goes, start to finish",
        "steps": [
            ("You reach us", "Call or text any hour. Mention how long you have noticed them, and send a picture of the hole they use if you can."),
            ("We look before we cut", "On site, a thermal camera and a few taps on the surface show where the comb sits, so the opening stays as small as it can be."),
            ("The colony comes out alive", "Bees, brood and comb are lifted out by hand and boxed. Nothing gets sprayed into the cavity."),
            ("The cavity is cleaned and sealed", "Leftover honey and wax are scraped out so nothing ferments or draws the next swarm, then the entry is closed."),
            ("Repairs, if you want them", "Our own licensed contractors, roofers and painters patch stucco, reset tile and touch up paint."),
        ],
        "price_kicker": "Straight numbers",
        "price_h": "What most people end up paying",
        "price": ("Jobs you can reach from the ground, with the colony close to the surface, usually come to about $300 to "
                  "$400. Colonies high on a roof, deep in a ceiling or spread through several wall bays take longer and "
                  "often need rebuilding, so those climb into the thousands. You pay nothing for the quote, which comes before "
                  "anything is opened.\n\nEmergency trips at night and over the weekend carry a higher rate than weekday appointments. For your files, "
                  "ask and we will send photos of the work and an itemized invoice."),
        "price_more": "Read the full cost breakdown",
        "fig_low": "typical ground-level job",
        "fig_high_b": "Into the thousands",
        "fig_high": "high, hidden or repair-heavy jobs",
        "props_h": "Not just houses",
        "props_sub": "Some buildings come with paperwork, boards, gate guards or farm schedules. These pages cover how each one runs.",
        "properties": [
            ("condos-high-rises", "tower", "Condo and high-rise buildings", "Balconies, planters, garages and roof equipment, with insurance certificates for the board."),
            ("hoa-commercial", "shield", "HOAs and businesses", "Common areas, storefronts, schools and warehouses, scheduled around your hours."),
            ("waterfront-boats", "boat", "Docks, seawalls and boats", "Stored boats, lift canopies, dock boxes and voids along the seawall."),
            ("nurseries-groves", "leaf", "Nurseries, groves and farms", "Shade houses, pump houses and packing sheds across South Dade farmland."),
        ],
        "regions_h": "Places we cover in Miami-Dade",
        "regions_sub": "Each place page covers its own buildings, trees and access quirks. The county page lists the rest of the places we serve.",
        "regions_more": "See every area in the county",
        "guides_h": "From the field guide",
        "guides_more": "All field guide articles",
        "faqs_h": "Before you call",
        "faqs": [
            ("If I leave them alone, do the bees eventually move out?",
             "A swarm hanging in the open usually moves on within a day or so once its scouts pick a new home. "
             "A colony that is already building comb inside a wall or roof is staying. It will keep growing until "
             "someone takes the comb out."),
            ("Can I spray them and be done with it?",
             "Spraying kills the bees you can see but leaves the comb, the honey and the dead brood inside the "
             "cavity. That mess can ferment, stain, attract other pests and pull in a new swarm. Live removal lifts out "
             "the wax and honey along with the bees."),
            ("Do you kill the bees?",
             "No. Extermination is not something we sell. The comb, brood and adult bees go into a box together and end up in a beekeeper's yard."),
            ("Do I have to be home?",
             "Not always. For a swarm outside or a box in the yard, a gate code and a phone call are often enough. For "
             "work that opens a wall or a ceiling, someone needs to let us in and sign off on the plan."),
        ],
        "form_h": "Get a free quote for your bees",
    },

    # ------------------------------------------------------------ removal hub
    "removal_hub": {
        "title": "Bee & Hive Removal Services Across Miami-Dade",
        "desc": ("Every kind of honey bee job we take on in Miami-Dade: swarms, walls, tile roofs, palms, meter boxes, "
                 "condos, docks and farms. Bees always leave alive."),
        "kicker": "Removal services",
        "h1": "Bee and Hive Removal Services in Miami-Dade",
        "lede": ("Pick the page that matches where your bees are or what kind of property you have. Each one explains how "
                 "that job is opened, cleared and closed."),
        "quick": ("Every job on this list ends the same way: the colony leaves alive for a beekeeper and the gap gets "
                  "sealed. What changes is the access. A swarm on a branch is a short job, while comb behind "
                  "stucco or under roof tile means opening the surface and rebuilding it. If you are not sure which page "
                  "fits, a photo by text settles it."),
        "groups": {
            "now": "When bees are stinging, swarming or pouring through a gap, this is where to start.",
            "inside": "Colonies that have moved into the building itself, which is most of what we open up.",
            "outside": "Trees, outbuildings and working land, where the job is more about reach than repairs.",
            "building": "Buildings where boards, managers, guards or dock rules shape how the visit runs.",
            "method": "How the colony is handled from first cut to the beekeeper's yard, and what is left to fix.",
        },
        "band": ("Not sure which of these you have?", "Send a photo of the entrance from a safe distance. Most jobs can be sorted out from one clear picture."),
        "after_h": "Why the cleanup matters as much as the bees",
        "after": ("Boxing up the bees is the first half of the work. Comb that stays in a wall keeps smelling like a home to the "
                  "bees that come scouting next, and honey left behind in the summer heat goes sour and seeps through drywall and paint. "
                  "That is why every removal here includes scraping the cavity and closing the entrance, and why "
                  "[[svc:repairs|repairs after removal]] and [[svc:honeycomb-cleanup|honey and wax cleanup]] each get their own "
                  "pages.\n\nOur workmanship carries a warranty with one plain promise behind it. It covers the work "
                  "on the opening we closed: should a new colony try that same gap, our crew returns to deal with it."),
    },

    # ------------------------------------------------------------ field guide hub
    "guides_hub": {
        "title": "Field Guide: Honey Bee Problems in Miami-Dade",
        "desc": ("Short, practical articles for Miami-Dade owners and renters: scout bees, storms, home sales, landlords, "
                 "thermal cameras, seasonal homes and repeat swarms."),
        "kicker": "Field guide",
        "h1": "A Field Guide to Honey Bee Problems in Miami-Dade",
        "lede": ("The questions that come up between spotting bees and booking a removal, answered for the way buildings "
                 "and leases work in this county."),
        "quick": ("These articles cover the situations that are not plain removals: a handful of bees inspecting the "
                  "eaves, a colony uncovered by storm damage, bees turning up during a home sale, a rental where nobody "
                  "is sure who pays, and a seasonal home left empty for months. Each one ends with what to do next."),
        "list_h": "Articles",
        "read": "Read it",
        "note_h": "When reading is not enough",
        "note": ("If bees are coming inside, stinging, or building comb you can see, skip the reading and reach out. "
                 "A quick look at a photo tells us more than any article can, and the quote costs nothing."),
    },

    # ------------------------------------------------------------ cost
    "cost": {
        "title": "Bee Removal Cost in Miami-Dade: How Quotes Work",
        "desc": ("Most ground-level bee removals in Miami-Dade run about $300 to $400. See what pushes a job higher, when "
                 "repairs add cost, and how quotes work."),
        "kicker": "Pricing",
        "h1": "What Bee Removal Costs in Miami-Dade",
        "lede": ("Two numbers cover most calls. The rest depends on how high the bees are, how much comb they built, and "
                 "what has to be rebuilt afterward."),
        "quick": ("When the colony is reachable from the ground and sits close to the surface, expect roughly $300 to $400. "
                  "Once the work involves a roof, a high soffit, a ceiling or several wall bays, plus repairs, the total "
                  "can climb into the thousands. Quotes are free and given before anything is cut. If you need us "
                  "overnight or on a weekend, the bill runs higher than a weekday visit would."),
        "tiers_h": "The ranges",
        "tiers": [
            ("$300–$400", "Ground-level, near the surface",
             "A meter box, a low section of wall, a shed corner or a swarm on a shrub. One visit, a small opening, and the "
             "entry sealed when the colony is out."),
            ("Into the thousands", "High, deep or spread out, with rebuilding",
             "Comb under roof tile, above a ceiling, high in a soffit or spread through several cavities. These need lifts "
             "or roof work, more hours inside the cavity, and finish work to put the surface back."),
            ("Free", "The quote itself",
             "Photos by text often get you a working range the same conversation. A firm number follows once we have "
             "looked at the spot."),
            ("Higher after hours", "Nights and weekends",
             "Emergency calls outside weekday hours are priced above a regular weekday visit. If the bees are not "
             "threatening anyone, waiting for a weekday keeps the bill down."),
        ],
        "drivers_h": "What decides where your job lands",
        "drivers": [
            ("Height and reach", "Anything above a single ladder means more setup, more safety gear and sometimes a lift."),
            ("How long the bees have been there", "A colony that moved in last week has a little comb. One that has been "
             "there all season may fill a cavity from top to bottom."),
            ("What covers the comb", "Drywall and vinyl soffit open easily. Stucco over block, roof tile and finished "
             "ceilings take more care to open and to rebuild."),
            ("Repairs you want us to handle", "Our licensed contractors, roofers and painters can close everything up, "
             "which adds to the bill but saves hiring a second crew."),
            ("Access and paperwork", "Guard gates, condo boards, elevator bookings and certificates of insurance take time "
             "to arrange, which matters for some buildings."),
        ],
        "band": ("Want a number before you decide?", "Text a few photos of the entrance and the wall or roof around it. We will tell you which range you are likely in."),
        "body": [
            ("Why spraying ends up the expensive option",
             "Spraying a colony inside a wall can look like the low-cost option, but it leaves pounds of comb and honey in "
             "the cavity. In Miami's heat that honey ferments, stains through paint and drywall, and draws ants, roaches "
             "and wax moths. The scent of old comb also makes the same spot attractive to the next swarm. Paying once "
             "to remove everything is usually cheaper than paying twice.\n\nIt is also why we never quote a removal "
             "that leaves comb behind. If we open it, we clear it."),
            ("What you get in writing",
             "You get a quote before work starts, so you can say yes or no to it. If you need records for an "
             "association, a landlord, a buyer or your own files, ask and we will send photos of the job and an "
             "itemized invoice showing the removal, the cleanup and any repair work as separate lines."),
            ("Repairs: our crews or yours",
             "Some owners want everything handled at once. Others already have a contractor or a painter they trust. "
             "Either works. We can seal the entry and leave the finish work to your people, or our own licensed "
             "contractors, roofers and painters can rebuild and match the surface. The quote spells out which way you "
             "chose."),
        ],
        "faqs": [
            ("Is there a charge just to come out and look?",
             "The quote is free. Photos by text often give you a range without a visit at all, and a firm number comes "
             "after we see the spot."),
            ("Why do nights and weekends cost more?",
             "Crews called out after hours are paid more to drop everything and go. That cost is built into after-hours "
             "pricing. If nobody is in danger, a weekday visit costs less."),
            ("Does the price include sealing the hole?",
             "Yes. Closing the entrance the bees used is part of every removal, because an open gap invites the next "
             "colony. Rebuilding a finish surface, such as stucco texture, tile or paint, is quoted on its own line."),
            ("What if the bees come back after I pay?",
             "Call the same number. A colony reappearing at an entry our crew closed is covered by the workmanship warranty, so we return and handle it."),
            ("Can I get a written breakdown for my HOA or landlord?",
             "Yes. Request them when you book. Job photos and a line-by-line invoice go out once the work wraps up."),
        ],
        "form_h": "Ask for your free quote",
    },

    # ------------------------------------------------------------ answers
    "answers": {
        "title": "Answers About Honey Bees on Miami-Dade Property",
        "desc": ("Plain answers about honey bees on Miami-Dade property: safety, swarms, removal, repairs, scheduling, "
                 "condos, HOAs and what happens to the bees afterward."),
        "kicker": "Answers",
        "h1": "What Miami-Dade Owners Ask Before a Bee Removal",
        "lede": "Grouped by what you are probably trying to figure out. If your question is not here, text it to us with a photo.",
        "quick": ("Most questions come down to three things: whether the bees are dangerous right now, whether they will "
                  "leave on their own, and what it takes to get them out without wrecking the wall. The short version "
                  "is that a resting swarm usually moves on, a colony with comb does not, and live removal clears out "
                  "the bees and the comb in one job."),
        "band": ("Question not on the list?", "Call or text it to us with a photo. A short conversation usually answers it."),
        "groups": [
            ("Safety right now", [
                ("Bees are stinging. What do I do first?",
                 "Move everyone indoors and shut doors and windows. Do not swat or spray, since that brings more bees out. "
                 "Dial 911 right away if a person's lips or throat swell, they wheeze, or they took a lot of stings. "
                 "After that, phone us; anyone actively being stung gets handled ahead of routine work."),
                ("Is it safe to mow or trim near the colony?",
                 "Not until it has been removed. Mower and trimmer vibration and noise are a common reason colonies get "
                 "defensive. Keep machines, kids and pets well back from the entrance."),
                ("Are Miami honey bees more aggressive than elsewhere?",
                 "South Florida has Africanized honey bees mixed into its wild population, and some colonies defend their "
                 "nest harder than others. You cannot tell by looking, so treat every wild colony with care."),
            ]),
            ("Swarms and colonies", [
                ("What is the difference between a swarm and a hive?",
                 "A swarm is a clump of bees resting in the open with no comb, waiting for scouts to choose a home. Once "
                 "they pick a hollow and start drawing wax inside it, you have an established colony. Swarms tend to leave; "
                 "colonies stay."),
                ("How fast does a colony grow inside a wall?",
                 "It depends on the season and the space, but a colony that settles in spring can fill a good part of a "
                 "wall bay with comb within months. The sooner it comes out, the smaller the opening and the repair."),
                ("I only see a few bees at a crack. Is that a hive?",
                 "It might be scouts checking the gap, or the first days of a colony. Watch for a steady stream going in "
                 "and out over an hour. Our [[guide:scout-bees|scout bee article]] explains how to tell."),
            ]),
            ("The removal itself", [
                ("Does getting the comb out mean opening up drywall or stucco?",
                 "When the comb is inside, yes, because the comb has to come out. A thermal camera shows where it sits so "
                 "the cut lands on target and stays small."),
                ("How long does a removal take?",
                 "A swarm can be boxed quickly. A colony inside a structure usually takes a few hours, longer when it "
                 "spreads across several cavities or sits high up."),
                ("What happens to the bees?",
                 "They are boxed with their comb and brood and handed to beekeepers, who rehome them. No colony is "
                 "exterminated."),
                ("Do you take out the honeycomb too?",
                 "Always. Leaving comb behind invites fermenting honey, pests and another swarm. See "
                 "[[svc:honeycomb-cleanup|comb and honey cleanup]]."),
            ]),
            ("Repairs and follow-up", [
                ("Who fixes the opening afterward?",
                 "Our own licensed contractors, roofers and painters can rebuild stucco, drywall, soffit and tile, or you "
                 "can have your own contractor finish it once we seal the entry."),
                ("A colony returned to my patched wall. Now what?",
                 "Tell us. A colony settling again behind a patch our crew made falls under our workmanship warranty and a crew is sent back."),
                ("Can I get photos of the work?",
                 "Yes, on request, along with an itemized invoice. Associations, landlords and buyers often ask for both."),
            ]),
            ("Buildings, boards and scheduling", [
                ("The building manager wants a COI before anyone goes on the roof. Can you send one?",
                 "Yes. Tell us who should be named as certificate holder, usually the association or its management "
                 "company, and the COI is sent ahead of the visit. We carry a license and insurance for this work."),
                ("Our shop is open nine to six. Can the visit happen outside that?",
                 "Yes. Storefronts, offices and schools often prefer early or late visits. After-hours work is priced "
                 "above a weekday visit."),
                ("Do you cover my part of the county?",
                 "We cover all of Miami-Dade, from the beaches to the farm roads, and nowhere outside it. The "
                 "[[page:county|county page]] lists the places we serve."),
            ]),
        ],
    },

    # ------------------------------------------------------------ who we are
    "who": {
        "title": "About Miami Bee Rescue: Live Removal, No Poison",
        "desc": ("Who we are and how we work: live honey bee removal across Miami-Dade, colonies rehomed with beekeepers, "
                 "our own repair crews and a 24-hour response."),
        "kicker": "Who we are",
        "h1": "The Crew Behind Miami-Dade's Live Bee Removals",
        "lede": "A removal company that serves one county and has one rule about the bees: they leave alive.",
        "quick": ("Miami Bee Rescue takes honey bee colonies out of buildings, trees and equipment anywhere in Miami-Dade "
                  "and gives them to beekeepers. We are licensed and insured, answer the phone at all hours, respond "
                  "within 24 hours, and use our own licensed contractors, roofers and painters to put things back "
                  "together."),
        "body": [
            ("Why live removal and nothing else",
             "Honey bees pollinate a long list of the plants South Florida grows, from backyard avocado and lychee trees to the "
             "groves and nurseries down in the Redland. Killing a colony solves the problem for a few weeks and leaves "
             "the comb behind. Taking it out alive solves it for good and keeps the bees working somewhere they are "
             "wanted.\n\nSo we do not sell extermination, and we do not spray colonies in walls. Every job ends with the "
             "bees boxed up for a beekeeper."),
            ("One county, all of it",
             "We work Miami-Dade and nowhere else. That covers condo towers on the barrier islands, older bungalows in the "
             "city's neighborhoods, gated communities in the west, and farm buildings in the south. Keeping to one "
             "county is how we can promise a response within 24 hours of every call."),
            ("What you can hold us to",
             "Our workmanship is warrantied, which means a return trip if bees get back into any opening we closed. If you need paperwork, we can provide a "
             "certificate of insurance, photos of the work and an itemized invoice. If you call at 3 a.m., someone "
             "answers. Those are the promises; anything else would be marketing."),
            ("How to reach us",
             "Call or text any time, or use the form below. Texting a picture of the gap the bees use is the "
             "fastest way to get a useful answer."),
        ],
        "commit_h": "What every job includes",
        "commitments": [
            ("bee", "The colony leaves alive", "Bees, brood and comb are moved together and handed to a beekeeper."),
            ("heat", "A look before any cutting", "A heat camera traces the warm brood nest through the surface before a single cut is made."),
            ("check", "The cavity is cleared", "Honey and wax are scraped out so nothing ferments or draws new bees."),
            ("home", "The entry is closed", "And if bees come back to that sealed spot, so do we."),
            ("shield", "Proof when you need it", "Certificates of insurance, photos and itemized invoices on request."),
        ],
        "band": ("Bees on your property today?", "Pick up the phone, send a picture by text, or fill in the form. Whichever you choose, the 24-hour response guarantee applies, and stinging cases are taken first."),
    },

    # ------------------------------------------------------------ request
    "request": {
        "title": "Request Bee Removal in Miami-Dade: Free Quote",
        "desc": ("Send a free quote request for honey bee removal anywhere in Miami-Dade. Name, phone and location are "
                 "all we need. Calls and texts answered 24/7."),
        "kicker": "Request removal",
        "h1": "Request Bee Removal Anywhere in Miami-Dade",
        "lede": "Fill in the short form, call, or text a photo. Whichever is easiest for you works for us.",
        "quick": ("The form goes straight to the person who books removals. Expect a callback from our number within 24 "
                  "hours, sooner when someone is being stung. If you can, text a photo of the entrance as well; it often "
                  "lets us give you a price range on the first call."),
        "alarm": ("Shut everyone, two-legged and four-legged, inside. A sting victim whose face or throat puffs up, "
                  "who struggles to breathe, or who was hit many times needs 911. Then skip the form and phone us."),
        "form_h": "Your removal request",
        "ways_h": "Other ways to reach us",
        "ways": [
            ("phone", "Call", "Best when bees are stinging or getting inside the house. A real person takes the call whatever the hour."),
            ("chat", "Text a photo", "Stand back, zoom in on the entrance, and send it with your neighborhood. Add a "
             "second shot that shows the whole wall or roofline."),
            ("form", "Email", "Fine for planning ahead, for property managers sending several addresses, or for "
             "attaching documents."),
        ],
        "body": [
            ("What happens after you send it",
             "We read the details, look at any photos, and call you back from our main number. On that call we work out "
             "whether it is a swarm or an established colony, roughly where the comb sits, and which price range is "
             "likely. Then we set a visit time that works for you, or for your building manager or gate."),
        ],
    },

    # ------------------------------------------------------------ 404
    "notfound": {
        "title": "Page Not Found | Miami Bee Rescue",
        "desc": ("This address does not lead anywhere on our site. Use the links here to find bee removal help in "
                 "Miami-Dade, or call or text us at any hour."),
        "kicker": "Error 404",
        "h1": "No Page Here, but Miami-Dade Bee Help Is One Tap Away",
        "lede": ("Whatever link brought you here points at nothing we publish. If you have bees to deal with, the buttons "
                 "below reach us directly, and the list underneath covers the pages people use most."),
        "links_h": "Try one of these",
        "links": [("/", "Homepage"), ("/removal/", "All removal services"), ("/miami-dade/", "Places we serve"),
                  ("/cost/", "What removal costs"), ("/answers/", "Common questions"), ("/request-removal/", "Request removal")],
    },

    # ------------------------------------------------------------ llms.txt
    "llms": {
        "summary": ("Miami-Dade County, Florida bee removal outfit that works only with live methods: wild honey bee colonies are "
                    "boxed up and passed to beekeepers rather than killed."),
        "intro": ("Service-area business with no public storefront. Crews travel to homes, condos, HOAs, businesses, "
                  "docks, nurseries and farms anywhere in Miami-Dade County, and work nowhere outside it."),
        "area": "Service area: Miami-Dade County, Florida only",
        "hours": "Phones answered 24 hours a day, 7 days a week; response guaranteed within 24 hours",
        "facts": [
            "Live, humane removal only; bees are relocated to beekeepers",
            "Licensed and insured; certificates of insurance for HOAs, condo associations and businesses",
            "Stinging emergencies handled first",
            "Thermal imaging used to locate hidden colonies",
            "Repairs by the company's own licensed contractors, roofers and painters",
            "Warrantied workmanship: if bees return to a spot the company sealed, it comes back out",
            "Free quotes; night and weekend emergency calls cost more than weekday visits",
            "Typical ground-level jobs about $300 to $400; complex jobs with repairs can reach the thousands",
            "Photos of the work and an itemized invoice available on request",
        ],
    },
}
