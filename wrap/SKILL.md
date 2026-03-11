---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, NOW.md, learnings safety net.
user_invocable: true
---

# Wrap

End-of-session wrap-up. Pre-wrap check + three mechanical steps + meta-close.

## Execution Notes

- Execute in order. Don't skip earlier steps because a later one seems more interesting.
- Skip Steps 1–3 silently if nothing applies. Step 4 always runs and always produces output. No ceremony.
- Session scope = files modified + tool calls + conversation turns since this session began.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "what did we learn"
- End of long/meaty session

## Workflow

### Skip gate (repeat wrap guard)

Before anything else, run:
```bash
now-age
```
If NOW.md is **<15 minutes old** AND the user did not explicitly invoke `/wrap`, this wrap already ran in this session. Skip Steps 0–3, run Step 4 briefly, then Output. If the user explicitly typed `/wrap` or "wrap", always run all steps regardless of age.

### Step 0: Pre-Wrap Check (soft gate)

Run before anything else. Present all findings in one block, then proceed — don't block waiting for user action.

#### A. Mechanical checks (run in parallel)

Run all mechanical checks with:
```bash
prewrap
```
Interprets output: `⚠` = action needed, `✓` = clean, `?` = check unavailable. Only use `⚠` when there is something to act on — never `⚠  none`.
- Unlinked skills → suggest `ln -s` or `/agent-sync`
- Dirty repos → show files, offer to commit (don't auto-commit)
- MEMORY.md >150 lines → suggest demoting to `~/docs/solutions/memory-overflow.md`

**CLAUDE.md modified?** If CLAUDE.md was changed this session, do a one-line tightening check on each addition: does this need to be in CLAUDE.md, or does it belong in a skill / MEMORY.md / `~/docs/solutions/`? Flag candidates — don't move them automatically.

#### B. Session loose ends (active checklist)

Answer each question before moving on. Do not scan and skip — a "no" is a valid answer; silence is not.

1. **Anything unverified?** Did any tool call, file write, or command run this session produce output that wasn't checked? If yes → note it.
2. **Anything deferred?** Did the conversation mention "later", "next", "should", "TODO", or "follow up" for something not yet captured? If yes → add to TODO.md or note it.
3. **Uncommitted changes?** Any dirty repo with context that won't survive `/clear`? **Only act on repos touched this session** — dirty files from other sessions or parallel agents should be left alone (they may be in-progress work). If yes and touched this session → offer to commit.
4. **Garden post?** Did a non-obvious insight emerge with a clear thesis, no factual claims needing verification, and no real names? Terry's lane = AI engineering, workflow systems, tooling, personal systems, consulting practice — if the insight touches any of these, lane = yes. **Bar is staging, not perfection** — the garden is a holding area; LinkedIn pulls from it when timing is right. When in doubt: draft and let judge decide. Judge is the gate, not this check. Answer yes or no explicitly. If yes → run the sarcio auto-publish protocol now. Do not defer. Wrap is the safety net.
5. **Consulting arsenal?** Did anything surface that's concretely applicable to a bank or client AI engagement? Answer yes or no explicitly. If yes → add bullet to `[[Capco Transition]]` under "Consulting Arsenal" now.

Questions 4–5 require an explicit yes/no answer in the Pre-Wrap output block. Omitting them is a skip, not a "no."

**Active experiments?** Run `peira status 2>/dev/null || true` — if a campaign is active, surface current score in the Pre-Wrap block. Exit code 1 with "Failed to read log.toml" = no active experiment, treat as clean skip.

#### C. Background dispatch queue

Dispatch standing audits when the session touched the relevant area. Fire with `run_in_background: true` — don't wait for results.

| Audit | Dispatch when |
|-------|---------------|
| MEMORY.md hook coverage | MEMORY.md was modified this session AND line count <145 |
| Skill staleness (scan `~/skills/` for outdated refs) | Any skill edited or added |
| Solutions KB dedup (find overlapping entries in `~/docs/solutions/`) | `~/docs/solutions/` modified |
| Vault orphan links (`nexis` skill) | Monthly only — skip if run this month |

If nothing qualifies, skip silently. If dispatched, add a `Dispatched:` line to the Pre-Wrap block. **Check results at Step 4** (meta-close) — dispatch happens early enough in wrap that most audits complete before Step 4 runs. Do NOT dispatch at the very end of a session; background agents are child processes and die when the session closes.

#### Output format

One block, before any wrap steps. Q4–6 are **always present** — no "all clear" shortcut that skips them:

```
─── Pre-Wrap ────────────────────────────────────
⚠  [only if action needed — omit this line entirely if nothing to flag]
→  Deferred: [things mentioned as "later/next/TODO" not yet captured, or "none"]
✓  [clean checks, e.g. "skills synced, repos clean, MEMORY.md 147/150"]
Garden post: drafted → <slug> | no — [reason]
Arsenal:     added → [[Capco Transition]] | no — [reason]
Dispatched:  <audit name> (<task-id>) | none
─────────────────────────────────────────────────
```

**"yes" is not a valid terminal state for garden post.** It must resolve to either `drafted → <slug>` (sarcio ran, judge passed, published) or `no — [reason]`. "Flagging as idea", "needs more work", or "will do later" are all `no`. Draft now or say no — there is no middle ground.

**Blocking actions — complete before outputting pre-wrap block:**
- Garden post: invoke the `sarcio` skill to get command syntax, then run: `sarcio new "Title"` → write post → judge → `sarcio publish <slug> --push`. Then write `drafted → <slug>` in the block. Do NOT stage or defer — draft and publish in the same wrap.
- Arsenal: add bullet to `[[Capco Transition]]`. Then write `added → [[Capco Transition]]`.

The block is a receipt, not a plan. Write it after the action, not before.

"I'll do it later" or adding to NOW.md does not count. The point of the gate is that session context — the material for the post — evaporates after wrap. Act while the insight is hot.

**HARD STOP after Pre-Wrap block.** Output the Pre-Wrap block, then stop. Do not continue to Steps 1–4 in the same response. Wait for user reply. This is the only real enforcement — if Pre-Wrap and Step 1 are in the same response, there is no pause and blocking yes answers get skipped.

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Two scans:
If TODO.md is missing, note "TODO sweep skipped (TODO.md unavailable)" and continue to Step 2.

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
If write fails, note "Daily log update failed" in final wrap output and continue.

### Step 3: NOW.md + Project Trackers

**NOW.md** (`~/notes/NOW.md`) — check age first:
```bash
now-age
```
If recent (<1h, likely another session), update only what changed. Otherwise, full overwrite.
If age check command fails, treat as stale and proceed with full overwrite.

**ALWAYS read NOW.md from disk before writing.** Use the on-disk content as the baseline — never reconstruct from session memory alone. Apply session deltas (new decisions, completed items) on top of what's already there. This prevents resurrecting items completed in other sessions or by Obsidian CloudKit sync between wraps.

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

**Prune `[decided]` items aggressively.** Keep only if they still gate a future action (a date not yet passed, a follow-up not yet sent). If done-and-absorbed → drop from NOW.md. The daily note (step 2) is the permanent record — once it's logged there, NOW.md doesn't need to hold it.

**Vault flush:** If the session advanced a project with a canonical tracker note (e.g. `[[Capco Transition]]`), update that note now. Context doesn't survive — if it's not in a file, it's lost.
If tracker note is missing, note "Tracker unavailable" and keep summary in daily note.

**Project CONTEXT.md** — if the session cwd is inside `~/code/<project>/`:

Check for `~/code/<project>/CONTEXT.md`. If the session made meaningful progress (code written, decisions made, direction changed) → write or update it:

```markdown
# <project> Context
<!-- Updated: YYYY-MM-DD -->

## What it does
One sentence.

## State
Current implementation status.

## Last session
What was done or decided.

## Next
Immediate next step (one action).

## Open questions
Things still to resolve (omit section if none).
```

Only the **State**, **Last session**, **Next**, and **Open questions** sections change between sessions — don't rewrite the whole file if only one section changed.

After writing: `cd ~/code/<project> && git add CONTEXT.md && git commit -m "Update CONTEXT.md"`.

Skip if: the session was a light read/explore with no new decisions, or CONTEXT.md is already accurate.

### Step 4: Meta-Close (always run)

Always run. If nothing surfaces, one line: "Nothing to generalise." Do NOT invent learnings.

**Scope: this session + any direct predecessors since last deep capture.** Follow-on sessions (NOW.md recent, short conversation) often contain gems from the preceding session that weren't captured yet. Don't restrict the scan to just what happened in this exchange.

One pass, three outputs:

**A. What generalises?** — Start with: *"Name 1–3 things from this session (or the work it built on) that were non-obvious."* If you can name them, **file them immediately** — edit MEMORY.md, `~/docs/solutions/`, or the relevant skill now. Do not state them in the wrap output without also writing them to a file. Stated-but-not-filed learnings are lost after `/clear`. If truly nothing, say "Nothing to generalise" explicitly.

**B. File learnings** — Uncaptured friction, corrections, gotchas, or system evolution? Route to the most specific file: tool gotcha → `~/docs/solutions/`, cross-session context → MEMORY.md, skill workflow → the skill's SKILL.md. **Implement directly** — edit the target file now. Should a skill be tightened? Edit it. Hook needed? Write it. Same mistake twice → escalate per `~/docs/solutions/enforcement-ladder.md`. Only defer if the change requires user input or is genuinely out of scope for a wrap.

**C. Implement improvements** — 1-3 specific improvement candidates: things that felt clunky, a tool that behaved unexpectedly, a repeated manual step that could be automated. For each: **implement if it's a small, safe, local change** (skill edit, MEMORY.md addition, solutions file). Propose (don't implement) only if the change is large, risky, or requires user decision. If nothing surfaced, say "Nothing to implement." Do NOT ask open-ended questions — the burden is on Claude to identify and act on candidates.

**MEMORY.md at ≥145 lines and entries added this session → demote inline now.** Don't dispatch an audit — identify the lowest-recurrence entries added this session and move them to `~/docs/solutions/memory-overflow.md` immediately. The background hook audit is for general coverage; budget pressure is the trigger for immediate action.

## Output

**Write first, then summarise.** All file writes must complete before the bordered output appears.

Use the bordered format below. Prose (not bullets or labels) forces linear reading. The border makes wrap visually distinct from tool output.

Handoff note to tomorrow-you, not a build log. 2-3 sentences for light sessions, up to 6 for heavy ones. Cover: arc, what's staged/unfinished, learnings captured. Weave vault changes in — don't list them. Implementation details belong in vault notes, not here.

**Format:**

```
─── Wrap ───────────────────────────────────────

STR relabelling: from WIP to cold-start handover package. Handover doc drafted, 34 scripts committed with README, CDSW dry run passed. Pipeline test gist staged for the next window.

Filed: [file path or "nothing to generalise"]
─────────────────────────────────────────────────
```

The `Filed:` line is a receipt — name the exact file edited, or state "nothing to generalise" explicitly. Omitting it means Step 4 was skipped.

**Do NOT hard-wrap the prose.** Let the terminal handle line wrapping naturally.

## Notes

- Steps 0–3 are mechanical and fast. Step 4 always runs — "Nothing to generalise" is a valid one-line answer for light sessions.
- One insight well-routed beats five dumped in the same file

## Boundaries

- Do NOT perform external sends (messages, emails, posts) during wrap.
- Do NOT run deep audits or long research; wrap is a close-out ritual, not a new workstream.
- Stop after writes + wrap summary. Do not continue with implementation unless explicitly requested.
