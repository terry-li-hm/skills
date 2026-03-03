---
name: kairos
description: "Any-time situational snapshot — what's actionable right now. Use when user says 'kairos', 'what now', 'what should I do', 'what's next', or needs a mid-session priority check."
user_invocable: true
triggers:
  - kairos
  - what now
  - what should I do
  - what's next
  - what do I do
  - priority check
---

# Kairos — The Opportune Moment

*Kairos* (Greek: καιρός) — qualitative time, not clock time. Not "what time is it?" but "given this moment, what's the right action?"

Unlike `auspex` (morning delta) or `cardo` (midday reflection), Kairos is stateless and anytime. No session scanning, no reflection on what shipped — just the live situation and what to do next.

## Triggers

- "kairos"
- "what now"
- "what should I do"
- "what's next"
- "priority check"

## Steps

Run steps 1–4 in parallel.

### 1. Get current time + day

```bash
date
```

Note: day of week, time of day (HKT), proximity to end of day.

### 2. Today's calendar — what's coming

```bash
gog calendar list
```

- Extract remaining events for today
- Flag: anything within the next 60 minutes (needs prep or wrap-up now)
- Flag: anything within 2–4 hours (good to know)
- If nothing remaining, note "calendar clear"

### 3. Active decisions and gates — NOW.md

Read `~/notes/NOW.md`.

- Pull any open decisions (not yet `[decided]` or `[done]`)
- Pull any active processes or waiting-on states
- If a PID is mentioned, skip process check — too slow for a quick snapshot

### 4. Overdue and today's TODO items

Read `~/notes/TODO.md`.

- Surface only: items with `due:` <= today, items with `when:` <= today that are not completed
- Skip `someday` items, skip items due later in the week
- Max 5 items — if more qualify, pick the most time-sensitive

### 5. Synthesise — time-aware routing

Based on current time and what was found:

**Pre-meeting (< 45 min to next calendar event):**
→ Lead with the upcoming event. Surface any prep items. Keep it brief — they're about to be in a meeting.

**Post-meeting block (event ended < 30 min ago):**
→ Flag follow-up capture: "Just finished X — anything to log or action from that?"

**Free block (no meeting for 2+ hours):**
→ Surface top 1–2 priorities from NOW.md + overdue TODO. Concrete, doable.

**Late afternoon (after 5pm HKT) or pre-EOD:**
→ Flag EOD proximity: "< N hours left — what needs wrapping before you close?"

**No context to surface:**
→ Say so plainly: "Calendar clear, nothing overdue, no open gates in NOW.md — you've got a clean slate." Then offer: "Want me to check inbox or surface low-energy tasks?"

## Output

One short paragraph. No headers, no bullets unless there are 3+ overdue items. Lead with time context, close with the clearest next action.

**Example outputs:**

> **3:15pm Tuesday** — Meeting-free until 5pm. One open gate in NOW.md: the Lacuna Railway deployment (waiting on Terry to test the new endpoint). Two overdue: school research checklist (since Feb 28), SmarTone bill. The deployment test is the sharpest thing — 20 minutes to close that loop.

> **10:45am Wednesday** — Standup in 12 minutes. After that you're free until 2pm. Nothing in NOW.md flagged as urgent. Clean slate post-standup.

> **6:20pm Thursday** — EOD in sight. Two open decisions in NOW.md: Capco start date (waiting on Gavin) and lucus Phase 2 design. Neither is closeable today — flag both in daily note and call it. One overdue TODO: AXA insurance form (since Mar 1).

## Notes

- Do NOT scan anam/session history — that's cardo's job. Kairos is forward-looking.
- Do NOT reflect on what was shipped this session. Pure situational read.
- If keychain is locked and gog fails, note it and skip calendar gracefully.
- Keep it under 5 sentences. The point is to decide and move, not to read a report.
- If the user just ran `auspex` or `cardo` recently (same session), skip NOW.md/TODO repeat and just surface what's changed: new calendar events or new open gates since then.
