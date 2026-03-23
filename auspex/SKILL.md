---
name: zeitgeber
description: Morning brief — weather, sleep scores, overnight results. Optional, run if time before Theo's school rush. "zeitgeber", "gm", "weather", "how did I sleep"
user_invocable: true
disable-model-invocation: true
---

# Morning Brief

Weather, sleep, overnight results. 60 seconds, phone-friendly. Optional — skip if Theo's school rush takes over.

## Triggers

- zeitgeber
- gm
- weather
- how did i sleep
- morning
- sleep score

## Steps

Run all in parallel:

1. **Weather + Tara** — `zeitgeber` CLI (sends weather to Tara via iMessage automatically)
   - Use `zeitgeber --no-send` to skip iMessage (testing)

2. **Sleep & health scores** — `sopor today`
   - Shows last night's sleep: Oura sleep score, readiness, HRV, EightSleep data
   - If readiness <65, flag it: "Low readiness — consider an easier day"
   - If `sopor` fails or returns empty, skip silently

3. **Overnight results** — check both files, skip silently if missing or stale (>24h):
   - `~/.claude/nightly-health.md` — system health dashboard. Surface any warning or red rows. If all green, just say "System health: all green."
   - `~/.claude/skill-flywheel-daily.md` — skill routing misses. Surface any total misses or low hit rate.
   - Check `~/.cache/kinesin-runs/` for overnight agent results — read most recent `summary.md`. Flag NEEDS_ATTENTION or CRITICAL items. Skip silently if empty.

Present everything in one compact brief.

## Boundaries

- Do NOT surface work priorities, TODO, calendar, or inbox — that's `/commute` (evening) or `/ultradian` (ad-hoc)
- Do NOT create or edit vault notes
- Do NOT run Oura trend analysis — that's `/weekly` health section
- Keep it under 60 seconds of reading. Morning is for glancing, not studying.

## See also
- `/commute` — the one daily routine (evening)
- `/ultradian` — ad-hoc "what now?" (anytime)
- [[cadence-design]] — principles behind the cadence stack
