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
   - Read `~/notes/Daily/YYYY-MM-DD.md` (yesterday)
   - Pull the `## Tomorrow` section if it exists — this is the plate preview from last night
   - Pull any `## Follow-ups` items — these are carryover

4. **Overnight messages** (the core value of this skill):
   - Scan Gmail for Capco/HR emails (past 24h): `gog gmail search "capco OR first advantage OR background check OR PILON OR alison" | head -10`
   - Flag anything requiring action

5. **Cora email brief** (AI-triaged inbox summary):
   - Fetch the latest Cora brief: `gog gmail search "from:briefs@cora.computer" --max 1 | head -5`
   - Read the brief: `gog gmail read <ID>`
   - Cora sends briefs at ~8am and ~3pm (configurable). Surface the key stats: emails handled %, emails needing attention, emails archived
   - If Cora flagged emails needing attention > 0, list them
   - If no brief found in last 24h, skip silently

6. **Check cron logs** (overnight output):
   - Check `~/logs/cron-weather.log` and `~/logs/cron-capco.log` for recent entries
   - Note any failures or missing deliveries

7. **Check overnight OpenCode results** (two sources):
   - **Recurring queue:** Check `~/notes/opencode-runs/` for last night's run — read the most recent `summary.md` (by date folder). Report task count, pass/fail, and flag anything NEEDS_ATTENTION or CRITICAL.
   - **Ad-hoc queue:** Read `~/notes/WORKING.md` — look for `## Overnight Queue` section. If present, check each listed output file exists and isn't empty (`wc -l`). Report which arrived, which failed silently.
   - If neither has results, skip silently.

8. **Health scores** (from Oura Ring):
   - Run: `oura scores` (requires `OURA_TOKEN` in env — set in `~/.zshenv`)
   - Include the one-line output in the brief under "Health:"
   - If it fails or returns all `--`, skip silently (ring may not have synced)

9. **Weather** (action-oriented only):
   - `/hko` — focus on warnings (typhoon, rainstorm, extreme heat) and rain probability
   - Skip if already delivered by cron and no warnings active

10. **Things inbox drain** (mobile captures → TODO.md):
   - Run `python3 ~/scripts/things-drain.py`
   - If items were drained, include them in the brief under "Captured:" with a note to triage
   - If inbox empty, skip silently

11. **Overdue + today's deadlines** (quick scan, not full TODO review):
   - Read `~/notes/TODO.md`
   - Surface only: items with `due:` <= today, items with `when:` <= today
   - Skip someday items, skip items due later this week
   - This is a reminder, not a restatement — daily's tomorrow preview already set expectations

12. **Friday nudge** — if today is Friday, append to the brief: "It's Friday — run `/weekly` this afternoon for your weekly review."

13. **Token budget nudge** (Friday + Saturday only):
   - Skip if not Friday or Saturday
   - Run: `ccusage daily -s $(date -v-6d +%Y%m%d)` to get this week's consumption
   - Compare total against ~$1,050 weekly cap (Max20)
   - If >20% remains (~$210+), nudge: "~$X remaining before Saturday 8pm reset — burn it or lose it."
   - If <20% remains, skip silently — already well-utilized
   - Saturday: also note approximate hours until reset (resets ~8pm HKT)

13. **Deliver the brief** — concise, no filler:

## Output Format

```
**Tuesday, February 12, 2026**

Health:
- Sleep 82  Readiness 79  Activity 91 [or omit if unavailable]

Overnight:
- [New messages, cron results, or "Quiet night."]

Inbox (Cora):
- [Stats from latest brief, or omit if no brief]

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
