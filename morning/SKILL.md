---
name: morning
description: Daily briefing to start the day with focus. Use when user says morning, good morning, or gm.
user_invocable: true
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
   - Check `~/notes/Capco Transition.md` for resignation/onboarding status

5. **Staleness check** (context gap detection):
   - Run `stat -f '%Sm' -t '%Y-%m-%d' ~/notes/WORKING.md ~/notes/Capco\ Transition.md ~/notes/TODO.md`
   - If any file's last-modified date is >48h old, flag it: "WORKING.md last updated X — may be behind reality"
   - This catches status updates shared in conversation but not flushed to vault before `/clear`

6. **Check cron logs** (overnight output):
   - Check `~/logs/cron-weather.log` and `~/logs/cron-capco.log` for recent entries
   - Note any failures or missing deliveries

7. **Check overnight OpenCode runs** (if any):
   - Look in `~/notes/opencode-runs/` for recent run directories
   - Read `summary.md` from any runs in the last 24 hours
   - Summarize findings: what ran, what succeeded/failed, key outputs

8. **Check TODO.md** (Today view):
   - Run `/todo today` logic: get today's date (`date +%Y-%m-%d`), read `~/notes/TODO.md`
   - For each unchecked `- [ ]` line:
     - SKIP if line has `someday`
     - SKIP if line has `when:YYYY-MM-DD` where date > today (not yet started)
     - INCLUDE everything else (Anytime tasks, tasks where `when:` <= today, tasks with `due:`)
   - Show overdue items first (`due:` date < today) with a warning prefix
   - Then show today's actionable items grouped by section
   - End with count: "X tasks today, Y overdue"

9. **Scan Gmail for Capco/HR emails** (past 48 hours):
   - `gog gmail search "capco OR first advantage OR background check OR PILON OR alison" | head -10`
   - Flag anything requiring action (document requests, buyout confirmation, start date changes)

10. **Weather check** (optional):
    - `/hko` for Hong Kong weather if going out

11. **Deliver a concise briefing**:
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
