---
name: auspex
description: Morning weather check — sends weather to Tara via iMessage. Optional, run if time before Theo's school rush. Invoke with /auspex.
user_invocable: true
disable-model-invocation: true
---

# Morning Weather

Weather + send to Tara. That's it.

## Triggers

- auspex
- gm
- weather
- morning weather
- send tara weather

## Steps

1. Run: `auspex` (CLI at `~/bin/auspex`, source `~/code/auspex/`)
   - Sends weather to Tara via iMessage automatically
   - Use `auspex --no-send` to skip the iMessage (testing)

2. Present the weather output.

## Boundaries

- Do NOT surface work priorities, TODO, calendar, or inbox — that's `/commute` (evening) or `/kairos` (ad-hoc)
- Do NOT check nightly reports, overnight results, or system health
- Do NOT create or edit vault notes

## See also
- `/commute` — the one daily routine (evening)
- `/kairos` — ad-hoc "what now?" (anytime)
