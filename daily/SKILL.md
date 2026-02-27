---
name: daily
description: Bedtime daily close. Full-day reflection, mood, tomorrow preview. Use when user says "daily", "end of day", "eod", or before bed.
user_invocable: true
---

# Daily

Bedtime close → daily note. The final checkpoint of the day.

## Triggers

- "daily", "end of day", "eod"
- Before bed / winding down for the night

## Relationship to /eow

`/eow` (end of work) is the optional mid-day checkpoint — work themes, work mood, unfinished threads. If it was run, the daily note already has an "End of Work" section. This skill builds on top of it:

- **eow was run:** Skip re-summarising work. Focus on evening activity, full-day reflection, and overall mood.
- **eow was NOT run:** Cover the full day (work + personal) in one pass, same as before.

## Workflow

1. **Get today's date** (YYYY-MM-DD, HKT)

2. **Read today's daily note** (`~/notes/Daily/YYYY-MM-DD.md`)
   - Check for existing session logs from `/wrap` and an "End of Work" section from `/eow`.
   - If the note is empty or missing, **fallback:** delegate history scan to a subagent — use Task tool (subagent_type: "general-purpose", model: "haiku") with prompt: "Run `python ~/scripts/chat_history.py --full` and synthesize a concise summary of today's activity. Group by theme. List key accomplishments, decisions, and unfinished threads. Keep output under 30 lines."

3. **Thematic summary:**
   - **If eow exists:** Acknowledge work themes already captured. Add any evening/personal sessions. Synthesise the full day arc (work + personal).
   - **If no eow:** Cluster all sessions into 3-5 major themes (e.g. "DBS prep", "system hygiene", "personal"). For each theme: key actions and outcomes in one line.
   - Present to Terry in chat before writing.

4. **Review with Terry:**
   - Show the summary — "Here's how today groups..."
   - Ask: anything missing? Any sessions without a wrap?
   - Ask for **overall mood** (1-5 or a word) — this is the day mood, distinct from work mood if eow captured one

5. **Tomorrow preview** — scan for what's queued tomorrow:
   - Get tomorrow's date (`date -v+1d +%Y-%m-%d`)
   - Read `~/notes/Schedule.md` — check for recurring commitments on that day of the week
   - Read `~/notes/TODO.md` and surface:
     - Items with `due:` = tomorrow (deadlines)
     - Items with `when:` = tomorrow (scheduled starts)
     - Any overdue items (`due:` < tomorrow) that weren't completed
   - Check if tomorrow's daily note already exists (carryover from today's follow-ups)

6. **Fix header** — validate and update the `# YYYY-MM-DD — Day` line:
   - Verify day-of-week matches `date` output (wrap sometimes gets this wrong). Fix if needed.
   - Append a thematic tagline: compress the themes to a few words each, comma-separated.
   - Result: `# 2026-02-19 — Thursday — Doumei shipped, CV submitted, GARP grinding`

7. **Finalize the daily note** — append all closing sections at once:

```markdown
---

## Reflection

[Full-day synthesis. If eow exists, weave work themes with evening activity into a day arc — don't repeat the eow summary, build on it. If no eow, cover everything. Then 1-2 sentences on patterns: time allocation, focus vs scatter, energy, what worked vs what drifted. Honest, not cheerful.]

## Learnings

- [Insights from the day, if any — check wrap captures]

## Follow-ups

- [ ] [Things to do tomorrow]

## Mood

[1-5 or word, with brief colour if Terry offers it. If eow captured a work mood, note the contrast if interesting — e.g. "Work: 3 (scattered) → Evening: 4 (recharged)"]

## Tomorrow

- [Deadlines, scheduled items, overdue carryover — or "Clear plate."]
```

   - Tomorrow is a heads-up, not a plan. Morning skill handles the real-time brief.

## Notes

- If note exists, append/update rather than overwrite
- Don't force entries — "nothing notable" is fine
- The value is in the reflection, not the logging — wrap handles the session logging
- This is lightweight by design: wrap does the heavy lifting throughout the day
- Tomorrow preview is a closing thought — keep it to what's *known*, don't speculate
- The work mood vs day mood split is optional — if Terry only gives one mood, use it as the day mood
