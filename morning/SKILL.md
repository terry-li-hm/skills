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
   - If job hunting active: check `~/notes/Active Pipeline.md`

5. **Check scout intel** (OpenClaw overnight output):
   - Read `~/signals.log` — the job-heartbeat cron writes recruiter signals here
   - If there are entries from last 24h, summarize: new signals, suppressions, anything needing action
   - Check `~/.openclaw/workspace/memory/` for today's or yesterday's daily notes from OpenClaw
   - Note any cron findings that need Claude Code follow-up

6. **Check overnight OpenCode runs** (if any):
   - Look in `~/notes/opencode-runs/` for recent run directories
   - Read `summary.md` from any runs in the last 24 hours
   - Summarize findings: what ran, what succeeded/failed, key outputs

7. **Check TODO.md**:
   - Read `~/notes/TODO.md` for pending tasks
   - Display any unchecked items `- [ ]` prominently

8. **Scan Gmail for interview confirmations** (past 48 hours):
   - `gog gmail search "interview confirmed OR virtual interview OR interview scheduled" | head -10`
   - Look for subjects containing: "confirmed", "scheduled", "interview", "Teams meeting"
   - Cross-check against TODO.md — if an interview is in email but NOT in TODO.md, flag it
   - Add any missing interviews to TODO.md with date, time, platform, interviewer

9. **Weather check** (optional):
   - `/hko` for Hong Kong weather if going out

10. **Deliver a concise briefing**:
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
