---
name: scrinium
description: Route captured knowledge to the right storage layer — MEMORY.md, CLAUDE.md, docs/solutions/, vault, or skill. Consult before writing any persistent note or memory.
user_invocable: false
---

# Scrinium — Knowledge Routing

When capturing a lesson, correction, or discovery, route it here first.

## Decision Table

| What is it? | Where |
|-------------|-------|
| Hard rule / prohibition ("never do X") | `CLAUDE.md` |
| Recurring gotcha / tool quirk (one-liner) | `MEMORY.md` (with encoding context: why it exists) |
| **Exception to a skill's normal behavior** | **The skill itself** (Gotchas section) — store only the deviation, not the whole pattern |
| How-to / workflow with steps | `~/docs/solutions/` |
| Changes *how to act* next time | Skill (update or create) |
| Temporary "next time X, do Y" | `memory/prospective.md` (expires when actioned) |
| Reference / background context | Vault note |
| One-off correction, not generalizable | Daily note only |

## The One-Sentence Test

Can the lesson be stated in one sentence? → `MEMORY.md` bullet.
Does it have a trigger + multiple steps or variants? → Skill.
Is it rationale or research? → `~/docs/solutions/` or vault.
Does it change a standing rule? → `CLAUDE.md`.

## Skill vs MEMORY.md

**Skill** when the lesson changes *how to act* — it fires automatically next time via the trigger.
**MEMORY.md** when it's a fact or gotcha that informs judgment but doesn't prescribe steps.

If in doubt: skill holds the rule, docs holds the *why*. Non-exclusive.

**Gate before writing to MEMORY.md:** Ask — "does an existing skill own this behaviour?" If yes, update the skill instead. MEMORY.md is the last resort, not the default capture target. Writing to MEMORY.md without checking skills first is a miss.

## CLAUDE.md Rules

- Rules only — no time-sensitive facts (dates, status, amounts).
- Facts age fast; rules age slowly. Any fact → replace with a vault pointer.
- Hard rules go here; soft guidance goes in a skill where it can evolve.

## MEMORY.md Budget

- ~150 lines hard limit (content beyond line 200 silently dropped).
- One-liners only. If it needs more than one line, it belongs in `~/docs/solutions/`.
- After writing: ask "is this hook-able?" — mechanical rules should be enforced, not just documented.

## docs/solutions/ Conventions

- Use typed IDs: `ERR-YYYYMMDD-NNN` (tool failure), `LRN-YYYYMMDD-NNN` (correction), `REQ-YYYYMMDD-NNN` (feature).
- Dedup before writing: `ls ~/docs/solutions/ | grep -i <topic>` first.
- Operational how-tos → `~/docs/solutions/operational/`.
- Save research *before* acting on it — findings first, then action.

## Principles (accumulate here over time)

- **Skill > docs for behavioural lessons.** If it changes how to act → skill. If it's context → docs. **If a relevant skill already exists, update it directly — don't create an intermediate feedback memory that restates a skill rule.**
- **One-off corrections stay in the daily note.** Don't inflate MEMORY.md with single incidents.
- **MEMORY.md ≠ notebook.** Reference data (passwords, specs, account numbers) → vault.
- **Blink Shell config questions → search online first.** Its shell is non-standard; aliases don't work. Full setup: `~/docs/solutions/blink-shell-setup.md`.
