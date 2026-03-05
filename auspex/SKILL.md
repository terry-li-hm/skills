---
name: auspex
description: Wake-up brief — Oura scores, weather, today's calendar, overnight urgent emails. Run when you wake up. Invoke with /auspex.
user_invocable: true
---

# Wake-Up Brief

A 60-second brief for the moment you wake up. What's the weather, how did you sleep, what's on today, anything urgent overnight? That's it — work priorities and planning belong to `/statio` when you sit down.

## Triggers

- `/auspex` (user-invocable only)

## Steps

1. **Get today's date and day of week**

2. **Weather**:
   - Run: `caelum`
   - Always include in the brief
   - **Send to Tara**: compose a friendly prose weather note (2–3 sentences max). One lead weather emoji only + umbrella ☂️ if rain likely — no other inline emojis. Include temp range, key conditions, anything actionable. Send: `~/scripts/imessage.sh "<composed message>"`. Log "Weather sent to Tara ✓".
   - If imessage.sh fails (non-zero exit or "compose window" fallback), note "Weather send to Tara failed" — don't retry.
   - If `caelum` fails, note "Weather unavailable" and continue.

4. **Today's calendar** — what's actually on today:
   - Run: `fasti list` (or `gog calendar list` if fasti unavailable)
   - List events with times. Flag anything before 10am that requires prep.

5. **Overnight urgent emails** — a narrow scan only:
   - Run: `gog gmail search "capco OR PILON OR alison OR urgent" | head -5`
   - If gog fails (keychain locked): note "Gmail unavailable — unlock keychain" and skip.
   - Surface only emails that require action today. Skip FYI/newsletters/receipts.
   - SmarTone bill: if it appears, extract the QR payment link from raw HTML (`gog gmail get <id> --plain`) and surface with amount + due date.

6. **Deliver the brief** — two short paragraphs max:

## Output

Weather, then today's calendar. That's the whole brief.

**Example:**

> **Thursday, 5 March 2026**
>
> Mainly cloudy, 16–21°C, light rain early then sunny intervals. Weather sent to Tara ✓
>
> Today: lunch with Tara at 12:15, physio at 16:00.

Skip empty sections entirely. If nothing urgent overnight, one sentence saying so. Keep it short enough to read while still in bed.

## Boundaries

- Do NOT surface work priorities, NOW.md gates, or task queues — that's `/statio`
- Do NOT triage full inbox — narrow overnight scan only
- Do NOT run Capco intel, GARP check, or token budget — those belong in `/statio`
- Do NOT create or edit vault notes

## See also
- `/statio` — start-of-work brief (priorities, gates, prep items)
- `/kairos` — ad-hoc situational snapshot any time of day
