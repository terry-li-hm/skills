---
name: retro
description: End-of-session retrospective. Scan for non-obvious learnings worth capturing.
user_invocable: true
---

# Retro

Quick cleanup sweep at end of session — catch what "Compound As You Go" missed.

## Triggers

- "retro", "wrap up", "let's wrap"
- "what did we learn"
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

## Workflow

1. Quick scan of conversation
2. If nothing non-obvious → "Nothing to capture, we're good"
3. If something surfaces → update MEMORY.md (`~/.claude/projects/-Users-terry/memory/MEMORY.md`) or today's daily note
4. Done. No ceremony.

## Output

If something found:
```
**Retro:**
- [Learning] → added to MEMORY.md
```

If nothing:
```
Nothing non-obvious this session. ✓
```

## Notes

- This is a sweep, not a ritual
- Obvious corrections should've been captured on-the-fly
- Focus on patterns and implicit signals
