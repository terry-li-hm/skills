---
name: linkedin-research
description: Reference for finding people on LinkedIn and extracting profile data. Consult when task involves LinkedIn profile lookup, team mapping, or org research.
user_invocable: false
---

# LinkedIn People Research

## When to Consult

- Finding someone's LinkedIn profile
- Extracting profile details (experience, education, skills)
- Mapping team/org structure from LinkedIn

## Search Strategy (Waterfall)

1. **Name + company + site:linkedin.com** — default first attempt
2. **Role/title + company + site:linkedin.com** — when name search fails (privacy-gated names show as "Simon E.")
3. **`pplx search`** — better platform indexing than WebSearch
4. **`agent-browser` extraction** — when URL is known but content needed

Search engines index the *display name*, not the vanity URL slug. If someone's profile shows "Simon E." to non-connections, no amount of name variation will find them. Pivot to title/role immediately.

**Example pivot:**
```
# Fails — privacy-gated display name
"Simon Eltringham" HSBC site:linkedin.com

# Works — headline text is rarely abbreviated
HSBC "Director" "Responsible AI" "Risk Solutions" site:linkedin.com
```

## Profile Extraction

- `WebFetch` → HTTP 999 (always blocked by LinkedIn)
- `agent-browser` with `AGENT_BROWSER_PROFILE=1` → `open` → `snapshot`
- Scroll + re-snapshot for experience/education sections below the fold
- Key fields: headline, location, current company, experience list, education

## Org Chart Mapping

- Search multiple team members → cross-reference titles/dates → infer hierarchy
- Title signals: "Group" > "Director" > "Manager"; "Lead" implies team ownership
- Mark unverified reporting lines with `[?]`
- Save to vault with ASCII chart format (established pattern in Capco notes)

### Network Graph Traversal

Keyword search misses people whose titles don't reflect their work (common in consulting — "Principal Consultant" managing an AI engagement). Mine the sidebar from known profiles instead:

1. Open a known profile via `agent-browser` (already doing this for extraction)
2. The snapshot includes **"People also viewed"** and **"People you may know from [Company]"** sections — extract names and URLs
3. Follow those links to discover colleagues keyword search would miss
4. Repeat from the most relevant new profiles for 1-2 hops

This data is free — it's already in the snapshot. Don't discard it.

**Limitation:** Sidebar results are LinkedIn's algorithm, not a complete org chart. One message to an insider ("who else should I know?") is still faster for a complete team list.

## Gotchas

- LinkedIn abbreviates surnames for non-connections ("Simon E.")
- The existing `linkedin-engage` skill is for **content** (posts/comments) — this skill is for **research**
- Profile data from snapshots may be incomplete — check "Show all X experiences" expand links
