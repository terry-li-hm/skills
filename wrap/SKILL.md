---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, then capture non-obvious learnings.
user_invocable: true
---

# Wrap

End-of-session wrap-up — TODO sweep, session log, then catch what "Compound As You Go" missed.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "what did we learn"
- End of long/meaty session

## What to Look For

Answer these questions honestly during the scan. If any answer is yes, there's a learning to capture:

1. **Did I retry anything?** Multiple attempts at the same thing = friction worth documenting
2. **Did Terry correct me?** Correction = wrong assumption or missing context
3. **Did a tool behave unexpectedly?** API quirk, config trap, undocumented behaviour
4. **Did something work surprisingly well?** Worth noting what made it work
5. **Did the same issue come up more than once?** Repetition = pattern
6. **Did Terry choose X over Y without explaining?** Implicit preference worth capturing

## Workflow

1. **TODO sweep** — FIRST, before anything else. Check if anything done this session should be marked in `~/notes/TODO.md`. This is mechanical and must not be skipped.
2. **Session log** — ALWAYS append a summary block to today's daily note (`~/notes/Daily/YYYY-MM-DD.md`). Never skip this step, even for short sessions — a 1-line entry is fine.
3. **WORKING.md cleanup** — Read `~/notes/WORKING.md`. Flush anything useful (status changes, unfinished state) to the appropriate vault file or TODO. Then clear the file to a clean slate (`# Working\n\nNo active work.`). Skip if already clean.
4. **Learnings scan** — Run through the six questions in "What to Look For" **internally** (do not print them). If the session was ≤3 turns of simple Q&A with no corrections or retries, skip to done. Otherwise, you must answer the six questions before concluding there's nothing to capture.
5. If something surfaces → **dedup**, **route**, and optionally **promote**
6. Done. No ceremony.

### Step 1: TODO Sweep

Scan conversation for completed actions that match open items in `~/notes/TODO.md`:
- Messages sent, forms submitted, tasks finished → mark `[x]` with brief note
- New commitments or deadlines mentioned → add as new TODO items
- **WIP that got interrupted** → add TODO for the remaining work (with `agent:` tag if Claude can do it). If state is complex, ensure WORKING.md has resume instructions and TODO points there.
- Keep it fast — skim for verbs like "sent", "done", "submitted", "ordered", "confirmed"
- If nothing matches, skip silently

### Step 2: Session Log

Append a session summary to today's daily note (`~/notes/Daily/YYYY-MM-DD.md`). Create the file if it doesn't exist. Each entry is a **concise** block — key points only, with `[[interlinks]]` to vault notes where detail lives.

```markdown
### HH:MM–HH:MM — [Brief title]
- Key outcome or decision (1-3 bullets max)
- Link to vault note if detail exists: see [[Note Name]]
- What's left unfinished (if anything)
```

**Keep it tight.** 2-3 bullets per block. Implementation details (CLI flags, iteration counts, error specifics) belong in vault notes or `~/docs/solutions/`, not the daily log. The daily note answers "what did I do and what matters" at a glance — not a session replay.

This feeds `/daily` — by EOD the note is already populated. Don't editorialize ("productive session!") — just log what happened.

### Step 3: WORKING.md Cleanup

Read `~/notes/WORKING.md`. Three outcomes:
- **Status changes** (pipeline moves, completed items, decisions) → flush to the relevant vault file (TODO.md, project note, daily note)
- **WIP context** (half-finished tasks, resume instructions) → leave in place if work continues next session; otherwise move to TODO with enough context to resume
- **Stale/empty** → clear to `# Working\n\nNo active work.`

This prevents the #1 source of stale morning briefings: status changes trapped in WORKING.md that never made it to vault.

### Step 4a: Dedup

Before writing anything, `oghma search "<insight>" --mode keyword --limit 3`. If already captured with same substance, skip it — just mention "already in Oghma" in output.

### Step 4b: Route by Type

Don't dump everything into MEMORY.md. Route to the store that fits:

| Type | Destination |
|------|-------------|
| Tool gotcha / how-to | `~/docs/solutions/` (learnings-researcher queryable) |
| Workflow preference | Relevant vault note, or today's daily note if no note exists |
| Cross-session agent context | MEMORY.md (`~/.claude/projects/-Users-terry/memory/MEMORY.md`) |
| General insight | Relevant vault note, or `~/docs/solutions/` |
| Activity-specific | Today's daily note |

For `~/docs/solutions/`, create a simple markdown file in the appropriate category subdirectory. No YAML schema required — keep it lightweight. Just the gotcha, why it happens, and the fix.

**No staging area.** Route directly to the final destination. If you genuinely don't know where something belongs, put it in today's daily note — `/daily` will catch it.

### Step 4c: Pattern Promotion

If an insight matches something already in Oghma (dedup search returned a hit with similar theme), flag it:

> "This keeps coming up — worth promoting to MEMORY.md?"

Only suggest, never auto-promote. Terry decides.

## Output

**Write first, then summarise.** Route each finding to its destination, then print one compact block. The six questions are internal reasoning — never print them.

**Format — always this structure:**

```
**Wrap:**
TODO: [no changes | N items updated] · Daily: [appended → YYYY-MM-DD.md | created] · WORKING: [clean | N items updated | cleared]
💡 [one-line insight] → [destination path]
💡 [one-line insight] → already in Oghma, skipped
```

The first line (mechanical steps) is always present — confirms the steps ran. Learnings lines only appear if something was captured. If nothing:

```
**Wrap:**
TODO: no changes · Daily: appended → YYYY-MM-DD.md · WORKING: clean
No learnings — clean session.
```

Short sessions (≤3 turns):

```
**Wrap:**
TODO: no changes · Daily: appended → YYYY-MM-DD.md · WORKING: clean
```

## Notes

- This is a sweep, not a ritual — 30 seconds, not 3 minutes
- Obvious corrections should've been captured on-the-fly
- Focus on patterns and implicit signals
- One insight well-routed beats five dumped in the same file
