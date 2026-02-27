---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, NOW.md, learnings safety net.
user_invocable: true
---

# Wrap

End-of-session wrap-up. Three mechanical steps + a conditional meta-sweep.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "what did we learn"
- End of long/meaty session

## Workflow

Execute in order. Don't skip earlier steps if a later one seems more interesting.

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Three scans:

**Complete:** Done actions → mark `[x]` with brief note and `done:YYYY-MM-DD`. Hard test: truly done, or just "dev done"? If it needs testing, pushing, or confirmation — stays open with updated status.

**Create:** New commitments, deadlines, or interrupted WIP → add as items. Must have a verb and a concrete next action — "look into X" is not a TODO. Tag with `agent:` if Claude can resume it.

**Abandoned:** Did we go down a path, abandon it, and never record why? Add a one-liner to the session log: `- Abandoned X because Y`. Prevents the next session from rediscovering the same dead end.

Skip silently if nothing matches.

### Step 2: Session Log

Append to `~/notes/Daily/YYYY-MM-DD.md` (create if needed):

```markdown
### HH:MM–HH:MM — [Brief title]
- Key outcome or decision (1-3 bullets max)
- Link to vault note if detail exists: see [[Note Name]]
```

2-3 bullets. No implementation details — those belong in vault notes or `~/docs/solutions/`.

### Step 3: NOW.md + Project Trackers

**NOW.md** (`~/notes/NOW.md`) — check `stat -f %m` first. If written <1h ago by another session, update only what changed. Otherwise, full overwrite. If session was light and NOW.md is still accurate, skip. Max 15 lines:

```markdown
# NOW
<!-- Max 15 lines. Full overwrite at each /wrap. Stale after 24h. -->

## Resume point
- [decided] Exact next step — with [[links]] to canonical notes
- [open] Options discussed but not yet chosen — see [[Note]]
```

Resume points must pass the cold-start test: could another session resume from this alone, without reading any conversation history? Use `[decided]` vs `[open]` to signal how settled each item is.

**Vault flush:** If the session advanced a project with a canonical tracker note (e.g. `[[Capco Transition]]`), update that note now. Context doesn't survive — if it's not in a file, it's lost.

### Step 4: Meta-Sweep (conditional)

**Skip entirely if** the session was routine. Do NOT invent learnings. A routine session producing nothing here is correct.

**If the session had substance,** one pass through three lenses:

1. **Safety net:** Uncaptured friction, corrections, or gotchas? Route to the most specific file: tool gotcha → `~/docs/solutions/`, cross-session context → MEMORY.md, skill workflow → the skill's SKILL.md. **Budget check:** If MEMORY.md > 150 lines, flag for trimming — demote provisionals to `~/docs/solutions/memory-overflow.md`.
2. **System evolution:** Should a skill be created or tightened? Hook added? Same mistake twice despite a rule → escalate per `~/docs/solutions/enforcement-ladder.md`. Hexis port? (Generic only.) Propose, don't auto-implement.
3. **Generalization:** Does any learning apply beyond where it was routed? Instance → pattern → principle. Most don't. If nothing generalizes, move on.

One pass, all three lenses. If nothing surfaces, skip silently.

## Output

**Write first, then summarise.** All file writes must complete before the bordered output appears.

Use the bordered format below. Prose (not bullets or labels) forces linear reading. The border makes wrap visually distinct from tool output.

**Length scales with session complexity:**
- Light session (Q&A, one task): 2-3 sentences
- Normal session: 3-4 sentences
- Heavy session (multi-project, decisions, friction): 4-6 sentences

Cover only what applies — don't pad:
1. The arc (what happened)
2. What's unfinished or staged
3. Vault changes (weave in, don't list)
4. Learnings captured (only if something was)

Handoff note to tomorrow-you, not a build log. Implementation details belong in vault notes, not here.

**Format:**

```
─── Wrap ───────────────────────────────────────

STR relabelling: from WIP to cold-start handover package. Handover doc drafted, 34 scripts committed with README, CDSW dry run passed. Pipeline test gist staged for the next window.

─────────────────────────────────────────────────
```

**Do NOT hard-wrap the prose.** Let the terminal handle line wrapping naturally.

## Notes

- Sweep, not ritual — 30 seconds, not 3 minutes
- One insight well-routed beats five dumped in the same file
