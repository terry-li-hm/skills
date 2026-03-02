---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, NOW.md, learnings safety net.
user_invocable: true
---

# Wrap

End-of-session wrap-up. Pre-wrap check + three mechanical steps + conditional meta-close.

## Execution Notes

- Execute in order. Don't skip earlier steps because a later one seems more interesting.
- Skip any step silently if nothing applies. No ceremony.
- Session scope = files modified + tool calls + conversation turns since this session began.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "what did we learn"
- End of long/meaty session

## Workflow

### Step 0: Pre-Wrap Check (soft gate)

Run before anything else. Present all findings in one block, then proceed — don't block waiting for user action.

#### A. Mechanical checks (run in parallel)

**Skill gap:** Only check if `~/skills/` was modified this session. Unlinked skills are invisible to Claude Code.
```bash
comm -23 <(/bin/ls $HOME/skills/ | sort) <(/bin/ls ~/.claude/skills/ | sort)
```
If gaps: list them, suggest `/agent-sync` or `ln -s`.

**Dirty key repos:** Lost changes to `~/skills/` and `~/agent-config/` hurt future sessions.
```bash
git -C ~/skills status --short && git -C ~/agent-config status --short
```
If dirty: show which files, offer to commit. Don't auto-commit.

**CLAUDE.md modified?** If CLAUDE.md was changed this session, do a one-line tightening check on each addition: does this need to be in CLAUDE.md, or does it belong in a skill / MEMORY.md / `~/docs/solutions/`? Flag candidates — don't move them automatically.

**MEMORY.md budget:** Budget is 150 lines.
```bash
wc -l ~/.claude/projects/-Users-terry/memory/MEMORY.md
```
If >150: flag it, suggest demoting to `~/docs/solutions/memory-overflow.md`.

#### B. Session loose ends (cognitive scan)

Scan for signals of unfinished business:
- Recent tool calls and file writes — anything not verified or tested?
- Conversation mentions of "later", "next", "should", "TODO", "follow up"
- Git diff — uncommitted changes that need context preserved
- Decisions made but not written anywhere
- **LinkedIn angle?** Did anything this session surface a non-obvious insight, architecture decision, or inversion worth sharing? If yes → add entry to `[[LinkedIn Content Ideas]]` before wrapping. Don't draft — just capture the hook and angle.

Present as brief suggestions. User decides what to act on now vs. defer.

#### Output format

One block, before any wrap steps:

```
─── Pre-Wrap ────────────────────────────────────
⚠  [anything needing action]
→  [loose ends / suggested next steps]
✓  [clean checks, or "all clear" if nothing found]
─────────────────────────────────────────────────
```

If everything is clean and no loose ends, one line: "All clear — proceeding."

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Two scans:

**Complete:** Done actions → mark `[x]` with brief note and `done:YYYY-MM-DD`. Hard test: truly done, or just "dev done"? If it needs testing, pushing, or confirmation — stays open with updated status. Move newly-checked `[x]` items to `~/notes/TODO Archive.md`.

**Create:** New commitments, deadlines, or interrupted WIP → add as items. Must have a verb and a concrete next action — "look into X" is not a TODO. Tag with `agent:` if Claude can resume it.

### Step 2: Session Log

Append to `~/notes/Daily/YYYY-MM-DD.md` (create if needed):

```markdown
### HH:MM–HH:MM — [Brief title]
- Key outcome or decision (1-3 bullets max)
- Link to vault note if detail exists: see [[Note Name]]
- Abandoned: X because Y  ← include if a path was explored and dropped
```

2-3 bullets. No implementation details — those belong in vault notes or `~/docs/solutions/`. If a path was abandoned mid-session, record why here — prevents next session from rediscovering the same dead end.

### Step 3: NOW.md + Project Trackers

**NOW.md** (`~/notes/NOW.md`) — check age first:
```bash
/usr/bin/find $HOME/notes/NOW.md -mmin -60 2>/dev/null | grep -q . && echo "recent" || echo "stale"
```
If recent (<1h, likely another session), update only what changed. Otherwise, full overwrite.

A session is **light** if: <3 files were modified and no decisions were made. If light and NOW.md is still accurate, skip.

Max 15 lines:

```markdown
# NOW
<!-- Max 15 lines. Full overwrite at each /wrap. Stale after 24h. -->

## Resume point
- [decided] Exact next step — with [[links]] to canonical notes
- [open] Options discussed but not yet chosen — see [[Note]]
```

Resume points must pass the cold-start test: could another session resume from this alone, without reading any conversation history? Use `[decided]` vs `[open]` to signal how settled each item is.

**Prune `[decided]` items aggressively.** Keep only if they still gate a future action (a date not yet passed, a follow-up not yet sent). If the decision is done-and-absorbed into a skill/vault with no pending follow-up → delete it. "Morning cron killed" is history, not a resume point.

**Vault flush:** If the session advanced a project with a canonical tracker note (e.g. `[[Capco Transition]]`), update that note now. Context doesn't survive — if it's not in a file, it's lost.

### Step 4: Meta-Close (conditional)

**Run if:** a new skill was created, 2+ friction points encountered, or 2+ related decisions made. Otherwise skip.

Do NOT invent learnings. A routine session producing nothing here is correct.

One pass, three outputs:

**A. What generalises?** — The strongest consolidation signal is top-down intent. Explicitly ask: what from this session applies beyond today? Patterns, corrections, architectural insights, reusable approaches. If something generalises → route to MEMORY.md or vault now, before context is lost. If nothing generalises, say so and skip.

**B. File learnings** — Uncaptured friction, corrections, gotchas, or system evolution? Route to the most specific file: tool gotcha → `~/docs/solutions/`, cross-session context → MEMORY.md, skill workflow → the skill's SKILL.md. Should a skill be created or tightened? Hook added? Same mistake twice → escalate per `~/docs/solutions/enforcement-ladder.md`. Propose, don't auto-implement.

**C. Propose improvements** — 1-3 specific improvement candidates: things that felt clunky, a tool that behaved unexpectedly, a repeated manual step that could be automated. Present each as a concrete proposal with a suggested action. If nothing surfaced, say "Nothing to propose." Do NOT ask open-ended questions — the burden is on Claude to identify candidates.

If neither A nor B surfaces anything, skip silently.

## Output

**Write first, then summarise.** All file writes must complete before the bordered output appears.

Use the bordered format below. Prose (not bullets or labels) forces linear reading. The border makes wrap visually distinct from tool output.

Handoff note to tomorrow-you, not a build log. 2-3 sentences for light sessions, up to 6 for heavy ones. Cover: arc, what's staged/unfinished, learnings captured. Weave vault changes in — don't list them. Implementation details belong in vault notes, not here.

**Format:**

```
─── Wrap ───────────────────────────────────────

STR relabelling: from WIP to cold-start handover package. Handover doc drafted, 34 scripts committed with README, CDSW dry run passed. Pipeline test gist staged for the next window.

─────────────────────────────────────────────────
```

**Do NOT hard-wrap the prose.** Let the terminal handle line wrapping naturally.

## Notes

- Steps 0–3 are mechanical and fast. Step 4 is the only place judgment is needed — and only when the session had substance.
- One insight well-routed beats five dumped in the same file
