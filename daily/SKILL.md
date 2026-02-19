---
name: daily
description: End-of-day log. Capture activity, learnings, and mood in a daily note. Use when user says "daily", "end of day", "eod", or at end of day.
user_invocable: true
---

# Daily

End-of-day log → daily note.

## Triggers

- "daily", "end of day", "eod"
- Natural end of a work day

## Workflow

1. **Get today's date** (YYYY-MM-DD, HKT)

2. **Read today's daily note** (`~/notes/Daily/YYYY-MM-DD.md`)
   - `/wrap` appends session summaries throughout the day, so the note may already have session logs.
   - If the note is empty or missing, **fallback:** delegate history scan to a subagent — use Task tool (subagent_type: "general-purpose", model: "haiku") with prompt: "Run `python ~/scripts/chat_history.py --full` and synthesize a concise summary of today's activity. Group by theme. List key accomplishments, decisions, and unfinished threads. Keep output under 30 lines."

3. **Thematic summary** — cluster the day's sessions into 3-5 major themes (e.g. "DBS prep", "system hygiene", "personal"). For each theme: key actions and outcomes in one line. Present to Terry in chat before writing.

4. **Review with Terry:**
   - Show the thematic summary — "Here's how today groups..."
   - Ask: anything missing? Any sessions without a wrap?
   - Ask for mood (1-5 or a word)

5. **Tomorrow preview** — scan for what's queued tomorrow:
   - Get tomorrow's date (`date -v+1d +%Y-%m-%d`)
   - Read `~/notes/TODO.md` and surface:
     - Items with `due:` = tomorrow (deadlines)
     - Items with `when:` = tomorrow (scheduled starts)
     - Any overdue items (`due:` < tomorrow) that weren't completed
   - Check if tomorrow's daily note already exists (carryover from today's follow-ups)

6. **Fix header** — validate and update the `# YYYY-MM-DD — Day` line:
   - Verify day-of-week matches `date` output (wrap sometimes gets this wrong). Fix if needed.
   - Append a thematic tagline: compress the 3-5 themes to a few words each, comma-separated.
   - Result: `# 2026-02-19 — Thursday — Doumei shipped, CV submitted, GARP grinding`

7. **Finalize the daily note** — append all closing sections at once:

```markdown
---

## Reflection

[Thematic summary paragraph — group session logs into major themes with key outcomes. Then 1-2 sentences on patterns: time allocation, focus vs scatter, energy, what worked vs what drifted. Honest, not cheerful.]

## Learnings

- [Insights from the day, if any — check wrap captures]

## Follow-ups

- [ ] [Things to do tomorrow]

## Mood

[1-5 or word, with brief colour if Terry offers it]

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
