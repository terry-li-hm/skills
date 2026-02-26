---
name: wrap
description: End-of-session wrap-up. TODO sweep, session log, NOW.md, learnings safety net.
user_invocable: true
---

# Wrap

End-of-session wrap-up. Three mechanical steps + a conditional safety net.

## Triggers

- "wrap", "wrap up", "let's wrap"
- "what did we learn"
- End of long/meaty session

## Workflow

Execute in order. Each step is independent — don't skip earlier steps if a later one seems more interesting.

### Step 1: TODO Sweep

Read `~/notes/TODO.md`. Two scans:

**Match:** Completed actions → mark `[x]` with brief note and `done:YYYY-MM-DD`. Skim for: sent, done, submitted, ordered, confirmed, booked, cancelled.

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

**NOW.md** (`~/notes/NOW.md`) — full overwrite, max 15 lines:

```markdown
# NOW
<!-- Max 15 lines. Full overwrite at each /wrap. Stale after 24h. -->

## Resume point
- [What you were doing + exact next step — with [[links]] to canonical notes]

## Running (if any)
- [PIDs, log paths, resume commands]
```

**Vault flush:** If the session advanced a project with a canonical tracker note (e.g. `[[Capco Transition]]`, `[[Waking Up Transcription Progress]]`), update that note now. Conversation context doesn't survive — if it's not in a file, it's lost.

### Step 4: Learnings Safety Net (conditional)

**Skip this step if:** learnings were already captured during the session (check: any writes to `~/docs/solutions/`, MEMORY.md, or skill files this session?). The `UserPromptSubmit` hook already prompts real-time capture — wrap is the safety net, not the primary mechanism.

**If nothing was captured,** run this checklist internally (don't print):

- [ ] Retried anything? (friction)
- [ ] Terry corrected me? (wrong assumption)
- [ ] Tool behaved unexpectedly? (gotcha)
- [ ] Rule existed but got bypassed? (→ `~/docs/solutions/rule-violation-log.md`)
- [ ] Terry chose X over Y without explaining? (implicit preference)

If something surfaces, route directly:

| Type | Destination |
|------|-------------|
| Tool gotcha | `~/docs/solutions/` |
| Workflow preference | Relevant vault note |
| Cross-session agent context | MEMORY.md |
| Skill improvement | The skill's SKILL.md |
| Rule violation | `~/docs/solutions/rule-violation-log.md` |

No dedup search, no staging area. If you missed it all session, just write it now.

## Output

**Write first, then summarise.** A short prose paragraph under `**Wrap**`:

1. What the session accomplished (the arc)
2. What changed in the vault (weave in naturally)
3. What's unfinished or staged for next time
4. Learnings captured and where (only if something was captured)

3-5 sentences. Handoff note to tomorrow-you, not a build log.

**Example (meaty):**

> **Wrap**
> Spent the session turning the STR relabelling project from "my work in progress" into "a package someone else can pick up cold." Drafted a full handover doc, committed all 34 floating scripts with a README, ran the dry run on CDSW — all checks passed. TODO updated. Pipeline test gist staged for the next CDSW window.

**Example (light):**

> **Wrap**
> Quick session — replied to Luna about Thursday coffee and cleaned up Gmail labels. Daily note updated, nothing else changed.

## Notes

- This is a sweep, not a ritual — 30 seconds, not 3 minutes
- One insight well-routed beats five dumped in the same file
