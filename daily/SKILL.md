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

2. **Review what happened today**:
   - **Delegate history scan to a subagent** — use Task tool (subagent_type: "general-purpose", model: "haiku") with prompt: "Run `python ~/scripts/chat_history.py --full` and synthesize a concise summary of today's activity. Group by theme, not chronologically. List key accomplishments, decisions made, and unfinished threads. Keep output under 30 lines."
   - This keeps the raw history (~10K+ tokens on busy days) out of the main context window.
   - Scan current conversation for additional context
   - Ask if anything else worth noting

3. **Create/update daily note** at `~/notes/YYYY-MM-DD.md`:

```markdown
# YYYY-MM-DD

## Activity
- [What happened]

## Learnings
- [Insights, if any]

## Follow-ups
- [ ] [Things to do tomorrow]

## Mood
[Optional, 1-5 or word]
```

4. **Keep it short** — not everything needs logging

## Notes

- If note exists, append rather than overwrite
- Don't force entries — "nothing notable" is fine
- This is a log, not a ritual
