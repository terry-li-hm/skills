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
   - Run `stat -f '%Sm' -t '%Y-%m-%d' ~/notes/NOW.md ~/notes/Capco/Capco\ Transition.md ~/notes/TODO.md`
   - If any file's last-modified date is >24h old, flag it: "NOW.md last updated X — treat as stale"

3. **Yesterday's daily note** — quick glance:
   - Read `~/notes/Daily/YYYY-MM-DD.md` (yesterday)
   - Pull the `## Tomorrow` section if it exists — this is the plate preview from last night
   - Pull any `## Follow-ups` items — these are carryover
   - **Cross-reference against NOW.md `[decided]` entries before surfacing carryover items.** If a Tomorrow item is already resolved in NOW.md (as `[decided]` or `[done]`), skip it — don't re-surface as open. Also check today's daily note (if it exists — same-day earlier sessions may have resolved items before this session started).

4. **Overnight messages** (the core value of this skill):
   - Scan Gmail for Capco/HR emails (past 24h): `gog gmail search "capco OR PILON OR alison" | head -10`
   - If gog fails with "no TTY" / keyring error: keychain is locked. Note "Gmail unavailable — unlock keychain" and skip steps 4–5. Don't retry.
   - Flag anything requiring action

5. **Cora inbox triage** (read Cora's labels via Gmail — no website scraping):
   - Latest brief email: `gog gmail search "from:briefs@cora.computer newer_than:12h" --max 1 --plain`
     - If found, read it with `gog gmail get <id> --plain` — has headline stats (handled %, needs attention, archived)
   - Action items: `gog gmail search "label:Cora/Action newer_than:12h" --max 5 --plain`
   - Needs response: `gog gmail search "(label:✒️-Needs-Response OR label:✅-Todo OR label:⏰-Timely) newer_than:12h" --max 5 --plain`
   - If any action/response items found, list them
   - If no brief and no flagged items, skip silently

6. **Check cron logs** (overnight output):
   - Check `~/logs/` for any cron job failures (oghma, opencode-nightly, vault-backup, etc.)
   - Note any failures or missing deliveries; skip if all clean

7. **Check overnight OpenCode results:**
   - Check `~/notes/opencode-runs/` for last night's run — read the most recent `summary.md` (by date folder). Report task count, pass/fail, and flag anything NEEDS_ATTENTION or CRITICAL.
   - If no results, skip silently.

7b. **Read NOW.md** (`~/notes/NOW.md`):
   - Scan for running processes — check if PIDs are still alive (`ps -p <PID>`)
   - Note what was active last session — follow links to canonical project tracker notes for real context
   - If stale (>24h), mention it but don't rely on it

8. **Health scores** (from Oura Ring):
   - Run: `oura scores` (requires `OURA_TOKEN` in env — set in `~/.zshenv`)
   - Include the one-line output in the brief under "Health:"
   - If it fails or returns all `--`, skip silently (ring may not have synced)

9. **Weather**:
   - Fetch and build the weather line: run the three HKO curls, then `python3 ~/skills/hko/weather.py weather`
   - Always include in the brief
   - **Auto-send to Tara**: `~/scripts/imessage.sh "$(python3 ~/skills/hko/weather.py short)"` — send immediately, no confirmation needed. Log "Weather sent to Tara ✓" in the brief.
   - If imessage.sh fails (non-zero exit), note "Weather send to Tara failed" — don't retry.

10. **Today's calendar** (what's on the schedule):
   - Run: `gog calendar list` (NOT `gog calendar today` — that subcommand doesn't exist)
   - List events with times. Flag any that need prep (meetings, appointments)
   - If empty, skip silently

11. **Overdue + today's deadlines** (quick scan, not full TODO review):
   - Read `~/notes/TODO.md`
   - Surface only: items with `due:` <= today, items with `when:` <= today
   - Skip someday items, skip items due later this week
   - This is a reminder, not a restatement — daily's tomorrow preview already set expectations

12. **Capco countdown** (until start date):
   - Run `date` to calculate days remaining until Capco start (Apr 8, 2026 — or Mar 16 if buyout confirmed; check `~/notes/Capco/Capco Transition.md` for current date)
   - Show: "X days to Capco"
   - If `/capco-prep brief` hasn't been run recently (check `~/notes/Capco/.capco-drill-state.json` last_session date), nudge: "Run `/capco-prep brief` for today's prep item"
   - Weave the countdown naturally into the brief — don't make it a separate section

13. **GARP quiz check** (until Apr 4):
   - Run `~/scripts/rai.py stats 2>/dev/null | head -5` to get session count and phase
   - Check `.garp-fsrs-state.json` for any review dated today: `python3 -c "import json; d=json.load(open('$HOME/notes/.garp-fsrs-state.json')); today='$(date +%Y-%m-%d)'; print(sum(1 for e in d.get('review_log',[]) if e.get('date','').startswith(today)))"` — if >0, quiz already done today, skip
   - If no session today and schedule says one is due (cruise: 3x/week = Mon/Wed/Fri-ish), nudge: "GARP quiz due today"
   - If already done today, do NOT mention GARP quiz at all

14. **Friday nudge** — if today is Friday, append to the brief: "It's Friday — run `/weekly` this afternoon for your weekly review."

15. **Token budget nudge** (Friday + Saturday only):
   - Skip if not Friday or Saturday
   - Run: `ccusage daily -s $(date -v-6d +%Y%m%d)` to get this week's consumption
   - Compare total against ~$1,050 weekly cap (Max20)
   - If >20% remains (~$210+), nudge: "~$X remaining before Saturday 8pm reset — burn it or lose it."
   - If <20% remains, skip silently — already well-utilized
   - Saturday: also note approximate hours until reset (resets ~8pm HKT)

16. **Deliver the brief** — concise, no filler:

## Output

Write a short prose briefing under the date heading. Open with how you slept (if Oura data available), then what happened overnight — messages, cron results, Cora's inbox triage (from labels/brief email). If anything needs attention (weather warnings, staleness flags, overdue items), weave it in naturally. Close with what's on the plate today: calendar events, deadlines, and any carryover from yesterday's daily note.

Skip anything with nothing to report — don't mention empty sections. The brief should read like a colleague telling you what matters this morning, not a dashboard.

**Example:**

> **Tuesday, February 12, 2026**
>
> Solid night — sleep 82, readiness 79. Quiet overnight: Cora handled 91% of inbox, nothing flagged. One email from Gavin about background check docs — needs a reply this morning.
>
> Weather's fine, no warnings. You've got the dentist at 2:30pm and a GARP quiz due today. The STR handover doc is still waiting on Joel's signature — that's the main carry from yesterday.

## Notes

- This is a delta brief, not a full situational review. Daily already closed last night's loop.
- If yesterday had no daily note (skipped `/daily`), fall back to fuller review: include TODO scan + priority check from vault context files.
- Keep it to a short paragraph or two. The point is to start working, not to read a report.
