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

2. **Read today's daily note** (`~/notes/YYYY-MM-DD.md`)
   - `/retro` appends session summaries throughout the day, so the note should already have an `## Activity` section with detailed session logs.
   - If the note is empty or missing, **fallback:** delegate history scan to a subagent — use Task tool (subagent_type: "general-purpose", model: "haiku") with prompt: "Run `python ~/scripts/chat_history.py --full` and synthesize a concise summary of today's activity. Group by theme. List key accomplishments, decisions, and unfinished threads. Keep output under 30 lines."

3. **Review with Terry:**
   - Show what's already logged — "Here's what retro captured today..."
   - Ask: anything missing? Any sessions that didn't get a retro?
   - Ask for mood (1-5 or a word)

4. **Finalize the daily note** — add/update these sections:

```markdown
## Learnings
- [Insights from the day, if any — check retro captures]

## Follow-ups
- [ ] [Things to do tomorrow]

## Mood
[1-5 or word, with brief colour if Terry offers it]
```

5. **Quick reflection** — based on the session logs, offer a 1-2 sentence observation on how the day went (time allocation, focus vs scatter, energy patterns). Keep it honest, not cheerful.

7. **Tomorrow preview** — scan for what's queued tomorrow:
   - Get tomorrow's date (`date -v+1d +%Y-%m-%d`)
   - Read `~/notes/TODO.md` and surface:
     - Items with `due:` = tomorrow (deadlines)
     - Items with `when:` = tomorrow (scheduled starts)
     - Any overdue items (`due:` < tomorrow) that weren't completed
   - Check if tomorrow's daily note already exists (carryover from today's follow-ups)
   - Present as a short "Tomorrow" section (3-5 lines max):

```markdown
## Tomorrow
- [Deadlines, scheduled items, overdue carryover — or "Clear plate."]
```

   - This is a heads-up, not a plan. Morning skill handles the real-time brief.

## Notes

- If note exists, append/update rather than overwrite
- Don't force entries — "nothing notable" is fine
- The value is in the reflection, not the logging — retro handles the logging
- This is lightweight by design: retro does the heavy lifting throughout the day
- Tomorrow preview is a closing thought — keep it to what's *known*, don't speculate
