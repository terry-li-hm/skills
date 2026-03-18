---
name: auspex
description: Wake-up brief — weather, calendar, key deadlines today. Run when you wake up. Invoke with /auspex.
user_invocable: true
---

# Wake-Up Brief

A 60-second brief for the moment you wake up. Weather, what's on today, anything due today. That's it — work priorities belong to `/statio` when you sit down.

## Triggers

- `/auspex` (user-invocable only)

## Steps

1. Run: `auspex` (CLI at `~/bin/auspex`, source `~/code/auspex/`)
   - Runs all checks in parallel: weather (caelum), calendar (fasti), TODO deadlines, overnight results, acta teaser, missed emails (Cora blind spot)
   - Sends weather to Tara via iMessage automatically
   - Handles all failures gracefully — never crashes
   - Use `auspex --no-send` to skip the iMessage (testing)
   - Use `auspex --json` for structured output

2. Present the CLI output directly — it's already formatted for the brief.

3. If the missed email section shows results, flag them prominently — these are emails Cora received but never labelled (the failure mode that swallowed two interview invitations, Mar 2026).

4. **Nightly reports** — check both files, skip silently if missing or stale (>24h old):
   - `~/.claude/nightly-health.md` — system health dashboard. Surface any ⚠️ or 🔴 rows. If all ✅, just say "System health: all green."
   - `~/.claude/skill-flywheel-daily.md` — skill routing misses. Surface any total misses or low hit rate. If Haiku found missed triggers, propose the fixes inline.

## Boundaries

- Do NOT surface work priorities, NOW.md gates, or full task queues — that's `/statio`
- Do NOT check inbox beyond what the CLI surfaces — no Cora
- Do NOT run Oura, Capco intel, GARP, or token budget — those belong in `/statio`
- Do NOT create or edit vault notes

## See also
- `/statio` — start-of-work brief (Oura, priorities, gates, prep items)
- `/kairos` — ad-hoc situational snapshot any time of day
