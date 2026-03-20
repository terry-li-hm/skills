---
name: legatum
description: Session state transfer — bequeath volatile context to durable storage before session death. Learning capture, TODO sweep, session log. Use at gear shifts (checkpoint mode) or before /clear (full mode). NOT a daily routine — use eow/daily for day-level closures. Aliases "wrap", "legatum".
user_invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Legatum — Session State Transfer

A dying session bequeaths its knowledge forward. Two modes:

> **Core framing:** This is state transfer, not documentation. The session holds volatile state — decisions, understanding, corrections — that dies with `/clear`. The legatum's job is to move what matters to durable storage. Everything else is theatre.

- **Full** (`/legatum` or `/wrap`) — end-of-session close. All steps.
- **Checkpoint** (`/legatum checkpoint` or `/wrap checkpoint`, auto-triggered at gear shifts) — capture learnings + sweep TODOs, skip session-end bookkeeping. Preserves context — no /compact, no closure framing.

Session scope = files modified + tool calls + conversation turns since this session began (or since last checkpoint).

## Triggers

- "wrap", "wrap up", "let's wrap", "legatum" → full mode
- "checkpoint", "wrap checkpoint" → checkpoint mode
- **Auto-trigger (Claude-initiated):** When detecting a significant gear shift (different project, different domain, switching from building to admin, etc.), run checkpoint mode silently before proceeding. Don't ask — just capture.
- "what did we learn" → checkpoint mode

## Mode Detection

If invoked as checkpoint or auto-triggered at a gear shift → **checkpoint mode**.
If invoked at session end → **full mode**.

**Checkpoint mode runs:** Step 0 (pre-wrap), Step 1 (TODO sweep), Step 3 (learning capture).
**Checkpoint mode skips:** Step 2 (session log + NOW.md).

## Workflow

### Skip gate

```bash
legatum gather --json
```

Parse `now.age_label`. If **"fresh"** (NOW.md <15 min old) AND user did not explicitly invoke `/legatum`, skip to Step 3 briefly, then Output. Explicit invocation always runs all steps.

### Step 0: Pre-Wrap Check

```bash
legatum gather
```

This runs all deterministic checks (dirty repos, skill sync, MEMORY.md budget, NOW.md age, deps, peira). Review the output, then apply judgment:

**Three questions (not five):**
1. **Uncommitted?** Dirty repos *touched this session*? → commit.
2. **Deferred?** Anything mentioned as "later/next/TODO" not yet captured? Route: deadline → TODO.md, context trigger → `memory/prospective.md`, neither → daily note.
3. **Garden + arsenal?** Replay the session arc. What did we *learn*, not just *do*? What principle emerged?
   - **Garden test:** Non-obvious insight, clear thesis, Terry's lane? → publish via `sarcio`.
   - **Arsenal test:** Applicable to a bank/client AI engagement? → `[[Capco Transition]]`.

**CLAUDE.md modified?** One-line check: does it belong in CLAUDE.md or somewhere else?

**Output — light or full:**

If all clean: `✓ Clean — [gather summary]. Garden: [published/no]. Arsenal: [added/no].`

Otherwise:
```
─── Pre-Legatum ─────────────────────────────────
⚠  [only if action needed]
✓  [clean checks]
Garden:      published → <slug> | no — [reason]
Arsenal:     added → [[Capco Transition]] | no — [reason]
──────────────────────────────────────────────────
```

### Step 1: TODO Sweep

```bash
legatum archive
```

This moves completed `[x]` items to the archive with `done:` tags. Then apply judgment:

- **Create:** New commitments or interrupted WIP → add with verb + concrete next action. Tag `agent:` if Claude can resume.

### Step 2: Session Log + NOW.md (full mode only)

```bash
legatum daily "Brief session title"
```

This appends a timestamped session log template to today's daily note. Then fill in the content:

- Key outcome or decision (1-3 bullets)
- Abandoned: X because Y  ← if applicable

**The legatum summary prose goes here as the final paragraph of the session log.** This is the arc, the synthesis, the judgment — not just facts. The daily note is the durable record; the conversation transcript is ephemeral. The summary must be persisted.

**NOW.md** — read from disk. If recent (<1h), update only deltas. Max 15 lines, dual-ledger format (Facts + Progress).

**Vault flush:** Update canonical tracker notes if the session advanced them.

### Step 3: Learning Capture (always runs)

Single pass. If nothing surfaces: "Nothing to generalise."

**If learnings were captured continuously during the session** (memory entries, skill updates, CLAUDE.md edits already made), this step is a verification pass only. Confirm what was filed, note any gaps. Don't re-file.

**If learnings were NOT captured during the session**, scan and route:
- Tool gotcha → `~/docs/solutions/`
- Cross-session context → MEMORY.md
- Workflow change → relevant skill's SKILL.md
- Same mistake twice → escalate per enforcement ladder

**Default: implement now.** Don't propose — do.

**MEMORY.md ≥145 lines →** demote lowest-recurrence entry to overflow.

**Self-scan (30 seconds, no agents):**
1. Any CLAUDE.md rule violated AND caused worse outcome?
2. Anything compound that wasn't captured?
3. Garden posts 3+? → flag for quality cull.

**All file writes must complete before the output.**

## Output

**Full mode:** Bordered prose appended to daily note AND shown in conversation. The summary is the arc — what was learned, what's staged, honest judgment.

```
─── Legatum ────────────────────────────────────

[Prose summary — arc, learnings, what's staged/unfinished]

Filed: [exact file paths or "nothing to generalise"]
Session: [1-line honest judgment]
─────────────────────────────────────────────────
```

**Checkpoint mode:** Lighter. What was captured, then move on.

```
─── Checkpoint ─────────────────────────────────
[1-2 sentences: what was captured/filed]
─────────────────────────────────────────────────
```

## Boundaries

- Do NOT perform external sends during legatum.
- Do NOT run deep audits or research — legatum is a close-out, not a workstream.
- **Full mode:** Stop after writes + summary.
- **Checkpoint mode:** Continue with the next task after output.
