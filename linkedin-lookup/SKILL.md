---
name: linkedin-lookup
description: Look up a person on LinkedIn and save a structured profile note. Use when user says "linkedin lookup", "look up on linkedin", or "/linkedin-lookup".
user_invocable: true
arguments: name (required), company/role hint (optional, space-separated after name)
---

# LinkedIn Profile Lookup

Extract structured profile data from LinkedIn and save it as a person note in the vault.

## Workflow

### 1. Parse Input
- Identify the target **name** (e.g., "Ho Yin Li").
- Identify any optional **company/role hints** provided after the name (e.g., `Capco`, `Hedge Fund`).

### 2. Find LinkedIn URL (Search Waterfall)
Follow the search pattern from `linkedin-research` to find the most accurate profile URL:
1. **WebSearch:** `"<name>" site:linkedin.com` (+ company/role hint if provided).
2. **Privacy Pivot:** If results show privacy-gated names (e.g., "Simon E."), search for `"<role/title>" "<company>" site:linkedin.com` to find the matching profile.
3. **PPLX Fallback:** `pplx search "<name> linkedin <company>"` — better LinkedIn indexing, often finds full legal names that WebSearch misses (e.g., "Marco King Tao Chiu" when searching "Marco Chiu").
4. **LinkedIn Search (agent-browser):** If external search fails, search directly on LinkedIn — it handles name variations and company filtering better than Google:
   ```bash
   agent-browser open "https://www.linkedin.com/search/results/people/?keywords=<name>%20<company>" --profile
   agent-browser snapshot --profile
   ```
   Pick the correct result from the snapshot.
5. **Disambiguation:** If multiple potential matches appear, present the options to the user with brief context (headline/location) and ask them to select the correct one.
6. **Exit:** If no match is found, report this to the user and stop.

### 3. Extract Profile via agent-browser
LinkedIn is login-gated; always use the persistent profile. Commands must be executed **sequentially** (never chain with `&&`).

```bash
# Open profile and take initial snapshot
agent-browser open "<URL>" --profile
agent-browser snapshot --profile

# Scroll to capture experience and education below the fold
agent-browser eval "window.scrollTo(0, document.body.scrollHeight/2)" --profile
agent-browser snapshot --profile
agent-browser eval "window.scrollTo(0, document.body.scrollHeight)" --profile
agent-browser snapshot --profile

# Cleanup
agent-browser close --profile
```

**Extraction Fields:** Headline, location, current role, experience list (period, role, company), education (degree, institution), and "About" section.

**Note:** If snapshots fail or a login wall appears, suggest the user run `agent-browser --headed open "https://linkedin.com" --profile` to complete manual authentication first.

### 4. Save to Vault
- Ensure the directory exists: `mkdir -p ~/notes/People/`
- Target file: `~/notes/People/<Name> Profile.md`
- **Overwrite check:** If the file already exists, ask the user: "Profile for <Name> already exists. Overwrite or skip?"

#### Note Template
Use the following structure for the note. Get the current date using `date +%Y-%m-%d`.

```markdown
---
tags: [people, linkedin]
date: YYYY-MM-DD
---

# <Name> — Profile

**Role:** <current title>
**Company:** <company>
**Location:** <city>
**LinkedIn:** <url> — <connection degree, e.g. 1st degree>, <N mutual connections>

---

## Background

| Period | Role | Company |
|--------|------|---------|
| <period> | <role> | <company> |

**Education:** <degree, institution>

**About:** <about section text, if available — 2-3 sentences max>

---

## Connection History

| Date | Type | Summary |
|------|------|---------|
| YYYY-MM-DD | <Met / LinkedIn DM / Email / Call / etc.> | <1-line summary — what was discussed or sent> |

---

## Notes

- **Why they matter:** <networking angle, potential client, colleague, referral, etc.>
- <Key facts to remember — shared interests, context, anything relevant for next interaction>

---

**Related:** <[[vault links]]>
```

**What to fill in for each section:**
- **Connection History:** Log every meaningful touchpoint — first meeting, messages sent/received, follow-ups. Be specific enough to resume context after months of silence.
- **Notes:** Why does this person matter? What would you want to remember before your next interaction? Shared experiences, their priorities, anything that would make the next conversation warmer.
- **Tags:** Add context tags beyond `people, linkedin` — e.g. `cncbi`, `capco`, `networking`, `hsbc`.

### 5. Confirm
Provide a concise confirmation of the action:
- **Output:** "Saved to ~/notes/People/<Name> Profile.md — <Headline/Current Role>"

## Technical Mandates

- **No WebFetch:** LinkedIn returns HTTP 999; always use `agent-browser`.
- **Sequential Commands:** Never use `&&` with `agent-browser` to avoid "Resource temporarily unavailable" errors.
- **Authentication:** Always include the `--profile` flag for LinkedIn access.
- **Cleanup:** Always call `agent-browser close --profile` at the end of the workflow, even if an error occurs.

## Gotchas

- **`--wait` flag creates a directory in CWD.** Never use `--wait` with `agent-browser open`. It creates a browser profile directory named `--wait/` in the current working directory. Use `sleep` between commands instead.
- **LinkedIn sessions expire.** If snapshot returns a sign-in wall ("Sign in to message..."), re-login: `agent-browser --headed open "https://linkedin.com" --profile`, then close and retry headless.
- **Name variations break external search.** Chinese/Indian names on LinkedIn often use full legal names (e.g., "Marco King Tao CHIU" not "Marco Chiu"). Some users display initials only (e.g., "H Y LI" not "Ho Yin Li"). If WebSearch fails, escalate to pplx (which often finds full names) or use LinkedIn's own search via agent-browser — LinkedIn matches initials to full names better than Google does.
- **Vault context enriches profiles.** After saving, check `~/notes/` for existing context on the person (e.g., interview notes, meeting prep) and add a "Context" section to the profile note.
