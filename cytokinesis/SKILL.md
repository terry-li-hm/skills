---
name: cytokinesis
description: Consolidate while context is hot — capture what dies with the session
user_invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Cytokinesis — Session Memory Consolidation

> Cytokinesis is continuous, not terminal. Capture anything useful to vivesca the moment it surfaces — don't wait for the session to die. The end-of-session invocation is a verification pass, not the main event. The ideal cytokinesis has nothing left to do.

**One test:** is this useful to vivesca? If yes, route it:

| What | Where |
|---|---|
| Learning / correction | Memory file + MEMORY.md index |
| Workflow improvement | Skill update (edit now, don't defer) |
| Commitment / action | Praxis.md (with full context — hot todos > cold stubs) |
| Publishable insight | Tweet / garden / announce (draft and ship) |
| Tool gotcha | `~/docs/solutions/` |
| State change | Tonus.md |

**Capture generously — this means FILE MORE, not less.** Default is FILE. Only SKIP what is duplicated verbatim in an existing memory. If in doubt, file. The LLM's default is to over-filter; fight that instinct. A separate process handles forgetting.

**Selection priority** (when triaging candidates):
1. **Prediction errors** — corrections, wrong assumptions. Highest signal.
2. **Novelty** — first time this came up.
3. **Emotional weight** — strong pushback, repeated insistence.
4. **Pattern completion** — reinforces existing memory. Update, don't duplicate.
5. **Routine/expected** — only skip if obviously already known.

**Full** (`/cytokinesis`) — consolidation + housekeeping.
**Checkpoint** (`/cytokinesis checkpoint`, auto at gear shifts) — consolidation only.

## Workflow

### 1. Consolidation (the point)

Two things in parallel:

1. **Ask Terry: "What's worth keeping?"** — the nucleus knows what mattered.
2. **Run `cytokinesis gather`** — LLM extracts what it thinks is valuable.

Merge both. Terry fills gaps the LLM missed. LLM catches things Terry forgot. Route everything to the right places.

If continuous capture handled most of it → quick verification pass for both.

**MEMORY.md ≥145 lines →** demote lowest-recurrence entry.

### 2. Housekeeping (full mode only)

1. **Uncommitted?** Dirty repos touched this session → commit.
2. **TODO sweep:** `cytokinesis archive`
3. **Session log:** `cytokinesis daily "title"` — outcomes + session arc prose.
4. **Tonus.md** — update deltas. Max 15 lines, dual-ledger.

## Output

```
─── Cytokinesis ──────────────────────────────────
Filed: [exact file paths]
Published: [tweets/garden posts or "none"]
Done.
─────────────────────────────────────────────────
```

## Boundaries

- No deep audits or research — consolidation, not workstream.
- Full mode: stop after writes.
- Checkpoint mode: continue after output.
