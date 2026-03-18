---
name: kritike
description: Key considerations when evaluating — metric selection, Goodhart traps, vanity vs diagnostic, LLM eval patterns. Reference skill consulted by evals-skills, judex, peira, and when designing measurement systems. Not user-invocable.
version: 1
tags: [reference, evaluation, metrics, cognition]
disable-model-invocation: true
---

# Kritike — Theory of Evaluation

> *Kritike (κριτική): Greek "the art of judgment" — the faculty of discerning quality.*

Evaluation is **measuring the gap between what you have and what you want**. The hard part isn't measurement — it's choosing what to measure.

Reference skill. Consult when designing metrics, reviewing evaluation pipelines, or when a metric feels wrong but you can't articulate why.

## Structure of Every Evaluation

1. **Criterion** — what "good" means. Must be chosen BEFORE measurement, not after. Choosing after = cherry-picking.
2. **Measurement** — how you observe. Hierarchy: automated > manual > subjective. But subjective measurement of the right thing beats precise measurement of the wrong thing.
3. **Comparison** — against what? Baseline, previous version, absolute threshold, competitor. Measurements without comparison are meaningless.

## Goodhart's Law (The Central Problem)

> "When a measure becomes a target, it ceases to be a good measure."

Every metric is a proxy. You can't measure "quality" directly — you measure something correlated. The correlation holds until you optimize, then proxy and reality diverge.

**Defense:** portfolio of metrics hard to game simultaneously. Coverage + mutation testing + production error rate → gaming all three requires actually writing good tests.

## Vanity vs Diagnostic Metrics

| Type | Test | Examples |
|------|------|----------|
| **Vanity** | If +10%, would you change anything? If no → vanity | Total users, lines of code, test count |
| **Diagnostic** | If +10%, would you know what to fix? If yes → diagnostic | Error rate by endpoint, p99 latency, FPR by category |

Most dashboards are vanity. Most useful metrics are ugly, specific, and embarrassing.

## The Evaluation Paradox

Good evaluation requires knowing what "works" means. Knowing what "works" means requires deep problem understanding.

**Resolution:** iterate. First evaluation is crude. Using it teaches you what "good" means. Second is better. Don't wait for perfect — start measuring something and let the measurement teach you what to measure.

## Subjective Evaluation

For things that resist quantification (writing, UX, architecture): **structured subjectivity**.

- Define rubric with specific criteria
- Use multiple evaluators
- Inter-rater agreement IS the quality signal
- Disagreement is diagnostic — criterion isn't well-defined

LLM-as-judge = structured subjectivity. Not objective, but systematic and reproducible.

## LLM Evaluation Pattern

**Generator → Evaluator → Aggregator**

- System generates output
- Separate system (often LLM) evaluates against rubric
- Aggregator turns individual evaluations into actionable signal

**Trap: evaluating the evaluator.** LLM judge biases cascade. Need human calibration set — examples where humans rated output, against which judge is validated. See `evals-skills:validate-evaluator`.

## Failure Modes

| Failure | Description | Signal |
|---------|-------------|--------|
| **Metric fixation** | Optimizing metric, not the thing | Metric up, users don't notice |
| **Proxy decay** | Metric-reality correlation weakens | Trends stop predicting outcomes |
| **Streetlight effect** | Measuring what's easy, not what matters | Dashboard full, no insight |
| **Evaluation theater** | Going through motions | Reports produced, nothing changes |
| **Premature precision** | False confidence from precise wrong measurement | "95.3%" on unrepresentative test set |
| **Survival bias** | Only evaluating successes | No data on failures or filtered cases |

## Human vs Agent Evaluation

- **Humans:** holistic ("feels right"), integrates many criteria, inconsistent, doesn't scale
- **Agents:** consistent, scalable, blind to criteria not in rubric, systematically wrong in ways humans catch instantly
- **Hybrid:** agent evaluates at scale against rubric, human calibrates on a sample

## Agent Evaluation Patterns (Stolen from Specula 2026-03)

- **pass@k not pass@1.** Single-trial eval inflates agent performance. Tau-bench's pass^8 (solving 8 of 8 trials) reflects real reliability. An agent with 60% pass@1 might only achieve 10% pass^8. Always demand multi-trial evaluation.
- **Cost-of-pass metric.** Expected monetary cost per correct solution. 5% more accurate but 10x more expensive = worse product decision. Include in every agent evaluation.
- **Agent-as-judge > LLM-as-judge** for process evaluation (evaluating action chains, tool call sequences). Agent-as-judge disagrees with humans only 0.3% vs 31% for LLM-as-judge on code evaluation (arxiv:2508.02994).
- **Self-correction requires external signal.** LLMs cannot reliably self-correct reasoning without ground truth (Huang et al.). Don't prompt "check your reasoning." Give tools to test, search, calculate — let self-correction emerge from real signals.
- **Fresh-context self-review.** Review output in a clean context window — no contamination from generation (Osmani). Models subconsciously defend their own outputs.
- **TheAgentCompany ceiling.** Best agent = 30% on real workplace tasks. Use for client expectation management.

## When to Consult This Skill

- Designing metrics or KPIs — check for Goodhart vulnerability
- Building eval pipelines — generator→evaluator→aggregator pattern
- Metric feels wrong — check failure modes table
- Choosing between vanity and diagnostic — apply the +10% test
- LLM evaluation — structured subjectivity + human calibration
- Agent evaluation — pass@k, cost-of-pass, agent-as-judge patterns
