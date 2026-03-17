---
name: conclusio
description: Heuristics for session wrap-ups — failure modes, quality tests, routing rules. Reference skill consulted by wrap, eow, daily. Not user-invocable.
disable-model-invocation: true
---

# Conclusio — Wrap-Up Heuristics

> *Conclusio: Latin "closing, conclusion" — the deliberate end that preserves what matters.*

Reference skill for session close-out. Consulted by `wrap`, `eow`, `daily`.

## Organizing Principle

A wrap-up is **state transfer** — present-you (full context) to future-you (zero context). Use this to cut decisions fast:

- "Should I log this?" → "Will future-me need this to resume?"
- "Should I save this insight?" → "Will future-me encounter this situation again?"
- "Should I update NOW.md?" → "If I read only NOW.md tomorrow, would I know what's hot?"

## Failure Modes

1. **Completionism** — capturing everything. Wrap becomes longer than the work. Signal: wrap takes >10% of session time.
2. **Narration over extraction** — "I did X, then Y" instead of "the insight was W." Logs and insights serve different audiences and belong in different places.
3. **Deferred action as capture** — "TODO: think about X" instead of thinking about X now while context is live. The wrap becomes a dumping ground for decisions you don't want to make. Smell: any "TODO: consider..." in wrap output.
4. **Premature generalisation** — one-time observation promoted to rule before it's earned. Not everything deserves a memory entry. Test: has this happened twice?
5. **Missing gear shifts** — the most valuable insights come at domain boundaries (coding → strategy, project A → project B). Without checkpoints at these transitions, cross-domain connections evaporate.
6. **Stale ritual** — same depth regardless of session weight. A 10-minute admin session doesn't need the same wrap as a 3-hour build. Scale wrap effort to session complexity.
7. **Capture without routing** — a brilliant insight in a daily note is effectively lost. Knowledge must land where it will be *surfaced*, not just *stored*.

## Key Distinctions

- **Log vs. insight** — Logs record what happened (daily note). Insights record what was learned (skills, memory, solutions KB). Different audiences: "what did I do?" vs. "what should I do differently?"
- **Session vs. work vs. day** — Different scopes need different depth. Session = what's hot, resume point. Work = what's done, what's blocked. Day = arc, energy, tomorrow.
- **Capture vs. action** — The best wraps don't just capture — they *do*. File the memory, update the TODO, commit the code, publish the post. "I should do X" in a wrap note is a smell — either do it now or admit it's not important enough.

## Quality Axes

1. **Signal-to-noise** — Ratio of actionable content to filler. Best wraps are short.
2. **Routing accuracy** — Each piece of knowledge lands in the right layer (skill vs. memory vs. daily note vs. TODO vs. discard).
3. **Resume fidelity** — The cold-start test: "If I lost all memory and read only this, could I resume effectively?"
4. **Insight yield** — Did the wrap surface something the session didn't explicitly produce? Connections between topics, patterns across sessions.
5. **Time proportionality** — Wrap effort scales with session complexity, not fixed ritual.

## Human-Agent Split

| Agent | Human |
|-------|-------|
| Mechanical capture (files changed, git status, TODO sweep) | Recognising what actually mattered vs. what seemed urgent |
| Routing (where does each piece go?) | Cross-session pattern recognition |
| Cold-start test (is the resume point sufficient?) | Judgment on what's worth generalising |
| Consistency (never forgets the checklist) | Energy/emotional signal as data ("this drained me" is information) |

**Anti-pattern:** Agent captures everything mechanically but misses the one insight that mattered. Human reflects deeply but forgets to update the actual files. Good wraps combine both.

## The "So What" Test

For every item in a wrap, ask: "So what?" If the answer is "future-me needs this to resume" → keep. If "it's interesting" → probably discard. If "it changes how I work" → route to the right skill/memory. The test is ruthless but prevents wrap bloat.
