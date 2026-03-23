---
name: actin
description: Manage Praxis.md in the vault with time-based scheduling. Use when user says "todo", "add todo", "check todo", "done with", "overdue", "someday", or "actin".
user_invocable: true
---

# Praxis

Quick management of `~/notes/Praxis.md` with time-based scheduling.

## Commands

Invoke via `todo-cli <subcommand>`. Subcommands: `today`, `upcoming`, `overdue`, `someday`, `all`, `spare`, `stats`, `clean`. Present CLI output directly.

If `~/notes/Praxis.md` is missing, create it with a minimal heading before running any command. If creation fails, report "TODO store unavailable" and stop.

## Intake Gate (apply before `/actin add`)

| Test | Question | If NO → |
|------|----------|---------|
| **Irreversible** | If I miss this, is the consequence irreversible? | Lean skip |
| **Committed** | Has someone external been told this will happen? | Lean skip |
| **Natural recall** | Will I naturally remember this without a prompt? | If YES → skip |
| **Attention cost** | Does tracking this displace focus from higher-stakes items? | If YES → skip |

Pass 1 or 2 → add. Fail both but pass 3+4 → skip. Borderline → ask Terry rather than defaulting to add.

Append cleared tasks with: `echo "- [ ] <task>" >> ~/notes/Praxis.md`

## Due Alarm (moneo)

When adding a task with `due:` within 7 days, also set a phone alarm:

```bash
moneo add --date YYYY-MM-DD "<task title>"
```

Bar for `due:` at all: would forgetting cause real damage? Low-stakes admin belongs in TODO only — not Due. Pick a deliberate time, not just 9am default.

## Hard Rules

- **NEVER leave `- [x]` lines in Praxis.md.** When marking done — via `/actin done` or manually — move the completed line to `~/notes/Praxis Archive.md` in the same edit. Archive under current month's section (`## March 2026`), creating it if absent. No exceptions, no "clean up later".
- **Reflections/journaling items live in `~/notes/Reflections Queue.md`** — not Praxis.md.
- Single source: `~/notes/Praxis.md`. All agents share this file.
- Dates always ISO-8601 (`YYYY-MM-DD`) in HKT. Use `date +%Y-%m-%d` for today.
- Do NOT reinterpret task intent or create project plans — this skill manages TODO state only.
