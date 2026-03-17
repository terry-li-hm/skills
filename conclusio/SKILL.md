---
name: conclusio
description: Reference heuristics for session wrap-ups — failure modes, quality axes, state-transfer framing. Consult from wrap, eow, daily. Not user-invocable.
user_invocable: false
disable-model-invocation: true
---

# Conclusio — Theory of Wrap-Ups

> Fodina mine (Tier 1). Wired to: wrap, eow, daily.

## The Reframe

A wrap-up is **state transfer**, not documentation. The session holds volatile state — decisions, understanding, corrections — that dies with `/clear`. The wrap's job is to move what matters to durable storage. Everything else is theatre.

**The test for each piece:** "If I forget this entirely, will it cause harm or force re-derivation?" Yes → capture. No → skip.

## Failure Modes

| # | Name | Smell | Fix |
|---|------|-------|-----|
| 1 | **Performative capture** | "Updated X" with no what/why | State what changed and why it matters to a cold reader |
| 2 | **Deferred action as capture** | "TODO: consider whether..." | Decide now or delete. Wraps are not parking lots |
| 3 | **Completionism** | >3 "filed to X" items in one wrap | Prioritise. 15 learnings = 0 learnings |
| 4 | **Log-as-insight confusion** | Recording what happened, not what was learned | Logs → daily note. Insights → skill/memory/garden |
| 5 | **Wrap theatre** | Elaborate output, no behaviour change tomorrow | Ask: will a fresh session actually read and act on this? |
| 6 | **Missing the meta** | "Fixed keychain bug" | "Keychain ops need newline stripping" — prevent recurrence |
| 7 | **Context-dependent capture** | Insight requires full session context to parse | Rewrite for a cold reader or don't save |
| 8 | **Depth mismatch** | 10-min admin session gets full wrap | Scale depth to session complexity |
| 9 | **Wrap as new workstream** | Wrap takes >10 minutes | You're writing, not closing. Stop |

## Quality Axes

1. **Cold-start readability** — Can a fresh session with zero context pick up from this wrap? The handoff note is for tomorrow-you, not today-you.
2. **Actionability** — Every item has a concrete next action or is explicitly marked as decided/closed. No vague pointers.
3. **Signal density** — Ratio of useful information to total words. Shorter is almost always better.
4. **Correct routing** — Each piece landed in the right layer (skill > memory > daily note). Consult scrinium.
5. **Capture-action ratio** — Bias toward implementing now. If you can update the skill in 2 minutes during wrap, do it — don't defer.

## Key Distinctions

- **Log vs insight** — Logs record what happened (daily note, ephemeral). Insights record what was learned (skill/memory/garden, durable). Different audiences, different shelf life.
- **Summary vs handoff** — A summary recounts the session (backward-looking). A handoff tells the next session what to do (forward-looking). **Wraps should be handoffs.**
- **Specific vs general** — "We symlinked memory to vault" is a log entry. "CC memory should be backed up via vault symlink" is a transferable insight. Capture the general when it exists.

## The Volatile State Checklist

State that lives in conversation and dies with `/clear`:

| State type | Where to transfer | Risk if lost |
|------------|-------------------|--------------|
| Decisions made but not written | NOW.md, tracker notes | Re-deliberation, contradictory decisions |
| New understanding / mental models | Skill, garden post | Re-derivation (unreliable) |
| Corrections to prior beliefs | `[[Priors Worth Correcting]]`, memory | Old belief reasserts silently |
| Uncommitted code changes | Git commit | Lost work |
| Deferred items mentioned in passing | TODO.md, prospective.md | Forgotten commitments |

## Anti-Patterns to Watch

- **"Nothing to generalise"** after a substantive session → you're not looking hard enough. Replay the session arc.
- **Garden post inflation** — 3+ posts in one session is a smell. Quantity dilutes quality.
- **Recursive wrap improvement** — improving the wrap skill during wrap. Do it, but recognise the irony and stop at one change.
- **NOW.md churn** — rewriting NOW.md when nothing changed. Skip if still accurate.
