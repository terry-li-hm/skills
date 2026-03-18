---
name: eow
description: End-of-work checkpoint (afternoon/early evening). Synthesise the work day, capture work mood, note unfinished threads. Use when user says "eow", "end of work", "done for the day". Evening sequence is eow → quies → daily. NOT for session end (use legatum) or bedtime close (use daily).
user_invocable: true
disable-model-invocation: true
---

# End of Work

Work-day close — the gap between per-session `/legatum` and bedtime `/daily`.

## Triggers

- "eow", "end of work", "done working", "closing work"
- After the last work session of the day (before evening personal time)

## What This Is

A checkpoint that looks at the **whole work day** as a unit. `/legatum` handles individual sessions. `/daily` handles the full day before bed. This sits between them: "how was the work day?"

## What This Is NOT

- Not a session wrap (that's `/legatum`)
- Not the daily close (that's `/daily` — handles tomorrow preview, bedtime mood)
- Does not write the Tomorrow section

## Workflow

1. **Prep (silent)** — before the conversation:
   - Run `date` (HKT). If fails, use system-provided date.
   - Read today's daily note (`~/notes/Daily/YYYY-MM-DD.md`) — session logs from `/legatum` should already be there.
   - Scan `~/notes/TODO.md` for items with today's date or imminent due dates.
   - Run `gog gmail search "in:inbox" --limit 5`.
   - If daily note is empty/missing, delegate history scan to a subagent.

2. **Conversation** — ask Terry one open question: **"How was the work day?"**
   - Let Terry talk. Follow up naturally — dig into what mattered, what felt off, what's unfinished.
   - Use the daily note and TODO scan as context to ask good follow-up questions (don't dump them as a report).
   - If inbox has items, mention it naturally in the conversation ("also, X unread — worth clearing before you switch off?").
   - This should feel like a 2-minute chat, not a form. 2-3 exchanges max.

3. **Summarise** — once the conversation feels done, write the EOW close:

```markdown
