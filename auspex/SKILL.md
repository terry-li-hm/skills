---
name: auspex
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
   - **SmarTone bill:** If a SmarTone statement appears, extract the QR code payment link from the raw email HTML (`gog gmail get <id> --plain`) — look for `QRCodeGenServlet` href and surface as a clickable link with amount and due date.

5. **Cora inbox triage** — **MUST fetch from website, not just email. Email is summary only.**
   - Get today's brief ID: `gog gmail search "from:briefs@cora.computer newer_than:12h" --max 1 --plain`
   - **REQUIRED: Fetch full brief from Cora website** (email only has handled % and category counts — website has the actual action items, payment details, and flagged emails):
     ```
     AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile" agent-browser open "https://cora.computer/14910/briefs?date=<YYYY-MM-DD>&time=morning" \
       && agent-browser wait --load networkidle \
       && AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile" agent-browser eval "document.querySelector('main')?.innerText"
     ```
   - Only fall back to `gog gmail get <id> --plain` if agent-browser fails.
   - Action items: `gog gmail search "label:Cora/Action newer_than:12h" --max 5 --plain`
   - If any action/response items found, list them
   - If no brief and no flagged items, skip silently

6. **Check cron logs** (overnight output):
   - Check `~/logs/` for any cron job failures (oghma, opencode-nightly, vault-backup, etc.)
   - Note any failures or missing deliveries; skip if all clean

7. **Check overnight OpenCode results:**
   - Check `~/notes/opencode-runs/` for last night's run — read the most recent `summary.md` (by date folder). Report task count, pass/fail, and flag anything NEEDS_ATTENTION or CRITICAL.
   - If no results, skip silently.

8. **Health scores** (from Oura Ring):
   - Run: `oura scores` (requires `OURA_TOKEN` in env — set in `~/.zshenv`)
   - Include the one-line output in the brief under "Health:"
   - If it fails or returns all `--`, skip silently (ring may not have synced)

9. **Weather**:
   - Fetch and build the weather line: `caelum` (Rust CLI — fetches fresh from HKO, no pre-caching needed)
   - Always include in the brief
   - **Send to Tara**: compose a friendly prose weather note (2–3 sentences max). One lead weather emoji only + umbrella ☂️ if rain likely — no other inline emojis. Include temp range, key conditions, and anything actionable. Then send: `~/scripts/imessage.sh "<composed message>"`. Log "Weather sent to Tara ✓" in the brief.
   - If imessage.sh fails (non-zero exit), note "Weather send to Tara failed" — don't retry.

10. **Today's plate** — delegate to kairos:
   - Run kairos's steps (date, calendar, NOW.md, TODO scan) to gather the situational context.
   - Use those findings — calendar events, open gates, overdue items — to close the brief in auspex's morning voice. Don't paste kairos's output; reframe the facts for the morning narrative.
   - Don't re-run calendar or NOW.md independently — kairos owns that logic.

11. **Capco countdown + daily intel** (until start date):
   - Run `date` to calculate days remaining until Capco start (Apr 8, 2026 — or Mar 16 if buyout confirmed; check `~/notes/Capco/Capco Transition.md` for current date)
   - **Pick today's prep item** — rotate through topics by day-of-week (Mon: Capco methodology, Tue: client knowledge, Wed: AI governance frameworks, Thu: HK regulatory landscape, Fri: personal brand/intro pitch). One specific, 15-minute-doable item.
   - **Quick intel sweep** — 2–3 targeted searches:
     - "Capco HK news" or "Capco Asia fintech" (past week)
     - "HKMA AI banking announcement" (past week)
     - One competitor signal: Accenture/EY/KPMG/Deloitte APAC financial services AI
   - Surface: one key signal (1–2 sentences) + one talking point for client conversations
   - Skip the sweep if no results worth noting — don't pad
   - Weave countdown, prep item, and intel naturally into the brief — no separate section

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
- For ad-hoc mid-session priority checks later in the day, `/kairos`.

## Calls
- `kairos` — today's plate (calendar, NOW.md, overdue TODOs)
