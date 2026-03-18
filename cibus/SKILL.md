---
name: cibus
description: >-
  Restaurant finder for Hong Kong — takes location, cuisine, and budget
  constraints → calls the cibus CLI (OpenRice API) → returns ranked shortlist.
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

*cibus* (Latin: food, nourishment). Structured restaurant search for Hong Kong
via the `cibus` CLI (`~/officina/bin/cibus`), which queries the OpenRice JSON
API directly — no browser automation, no WAF bypass, no Firecrawl credits.

## Triggers

- `/cibus <query>` — e.g. `/cibus italian central`
- `/cibus --quick <area>` — fast mode: return first 5 matches, skip commentary
- Natural language: "find a restaurant", "where should we eat", "dinner spot near TST"

## CLI Reference

```
cibus [-c CUISINE] [-a AREA] [-b 1-5] [-n ROWS] [-j] [-l] [QUERY ...]
```

| Flag | Meaning |
|------|---------|
| `-c`, `--cuisine` | Cuisine filter (e.g. `italian`, `japanese`, `thai`, `cantonese`) |
| `-a`, `-d`, `--area`, `--district` | District filter (e.g. `central`, `tst`, `mong kok`) |
| `-b`, `--budget` | Price tier: 1=<$50, 2=$51-100, 3=$101-200, 4=$201-400, 5=$401-800 |
| `-n`, `--rows` | Number of results (default 5) |
| `-j`, `--json` | Raw JSON output (for programmatic use) |
| `-l`, `--list` | Print all known cuisines and districts |

**Positional shorthand:** `cibus italian central` is equivalent to `cibus -c italian -a central`.

Supported cuisines include: cantonese, sichuan, shanghainese, taiwanese, japanese,
korean, thai, vietnamese, italian, western, american, international, and more.
Run `cibus --list` if uncertain.

## Steps

### 1. Health context check

Before searching, read `~/notes/NOW.md` and check memory for active health context
(medications, conditions, dietary restrictions). If relevant, integrate as a
note in the output — e.g. if on Klacid, flag that raw-food-heavy restaurants
(sashimi, poke) are less ideal and note "eat cooked food with medication."

### 2. Parse the request

Extract from the user's query (prompt for anything critical that's missing):

| Field | Required | Maps to |
|-------|----------|---------|
| **Area / location** | Yes | `-a` flag |
| **Cuisine** | No | `-c` flag |
| **Budget** | No | `-b` flag (map "$200-400pp" → `4`, "cheap" → `1-2`, "splurge" → `5`) |
| **Party size** | No | Noted in output, not a CLI param |
| **Occasion** | No | Influences ranking commentary |
| **Constraints** | No | Noted in output (corkage, outdoor, kid-friendly) |

### 3. Run the CLI

```bash
cibus -c <cuisine> -a <area> -b <budget> -n <rows>
```

Default to 5 results. Use `--json` when you need to do further filtering or
extract fields the table doesn't show (e.g. addresses, phone numbers, URLs).

If the user asks about a cuisine or district not in the known list, run
`cibus --list` to check, then fall back to the closest match or omit that filter.

### 4. Enrich and present

The CLI outputs a formatted table with: name, cuisine, district, score, review
counts (smile/cry), price tier, open-now status, and today's hours. Below the
table it prints OpenRice URLs, addresses, and phone numbers.

Wrap the CLI output in context:

```
## Restaurant Shortlist — Italian near Central

<paste CLI table output>

### Commentary
- **Top pick:** [Name] — [why it fits the occasion/constraints]
- **Budget pick:** [Name] — [if relevant]
- Addresses and phone numbers are listed below the table.

⚕️ Note: [Health/med warnings if active]
```

For `--quick` mode, skip the commentary — just present the table.

### 5. Offer next steps

- "Shall I look up more details on any of these?" (run `cibus --json` + filter)
- "Want more results?" (increase `-n`)
- "Add to calendar?" → hand off to `/fasti`

## Output

Compact table from the CLI, wrapped with occasion-relevant commentary. Always include:
- Health/med warnings if active
- Corkage note if the occasion suggests wine (this data is not in the API; note
  that Terry should verify corkage policy directly with the restaurant)
- Opening hours from the table, validated against target time
- OpenRice links for each restaurant

## Boundaries

- Do NOT book without confirmation — draft only.
- Do NOT search outside Hong Kong (out of scope).
- Do NOT ignore active medication/dietary context from vault.
- Corkage, outdoor seating, kid-friendliness are NOT available via the API —
  flag these as "verify directly" rather than guessing.

## See also

- `/fasti` — calendar integration
- `/sched` — reminders and scheduling
- `~/officina/bin/cibus` — the CLI source
