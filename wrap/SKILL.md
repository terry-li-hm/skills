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

Execute in order. Each step is independent — don't skip earlier steps if a later one seems more interesting.

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Two scans:

**Match:** Completed actions → mark `[x]` with brief note and `done:YYYY-MM-DD`. Skim for: sent, done, submitted, ordered, confirmed, booked, cancelled. Hard test: is it truly done, or just "dev done"? If it still needs testing, pushing, or confirmation, it stays open with an updated status.

**Create:** New commitments, deadlines, or interrupted WIP → add as new items. Hard test: did anything start but not finish? If there's a concrete next action, it's a TODO (with `agent:` tag if Claude can resume it).

Skip silently if nothing matches.

### Step 2: Session Log

Append to `~/notes/Daily/YYYY-MM-DD.md` (create if needed):

```markdown
### HH:MM–HH:MM — [Brief title]
- Key outcome or decision (1-3 bullets max)
- Link to vault note if detail exists: see [[Note Name]]
```

2-3 bullets. No implementation details — those belong in vault notes or `~/docs/solutions/`. This feeds `/daily`.

### Step 3: NOW.md + Project Trackers

**NOW.md** (`~/notes/NOW.md`) — check `stat -f %m` first. If written <1h ago by another session, verify accuracy and update only what changed. Otherwise, full overwrite. Max 15 lines:

```markdown
# NOW
<!-- Max 15 lines. Full overwrite at each /wrap. Stale after 24h. -->

## Resume point
- [What you were doing + exact next step — with [[links]] to canonical notes]

## Running (if any)
- [PIDs, log paths, resume commands]
```

**Vault flush:** If the session advanced a project with a canonical tracker note (e.g. `[[Capco Transition]]`, `[[Waking Up Transcription Progress]]`), update that note now. Conversation context doesn't survive — if it's not in a file, it's lost.

### Step 4: Meta-Sweep (conditional)

**Skip entirely if:** the session was routine — simple Q&A, no friction, no corrections, no novelty. Do NOT invent learnings to satisfy this step. A routine session producing nothing here is the correct outcome, not a failure.

**If the session had substance,** one pass through three lenses:

1. **Safety net:** Uncaptured friction, corrections, or gotchas? (The `UserPromptSubmit` hook handles most in real-time — wrap catches what slipped through.) Route to the most specific relevant file: tool gotcha → `~/docs/solutions/`, cross-session context → MEMORY.md, skill workflow → the skill's SKILL.md, rule violation → `~/docs/solutions/rule-violation-log.md`.
2. **System evolution:** Should a skill be created or tightened? Should a hook be added? (Same mistake twice despite a rule → escalate per `~/docs/solutions/enforcement-ladder.md`.) Should something port to Hexis? (Generic fix only — not personal tooling.) Propose, don't auto-implement.
3. **Generalization:** Does any learning apply beyond where it was routed? Instance → pattern → principle. Most don't — if nothing generalizes, move on.

One pass, all three lenses. If nothing surfaces, skip silently.

## Output

**Write first, then summarise.** Use the bordered format below — prose inside, 3-5 sentences. The border makes the wrap visually distinct from tool output so it's easy to spot. Prose (not structured labels) forces linear reading.

Content to cover:

1. What the session accomplished (the arc)
2. What changed in the vault (weave in naturally)
3. What's unfinished or staged for next time
4. Learnings captured and where (only if something was captured)

Handoff note to tomorrow-you, not a build log.

**Format:**

```
─── Wrap ───────────────────────────────────────

Spent the session turning the STR relabelling
project from "my work in progress" into "a
package someone else can pick up cold." Drafted
a full handover doc, committed all 34 floating
scripts with a README, ran the dry run on CDSW —
all checks passed. TODO updated. Pipeline test
gist staged for the next CDSW window.

─────────────────────────────────────────────────
```

## Notes

- This is a sweep, not a ritual — 30 seconds, not 3 minutes
- One insight well-routed beats five dumped in the same file
