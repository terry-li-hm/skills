---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, then capture non-obvious learnings.
user_invocable: true
---

# Wrap

End-of-session wrap-up — TODO sweep, session log, then catch what "Compound As You Go" missed.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "retro", "what did we learn"
- End of long/meaty session

## When to Skip

- Session was trivial (quick questions, nothing complex)
- Already captured learnings during the session
- User seems done, don't force it

## What to Look For

Scan for **non-obvious** stuff only:

| Type | Signal |
|------|--------|
| **Patterns** | Same issue came up 3 times — that's a pattern |
| **Implicit preferences** | Terry kept choosing X over Y — preference? |
| **Hidden friction** | Something took 4 attempts — why? |
| **Surprising wins** | That worked way better than expected — why? |
| **Mistakes I missed** | Wrong assumption I didn't notice until now |
| **Tool gotchas** | API quirk, config trap, undocumented behaviour |

## Workflow

1. **TODO sweep** — FIRST, before anything else. Check if anything done this session should be marked in `~/notes/TODO.md`. This is mechanical and must not be skipped.
2. **Session log** — append a summary block to today's daily note (`~/notes/YYYY-MM-DD.md`)
3. Quick scan of conversation for non-obvious learnings
4. If nothing non-obvious → "Nothing to capture, we're good"
5. If something surfaces → **dedup**, **route**, and optionally **promote**
6. Done. No ceremony.

### Step 1: TODO Sweep

Scan conversation for completed actions that match open items in `~/notes/TODO.md`:
- Messages sent, forms submitted, tasks finished → mark `[x]` with brief note
- New commitments or deadlines mentioned → add as new TODO items
- Keep it fast — skim for verbs like "sent", "done", "submitted", "ordered", "confirmed"
- If nothing matches, skip silently

### Step 2: Session Log

Append a session summary to today's daily note under `## Activity`. Create the file if it doesn't exist. Each entry is a block, not a one-liner:

```markdown
### HH:MM–HH:MM — [Brief title]
- What was accomplished
- Key decisions made or options explored
- Blockers hit, friction points
- What's left unfinished (if anything)
```

This feeds `/daily` — by EOD the note is already populated. Write with enough detail that Terry can reflect on whether the time was well spent. Don't editorialize ("productive session!") — just log what happened.

### Step 3a: Dedup

Before writing anything, `oghma_search` for the insight (keyword mode, 3 results). If already captured with same substance, skip it — just mention "already in Oghma" in output.

### Step 3b: Route by Type

Don't dump everything into MEMORY.md. Route to the store that fits:

| Type | Destination |
|------|-------------|
| Tool gotcha / how-to | `~/docs/solutions/` (learnings-researcher queryable) |
| Workflow preference | `~/notes/Learnings Inbox.md` (or relevant vault note if one exists) |
| Cross-session agent context | MEMORY.md (`~/.claude/projects/-Users-terry/memory/MEMORY.md`) |
| General insight | `~/notes/Learnings Inbox.md` |
| Activity-specific | Today's daily note |

For `~/docs/solutions/`, create a simple markdown file in the appropriate category subdirectory. No YAML schema required — keep it lightweight. Just the gotcha, why it happens, and the fix.

### Step 3c: Pattern Promotion

If an insight matches something already in Oghma (dedup search returned a hit with similar theme), flag it:

> "This keeps coming up — worth promoting to MEMORY.md?"

Only suggest, never auto-promote. Terry decides.

## Output

**Write first, then summarise.** Route each finding to its destination (MEMORY.md, Learnings Inbox, solutions, daily note) — then print the summary so Terry sees what was captured and where.

If something found:
```
**Wrap:**
- [Learning] → saved to [destination + path]
- [Learning] → already in Oghma, skipped
```

If nothing:
```
Nothing non-obvious this session.
```

## Notes

- This is a sweep, not a ritual — 30 seconds, not 3 minutes
- Obvious corrections should've been captured on-the-fly
- Focus on patterns and implicit signals
- One insight well-routed beats five dumped in the same file
