---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, NOW.md, learnings safety net.
user_invocable: true
---

# Wrap

End-of-session wrap-up. Pre-wrap check + mechanical steps + learning capture.

Session scope = files modified + tool calls + conversation turns since this session began.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "what did we learn"
- End of long/meaty session

## Workflow

### Skip gate

```bash
now-age
```
If NOW.md is **<15 minutes old** AND user did not explicitly invoke `/wrap`, skip to Step 4 briefly, then Output. Explicit `/wrap` always runs all steps.

### Step 0: Pre-Wrap Check

Run `prewrap` and answer these five questions. Complete blocking actions (garden post, arsenal) *before* outputting the block — the block is a receipt, not a plan.

```bash
prewrap
peira status 2>/dev/null || true
```

**Questions (explicit yes/no for Q4–5, silence is not "no"):**
1. **Unverified?** Any tool output this session that wasn't checked?
2. **Deferred?** Anything mentioned as "later/next/TODO" not yet captured? → add to TODO.md
3. **Uncommitted?** Dirty repos *touched this session*? → offer to commit (leave other repos alone)
4. **Garden post?** Non-obvious insight, clear thesis, Terry's lane, no unverified facts? If yes → `sarcio new "Title"` → write → judge → `sarcio publish <slug> --push` now. "Yes" is not a terminal state — resolve to `drafted → <slug>` or `no — [reason]`.
5. **Consulting arsenal?** Anything concretely applicable to a bank/client AI engagement? If yes → add bullet to `[[Capco Transition]]` now.

**CLAUDE.md modified?** One-line tightening check: does it belong in CLAUDE.md or in a skill / MEMORY.md / `~/docs/solutions/`?

**Background dispatches** — fire with `run_in_background: true` when the session touched the relevant area:

| Audit | When |
|-------|------|
| MEMORY.md hook coverage | MEMORY.md modified AND <145 lines |
| Skill staleness | Any skill edited or added |
| Solutions KB dedup | `~/docs/solutions/` modified |
| Vault orphan links (nexis) | Monthly only |

**Output — light or full:**

If all checks clean and no blocking actions: `✓ Clean — [prewrap summary]. Garden: no — [reason]. Arsenal: no — [reason].`

Otherwise, full block:
```
─── Pre-Wrap ────────────────────────────────────
⚠  [only if action needed]
→  Deferred: [items or "none"]
✓  [clean checks summary]
Garden post: drafted → <slug> | no — [reason]
Arsenal:     added → [[Capco Transition]] | no — [reason]
Dispatched:  <audit> (<task-id>) | none
─────────────────────────────────────────────────
```

Then proceed to Steps 1–4.

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Skip if missing.

- **Complete:** Done items → `[x]` with note and `done:YYYY-MM-DD`. Hard test: truly done, or just "dev done"? Move checked items to `~/notes/TODO Archive.md`.
- **Create:** New commitments or interrupted WIP → add with verb + concrete next action. Tag `agent:` if Claude can resume.

### Step 2: Session Log

Append to `~/notes/Daily/YYYY-MM-DD.md`:

```markdown
### HH:MM–HH:MM — [Brief title]
- Key outcome or decision (1-3 bullets)
- Abandoned: X because Y  ← if a path was explored and dropped
```

### Step 3: NOW.md + Trackers

```bash
now-age
```

**NOW.md** — read from disk first. If recent (<1h), update only deltas. If light session (<3 files, no decisions) and still accurate, skip.

Max 15 lines. Resume points must pass cold-start test. Use `[decided]` vs `[open]`. Prune `[decided]` items that no longer gate future action.

**Vault flush:** Update canonical tracker notes (e.g. `[[Capco Transition]]`) if the session advanced them.

**Project CONTEXT.md** — if cwd is `~/code/<project>/` and meaningful progress was made, update State/Last session/Next/Open questions sections. Commit after writing.

### Step 4: Learning Capture (always runs)

Single pass. If nothing surfaces: "Nothing to generalise."

**Scope:** This session + direct predecessors since last deep capture.

**Scan → Route → Implement:**
- Scan for non-obvious patterns, friction, corrections, gotchas
- Route each finding to the most specific destination:
  - Tool gotcha → `~/docs/solutions/`
  - Cross-session context → MEMORY.md
  - Workflow change → the relevant skill's SKILL.md
  - Same mistake twice → escalate per `~/docs/solutions/enforcement-ladder.md`
- **Implement immediately** if small and safe (skill edit, MEMORY.md addition, solutions file). Propose only if large, risky, or needs user input.

**MEMORY.md ≥145 lines + entries added this session →** demote lowest-recurrence entry to `~/docs/solutions/memory-overflow.md` now. Don't ask — pick it yourself.

**All file writes must complete before the wrap output.**

## Output

Bordered prose. Handoff note to tomorrow-you — arc, what's staged/unfinished, learnings captured. 2-3 sentences for light sessions, up to 6 for heavy. Don't hard-wrap.

```
─── Wrap ───────────────────────────────────────

[Prose summary]

Filed: [exact file path or "nothing to generalise"]
─────────────────────────────────────────────────
```

## Boundaries

- Do NOT perform external sends (messages, emails, posts) during wrap.
- Do NOT run deep audits or long research — wrap is a close-out, not a new workstream.
- Stop after writes + wrap summary unless explicitly asked to continue.
