---
name: daily
description: End-of-day log. Capture activity, learnings, and mood in a daily note. Use when user says "daily", "end of day", "eod", or at end of day.
---

# Daily

End-of-day log → daily note.

## Triggers

- "daily", "end of day", "eod"
- Natural end of a work day

## Workflow

1. **Get today's date** (YYYY-MM-DD, HKT)

2. **Review what happened today**:
   - Scan conversation for activity
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
