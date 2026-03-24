---
name: secretion
description: Post to LinkedIn. GATE — requires a tweet first. The tweet tests the claim; LinkedIn expands with blindspots addressed.
user_invocable: false
context: fork
---

# announce — post to LinkedIn

## Gate: tweet first

**Do not post to LinkedIn without tweeting the core claim first.**

The pipeline is ordered:
1. **Tweet** — compress to 280, test publicly (`bird tweet` / tweet skill)
2. **Observe** — did anyone push back? What was missing?
3. **Announce** — expand with blindspots addressed, professional framing

If the tweet landed flat, the LinkedIn post might not be worth writing.

## Posting

Use `agoras` CLI or agent-browser for LinkedIn posting. LinkedIn requires professional framing — not a longer tweet, but a rewrite for the audience.

## Telemetry

After posting to LinkedIn, append one row to `~/notes/Meta/Content Telemetry.md`:

```
| {date} | linkedin | — | {topic} | secretion | {source-tweet truncated to 50 chars} |
```

- **date**: ISO date (YYYY-MM-DD)
- **topic**: 1–5 word label for what the post was about
- **source-tweet**: first 50 chars of the tweet this expanded from

If the file doesn't exist, create it with this header first:

```markdown
# Content Telemetry

| date | channel | slug | title | source-skill | tags |
|------|---------|------|-------|--------------|------|
```

## Quality bar

- **Higher than garden.** LinkedIn is front-stage. Terry reviews voice before shipping.
- **Blindspot-aware.** The tweet exposed what's missing — address it.
- **No insider details.** LinkedIn profile identifies Terry — assume readers check.
