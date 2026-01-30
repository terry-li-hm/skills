---
name: morning
description: Daily briefing to start the day with focus. Use when user says morning, good morning, or gm.
---

# Morning Review

Daily briefing to start the day with focus.

## Triggers

- "morning"
- "good morning"
- "gm"

## Steps

1. **Get today's date and day of week**

2. **Check calendar** (if available):
   - `gog calendar today` for scheduled events
   - Note any meetings, calls, or deadlines

3. **Review yesterday's daily note** (if exists):
   - Path: `~/notes/YYYY-MM-DD.md`
   - Look for incomplete items or carryover tasks

4. **Check for active priorities**:
   - Read `~/notes/CLAUDE.md` for current focus areas
   - Check `~/clawd/MEMORY.md` for recent context
   - If job hunting active: check `~/notes/Active Pipeline.md`

5. **Weather check** (optional):
   - `/hko` for Hong Kong weather if going out

6. **Deliver a concise briefing**:
   - Today's date and day of week
   - Scheduled events
   - Top priorities / focus areas
   - Any carryover from yesterday
   - Keep it short — a quick summary, not a wall of text

## Output Format

```
**Tuesday, January 20, 2026**

Calendar:
- [Scheduled events]

Focus today:
- [Priority 1]
- [Priority 2]

Pending from yesterday:
- [Carryover items if any]

Weather: [if relevant]
```
