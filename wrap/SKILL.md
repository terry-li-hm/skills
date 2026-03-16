---
name: wrap
description: Session wrap-up OR mid-session checkpoint. Learning capture, TODO sweep, session log. Use at gear shifts (checkpoint mode) or before /clear (full mode). NOT a daily routine — use eow/daily for day-level closures.
user_invocable: true
---

# Wrap

Learning capture + session bookkeeping. Two modes:

- **Full** (`/wrap`) — end-of-session close. All steps.
- **Checkpoint** (`/wrap checkpoint`, or auto-triggered at gear shifts) — capture learnings + sweep TODOs, skip session-end bookkeeping. Preserves context — no /compact, no closure framing.

Session scope = files modified + tool calls + conversation turns since this session began (or since last checkpoint).

## Triggers

- "wrap", "wrap up", "let's wrap" → full mode
- "checkpoint", "wrap checkpoint" → checkpoint mode
- **Auto-trigger (Claude-initiated):** When detecting a significant gear shift (different project, different domain, switching from building to admin, etc.), run checkpoint mode silently before proceeding. Don't ask — just capture.
- "what did we learn" → checkpoint mode

## Mode Detection

If invoked as `/wrap checkpoint` or auto-triggered at a gear shift → **checkpoint mode**.
If invoked as `/wrap` or at session end → **full mode**.

**Checkpoint mode runs:** Step 0 (pre-wrap), Step 0.5 (friction review, but don't truncate log), Step 1 (TODO sweep), Step 4 (learning capture).
**Checkpoint mode skips:** Step 2 (session log), Step 3 (NOW.md rewrite — delta update only if needed).

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
2. **Deferred?** Anything mentioned as "later/next/TODO" not yet captured? Route by type: has a deadline → TODO.md. Has a context trigger ("next time I'm in X") → `memory/prospective.md`. Neither → daily note.
3. **Uncommitted?** Dirty repos *touched this session*? → offer to commit (leave other repos alone)
4. **Garden posts + consulting arsenal?** Pause and replay the session arc (or arc since last checkpoint). What did we *learn*, not just *do*? What surprised us? What principle emerged that wasn't obvious at the start? Give yourself 30 seconds of generative thinking before answering — the best posts come from connections between topics, not from any single task.
   - **Garden test:** Non-obvious insight, clear thesis, Terry's lane, no unverified facts? Publish immediately via `sarcio new` → write → `sarcio publish --push`. Multiple posts per session is normal for meaty sessions.
   - **Arsenal test:** Concretely applicable to a bank/client AI engagement? If yes → add bullet to `[[Capco Transition]]` now.

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
Garden:      published → <slug>, <slug>, ... | no — [reason]
Arsenal:     added → [[Capco Transition]] | no — [reason]
Dispatched:  <audit> (<task-id>) | none
─────────────────────────────────────────────────
```

Then proceed to remaining steps.

### Step 0.5: CLI Friction Review

```bash
cat ~/.claude/cli-friction.jsonl 2>/dev/null | wc -l
```

If `~/.claude/cli-friction.jsonl` has entries: read the file, group errors by CLI tool, and for each tool with 2+ friction events (or 1 event with an obvious fix), suggest a concrete improvement (alias, positional arg, better error message). Output as a fenced block. If any fix is trivial (< 20 lines), implement it or add to TODO.md with `agent:claude`. **Full mode:** truncate the file after processing (`> ~/.claude/cli-friction.jsonl`). **Checkpoint mode:** leave the file intact (accumulate across checkpoints, truncate only at session end).

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Skip if missing.

- **Complete:** Done items → `[x]` with note and `done:YYYY-MM-DD`. Hard test: truly done, or just "dev done"? Move checked items to `~/notes/TODO Archive.md`.
- **Create:** New commitments or interrupted WIP → add with verb + concrete next action. Tag `agent:` if Claude can resume.

### Step 2: Session Log (full mode only)

Append to `~/notes/Daily/YYYY-MM-DD.md`:

```markdown
### HH:MM–HH:MM — [Brief title]
- Key outcome or decision (1-3 bullets)
- Abandoned: X because Y  ← if a path was explored and dropped
```

### Step 3: NOW.md + Trackers (full mode only)

```bash
now-age
```

**NOW.md** — read from disk first. If recent (<1h), update only deltas. If light session (<3 files, no decisions) and still accurate, skip.

Max 15 lines. Resume points must pass cold-start test. Use `[decided]` vs `[open]`. Prune `[decided]` items that no longer gate future action.

**Vault flush:** Update canonical tracker notes (e.g. `[[Capco Transition]]`) if the session advanced them.

**Project CONTEXT.md** — if cwd is `~/code/<project>/` and meaningful progress was made, update State/Last session/Next/Open questions sections. Commit after writing.

### Step 4: Learning Capture (always runs)

Single pass. If nothing surfaces: "Nothing to generalise."

**Scope:** Since last checkpoint (if any), otherwise since session start.

**Scan → Route → Implement:**
- Scan for non-obvious patterns, friction, corrections, gotchas, and new user preferences or personal context
- Route each finding to the most specific destination:
  - Tool gotcha → `~/docs/solutions/`
  - Cross-session context → MEMORY.md
  - Workflow change → the relevant skill's SKILL.md
  - Same mistake twice → escalate per `~/docs/solutions/enforcement-ladder.md`
- **Default: implement now.** Skill edits, MEMORY.md additions, solutions files, small hooks — do them, don't propose them. "Needs design input" is not a valid reason to defer a 20-line improvement. Propose only if: touches shared infrastructure, irreversible, or genuinely ambiguous (and state which). If you wrote "propose" in the wrap output, ask: could I have just done it? If yes, go back and do it.

**MEMORY.md ≥145 lines + entries added this session →** demote lowest-recurrence entry to `~/docs/solutions/memory-overflow.md` now. Don't ask — pick it yourself.

**Decay tracker:** If any MEMORY.md entries prevented mistakes this session, update `memory/decay-tracker.md` with today's date. This is the empirical signal for what to keep vs demote.

**Dispatch wrap audit agents (background, parallel).** These review the session with fresh eyes — not self-grading. Launch all applicable agents with `run_in_background: true`, collect results before writing wrap output.

| Agent | Prompt | When |
|-------|--------|------|
| **Unhookable rules** | "Review this session. Flag moments where a CLAUDE.md rule was violated but couldn't have been caught by a hook (too fuzzy for regex). Examples: asking personal questions without checking vault, deferring instead of acting immediately, asking 'should we?' on obvious actions. List each violation with what happened and whether a mitigation was added." | Always |
| **Compounding scan** | "Review this session. Flag things that compound (insights, frameworks, tools, relationships, skills) that weren't captured anywhere (garden post, skill, arsenal, vault note). Also flag time spent on non-compounding activity (pure admin, naming bikesheds, over-organising). One-line per item." | Always |
| **Garden cull** | "Review garden posts published this session. For each, assess: strong thesis? Own angle (not restating others)? Non-generic? Flag weak ones for removal or merge." | 3+ posts published |

Pass session summary context (files modified, key decisions, corrections received) to each agent. Use `model: "haiku"` for speed. Present results in the wrap output under a `Wrap Agents` section.

**Garden quality cull (weekly only):** If this is a `/weekly` wrap, also scan *all* posts from the week — not just this session's.

**All file writes must complete before the wrap output.**

## Output

**Full mode:** Bordered prose. Handoff note to tomorrow-you — arc, what's staged/unfinished, learnings captured. 2-3 sentences for light sessions, up to 6 for heavy. Don't hard-wrap.

```
─── Wrap ───────────────────────────────────────

[Prose summary]

Filed: [exact file path or "nothing to generalise"]
─────────────────────────────────────────────────
```

**Checkpoint mode:** Lighter border. What was captured, then move on. No handoff framing.

```
─── Checkpoint ─────────────────────────────────
[1-2 sentences: what was captured/filed]
─────────────────────────────────────────────────
```

## Boundaries

- Do NOT perform external sends (messages, emails, posts) during wrap.
- Do NOT run deep audits or long research — wrap is a close-out, not a new workstream.
- **Full mode:** Stop after writes + wrap summary unless explicitly asked to continue.
- **Checkpoint mode:** Continue with the next task after output. No stopping.
