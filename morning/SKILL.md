---
name: morning
description: Daily briefing to start the day with focus. Use when user says morning, good morning, or gm.
user_invocable: true
---

# Morning Review

Overnight delta brief — what changed since you slept.

The `/daily` skill previews tomorrow's plate at end of day. This skill focuses on **what's new** since then: overnight messages, weather, and anything that shifted.

## Triggers

- "morning"
- "good morning"
- "gm"

## Steps

1. **Get today's date and day of week**

2. **Staleness check** (context gap detection):
   - Run `stat -f '%Sm' -t '%Y-%m-%d' ~/notes/WORKING.md ~/notes/Capco\ Transition.md ~/notes/TODO.md`
   - If any file's last-modified date is >48h old, flag it: "WORKING.md last updated X — may be behind reality"

3. **Yesterday's daily note** — quick glance:
   - Read `~/notes/YYYY-MM-DD.md` (yesterday)
   - Pull the `## Tomorrow` section if it exists — this is the plate preview from last night
   - Pull any `## Follow-ups` items — these are carryover

4. **Overnight messages** (the core value of this skill):
   - Scan Gmail for Capco/HR emails (past 24h): `gog gmail search "capco OR first advantage OR background check OR PILON OR alison" | head -10`
   - Flag anything requiring action

5. **Check cron logs** (overnight output):
   - Check `~/logs/cron-weather.log` and `~/logs/cron-capco.log` for recent entries
   - Note any failures or missing deliveries

6. **Check overnight OpenCode queue** (if any):
   - Read `~/notes/WORKING.md` — look for `## Overnight Queue` section
   - If present: check each listed output file exists and isn't empty (`wc -l`)
   - Report: which arrived, which failed silently (missing or 0 bytes)
   - Flag files for review: "3/3 overnight tasks landed — review when ready"
   - If no Overnight Queue section, skip silently

7. **Weather** (action-oriented only):
   - `/hko` — focus on warnings (typhoon, rainstorm, extreme heat) and rain probability
   - Skip if already delivered by cron and no warnings active

8. **Overdue + today's deadlines** (quick scan, not full TODO review):
   - Read `~/notes/TODO.md`
   - Surface only: items with `due:` <= today, items with `when:` <= today
   - Skip someday items, skip items due later this week
   - This is a reminder, not a restatement — daily's tomorrow preview already set expectations

9. **Deliver the brief** — concise, no filler:

## Output Format

```
**Tuesday, February 12, 2026**

Overnight:
- [New messages, cron results, or "Quiet night."]

Warnings:
- [Weather warnings, staleness flags, or omit section]

Today:
- [Deadlines + overdue items from TODO, or "Plate as previewed last night."]

Carryover:
- [From yesterday's Follow-ups/Tomorrow, or omit if none]
```

## Notes

- This is a delta brief, not a full situational review. Daily already closed last night's loop.
- If yesterday had no daily note (skipped `/daily`), fall back to fuller review: include TODO scan + priority check from vault context files.
- Keep the brief under 15 lines. The point is to start working, not to read a report.
