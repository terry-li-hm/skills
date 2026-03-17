---
name: prospective
description: Context-triggered reminders — check at session start and when entering a matching context. NOT a user-invokable command — this is an internal agent procedure. Consult when starting a session, entering a project directory, or before a skill that has pending reminders.
user_invocable: false
---

# Prospective Memory

*"When X happens, remember Y."* Temporary, context-triggered reminders that expire after actioning.

Unlike skills (permanent, pattern-based) or MEMORY.md (unconditional, always loaded), prospective memories fire once when a matching context arises, then get deleted.

## File

`~/.claude/projects/-Users-terry/memory/prospective.md`

## When to Check

- **Session start** — after reading NOW.md, scan prospective.md for any WHEN that matches current context
- **Entering a project** — grep for the project name in WHEN clauses
- **Before a skill fires** — if the skill name appears in a WHEN clause, surface the reminder

## When to Write

- After deferring an action to "next time" — capture it as WHEN/THEN instead of relying on memory
- When a session produces a follow-up that can't be done now
- When `/legatum` identifies loose ends

## Format

```markdown
- WHEN: <trigger context> → THEN: <action> (added: YYYY-MM-DD)
```

## Lifecycle

1. **Created** during session (legatum, manual, or when deferring work)
2. **Fires** when context matches (session start, project entry, skill invocation)
3. **Actioned** — do the thing
4. **Deleted** — remove the entry from prospective.md

Entries older than 30 days without firing should be reviewed in `/weekly` — either the context never arose (delete) or the trigger was too narrow (rewrite).

## Gotchas

- This is NOT a TODO list. TODOs have deadlines. Prospective memories have contexts.
- Don't duplicate what Due/moneo handles (time-triggered reminders).
- Keep entries short — one line per reminder. If it needs explanation, it's a TODO or a vault note.
