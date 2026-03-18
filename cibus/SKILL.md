---
name: cibus
description: >-
  Restaurant finder for Hong Kong — takes location, occasion, and constraints
  (dietary, meds, budget, corkage) → searches OpenRice → returns ranked shortlist.
user_invocable: true
triggers:
  - cibus
  - find restaurant
  - find a restaurant
  - restaurant recommendation
  - where to eat
  - dinner spot
  - lunch spot
  - openrice
---

# Cibus — Restaurant Finder

*cibus* (Latin: food, nourishment). Structured restaurant search for Hong Kong,
built on OpenRice as primary data source. Integrates active health context
(medications, dietary constraints) so recommendations account for the full picture.

## Triggers

- `/cibus <query>` — e.g. `/cibus italian near central, 4 people, corkage friendly`
- `/cibus --quick <area>` — fast mode: skip ranking, return first 5 matches
- Natural language: "find a restaurant", "where should we eat", "dinner spot near TST"

## Input Parsing

Extract from the query (prompt for anything critical that's missing):

| Field | Required | Example |
|-------|----------|---------|
| **Area / location** | Yes | "Central", "near Kornhill", "Wan Chai" |
| **Cuisine** | No | "Italian", "Japanese", "any" |
| **Party size** | No | 2 (default) |
| **Occasion** | No | "birthday dinner", "casual lunch", "business" |
| **Budget** | No | "$200-400pp", "splurge", "cheap" |
| **Constraints** | No | "corkage friendly", "outdoor seating", "kid-friendly" |

## Steps

### 1. Health context check

Before searching, read `~/notes/NOW.md` and check memory for active health context
(medications, conditions, dietary restrictions). If relevant, integrate as a
constraint — e.g. if on Klacid, deprioritise raw-food-heavy restaurants (sashimi,
poke) and note "eat cooked food with medication" in output.

### 2. Build search query

Construct an OpenRice search URL or use `noesis search` / `exauro search` for
initial discovery:

```bash
# Option A: Direct OpenRice search via exauro (URL discovery)
exauro search "openrice hong kong <cuisine> <area> <constraints>"

# Option B: Structured facts via noesis
noesis search "best <cuisine> restaurants in <area> hong kong <constraints>"
```

### 3. Fetch restaurant details

For each candidate (up to 5), fetch the full OpenRice listing:

```bash
# peruro is the only tool that reliably bypasses OpenRice's Cloudflare WAF
peruro "<openrice-listing-url>"
```

**Cost:** ~1 Firecrawl credit per page. Budget: 5 credits per `/cibus` invocation
(5 restaurant pages). Use `noesis search` for initial filtering to avoid wasting
credits on poor matches.

**WAF bypass strategy** (in priority order):
1. `porta run --domain openrice.com` — cookie injection from live Chrome session
   (untested on OpenRice as of 2026-03-19; test before relying on this)
2. `peruro <url>` — Firecrawl residential proxies (confirmed working 2026-03-08)
3. Hidden API probing — OpenRice may have unprotected JSON endpoints behind the SPA
   (untested; see `~/notes/Reference/browser-automation/browser-hidden-api.md`)

### 4. Extract structured data

From each listing, extract:

- **Name** (EN + ZH)
- **Address** (EN + ZH)
- **Phone**
- **Opening hours** (flag if closed at target time)
- **Price range** (per person)
- **Cuisine tags**
- **Corkage policy** (fee, BYOB terms, cake cutting fee)
- **Rating / review count**
- **Notable reviews** (1-2 sentences from recent reviews)
- **Booking availability** (if shown)

### 5. Rank and present

Rank by relevance to the query. Present as a compact table:

```
## Restaurant Shortlist — Italian near Central (4 pax, corkage friendly)

| # | Restaurant | Price | Corkage | Rating | Notes |
|---|-----------|-------|---------|--------|-------|
| 1 | Osteria Marzia 海邊餐廳 | $400-600pp | Free BYOB | 4.2 ★ (312) | Hotel-quality pasta, harbour view |
| 2 | ... | ... | ... | ... | ... |

⚕️ Note: You're on Klacid — eat cooked food (avoid raw fish/salad-heavy spots).

### Top pick: Osteria Marzia
- 📍 Address (EN + ZH)
- 📞 Phone
- 🕐 Hours (open at target time ✓)
- 🍷 Corkage: Free, max 2 bottles
- 💬 "Excellent handmade pasta, book window seats" — recent review
```

### 6. Offer next steps

- "Shall I book via OpenRice?" (draft the booking details for Terry)
- "Want me to check more options?"
- "Add to calendar?" → hand off to `/fasti`

## Output

Compact ranked table (step 5 format). Always include:
- Health/med warnings if active
- Corkage details if requested or if occasion suggests wine
- Opening hours validated against target time
- Both EN and ZH names/addresses

## Boundaries

- Do NOT book without confirmation — draft only.
- Do NOT use `WebFetch`, `defuddle`, or `agent-browser` for OpenRice (all blocked by WAF).
- Do NOT spend >5 Firecrawl credits per invocation without asking.
- Do NOT ignore active medication/dietary context from vault.
- Do NOT search outside Hong Kong (out of scope for v1).

## WAF Research Notes (Design-Time)

OpenRice uses **Cloudflare Bot Management** with SHA-256 Proof-of-Work challenge.
Empirically confirmed 2026-03-08: every headless tool (WebFetch, defuddle, summarize,
agent-browser with persistent profile, curl, kleis) returns only the challenge page.

**What works today:** `peruro` (Firecrawl) — residential proxies + real browser
fingerprints. Confirmed: name, address, phone, hours, reviews, corkage fees all
returned. Cost: 1 credit/page.

**Unexplored angles for v2:**
1. `porta run --domain openrice.com` — inject Chrome cookies into a Playwright
   session that fetches the page in one shot. May fail if PoW token is per-session
   rather than cookie-based. Needs empirical test.
2. Hidden API discovery — curl OpenRice JS bundles, grep for `fetch(` / AJAX
   endpoints. OpenRice SPA likely has internal JSON routes that may be unprotected.
3. SHA-256 PoW solver — reverse-engineer the challenge JS, compute the proof in
   Rust/Python, submit with the request. Heavy engineering; defer unless porta + API
   both fail.

**Canonical routing:** `exauro search` (URL discovery) → `peruro` (page fetch).
See `~/notes/Reference/search/scraping-routing.md`.

## See also

- `/sched` — reminders and scheduling
- `/fasti` — calendar integration
- `/rector` — if building the cibus CLI tooling
- `~/officina/docs/solutions/cloudflare-bypass-tools.md` — WAF bypass benchmark
- `~/notes/Reference/search/scraping-routing.md` — scraping tool routing
- `~/notes/Reference/browser-automation/browser-hidden-api.md` — hidden API pattern
