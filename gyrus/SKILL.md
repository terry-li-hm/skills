---
name: gyrus
description: Flywheel design pattern — self-improving systems that minimize human touchpoints. Consult when building any recurring process, reviewing automation, or when artifex 14b identifies a feedback signal. NOT for one-shot tasks.
user_invocable: false
---

# Gyrus — Flywheel Design Pattern

*Gyrus* (Latin: circle, rotation) — systems that get better by running.

Consult when building anything that runs more than once. The question isn't "should this be automated?" — it's "does running it make it better next time?"

## The Three Tiers

Every check in a flywheel should be assigned a tier. Default to the highest tier possible — escalate to human only when you must.

| Tier | Human involvement | When to use | Example |
|------|-------------------|-------------|---------|
| **1. Auto-fix** | None | Fix is safe, reversible, obvious | Sopor stale → run sync. Daemon dead → restart. |
| **2. Auto-detect + surface** | Human decides action | Problem is clear but fix needs judgment | Skill trigger miss → propose new phrase in morning brief |
| **3. Human only** | Human detects and fixes | Requires taste, context, or irreversible action | Garden cull, theme synthesis, energy audit |

**Design pressure is always downward.** Every Tier 3 should be examined: can part of it become Tier 2? Every Tier 2: can the proposed fix just be applied automatically (Tier 1)?

### Tier 1 criteria (auto-fix)

All three must be true:
1. **Reversible** — the fix can be undone trivially
2. **Unambiguous** — there's exactly one correct action
3. **Safe to repeat** — running the fix when nothing's wrong causes no harm

If any is false → Tier 2.

### Tier 2 design

The value of Tier 2 is in the *surfacing*, not the reporting. Design principles:
- **Propose the fix, not just the problem.** "MEMORY.md is 162 lines" < "MEMORY.md is 162/150 — demote these 3 entries?"
- **Surface at the decision point.** Morning brief for daily issues, weekly review for trends.
- **Batch, don't interrupt.** Never alert in real-time for non-urgent Tier 2 items. Collect and surface at the next natural checkpoint.

## The Flywheel Loop

```
Predict/Check → Log → Reconcile → Fix → Predict better
     ↑                                        |
     └────────────────────────────────────────┘
```

### Five components

1. **Sensor** — detects the state (hook, cron, health check)
2. **Log** — append-only record (TSV, JSONL — not memory)
3. **Reconciler** — compares predicted vs actual, identifies gaps
4. **Fixer** — Tier 1: auto-applies. Tier 2: proposes. Tier 3: surfaces for human.
5. **Learner** — feeds fixes back into the sensor's rules so it predicts better

If any component is missing, you have a cron job, not a flywheel:
- No log → can't reconcile → no learning
- No reconciler → log is write-only
- No learner → same mistakes repeat
- No fixer → reconciler output is ignored

### The metric test

From artifex 14b: **what number goes up or down?** If you can't name it, you're building a monitor, not a flywheel.

Good metrics: hit rate, auto-fix count, time-to-surface, false positive rate.
Bad metrics: "number of checks run" (activity, not quality).

## Implementation Pattern

```
[Real-time hooks]      → Tier 1 auto-fix + log
[Nightly LaunchAgent]  → reconcile + Tier 2 proposals + deeper checks
[Morning skill]        → surface Tier 2 proposals at decision point
[Weekly review]        → trend analysis + Tier 3 judgment calls
```

### Nightly runner design

- **Orchestrator script** calls individual checks sequentially
- Each check writes to a known output file
- Morning skill reads the file — checks don't need to know about surfacing
- **Auto-fix before reporting.** If sopor is stale, sync it, then report "auto-fixed." Don't report the problem and wait for human.
- **Fail open.** A check that errors should log the error and continue, never block other checks.

### Cost model

- Real-time hooks: pure code, ~5ms per message, zero token cost
- Nightly bash checks: <10s total, zero cost
- Nightly LLM reconciliation: one Haiku call, free on Max20
- Morning surfacing: one paragraph in auspex, negligible

Total daily cost: ~0. The flywheel runs on infrastructure you already pay for.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| **Log without reconciliation** | Write-only database. Nobody reads it, nothing improves. |
| **Alert on everything** | Alert fatigue → all alerts ignored. Tier 2 must batch, not interrupt. |
| **Human in the fix loop for obvious actions** | Restart a daemon doesn't need permission. Auto-fix. |
| **Reconcile without learning** | Same misses repeat. The fixer must feed back into the sensor. |
| **Over-instrument** | 50 checks with no action path = monitoring theater. Each check needs a tier assignment. |

## When NOT to build a flywheel

- **One-shot tasks** — no recurrence, no learning
- **Binary health checks** — pass/fail with no gradient to improve (keep as simple cron)
- **Judgment-heavy processes** — if >70% of the work is Tier 3, the flywheel adds overhead without value
- **Premature optimization** — build the cron first, observe for a week, then upgrade to flywheel if there's a feedback signal

## Calls

- `artifex` 14/14b — feedback loop checkpoint + flywheel identification
- `skill-review` 4b — skill suggest flywheel report
- Nightly runner: `~/.claude/hooks/nightly-run.sh`
