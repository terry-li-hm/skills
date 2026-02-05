---
name: parallel-council
description: Spawn 3 parallel expert agents to analyze a decision from different angles, then synthesize. Use when facing a high-stakes decision that benefits from structured multi-perspective analysis. Different from /frontier-council (which uses different models) — this uses different expert roles within Claude.
---

# Parallel Council

Spawn 3 expert agents simultaneously, each analyzing the same decision from a different angle. Synthesize into a single recommendation with explicit disagreements.

## When to Use

- High-stakes career, financial, or strategic decisions
- When you need *depth from multiple angles*, not just *different AI opinions*
- Complements `/frontier-council` — use both for maximum coverage

**Use `/frontier-council` instead when:** You want different models' reasoning styles.
**Use this instead when:** You want structured expert analysis from specific angles.

## Triggers

- "parallel council", "council on [topic]"
- "analyze this from multiple angles"
- "I need perspectives on [decision]"

## Default Panels

### Career Decisions (default)

| Agent | Role | Focus |
|-------|------|-------|
| **Strategist** | Negotiation & positioning | Leverage, timing, counter-offers, signalling |
| **Analyst** | Market & compensation | Benchmarks, demand signals, role trajectory |
| **Auditor** | Risk & downside | What can go wrong, contractual traps, reputation risk |

### Technical Decisions

| Agent | Role | Focus |
|-------|------|-------|
| **Architect** | System design | Scalability, maintainability, trade-offs |
| **Pragmatist** | Delivery & timeline | What ships fastest, what's overengineered |
| **Critic** | Failure modes | Edge cases, security, what breaks at scale |

User can also specify custom panels.

## Workflow

### 1. Gather Context

Before spawning agents, assemble the full context package:

- **The decision:** What's being decided, in one sentence
- **Options:** The concrete choices (A vs B vs wait, etc.)
- **Constraints:** Timeline, budget, relationships, irreversibility
- **Background:** Relevant vault context (pipeline, comp, signals)

Read from vault as needed:
```
/Users/terry/notes/Active Pipeline.md
/Users/terry/notes/Job Hunting.md
/Users/terry/notes/CLAUDE.md
```

### 2. Spawn 3 Agents in Parallel

Use the Task tool with `subagent_type: "general-purpose"`. Launch all 3 in a **single message** for true parallelism.

Each agent gets:
- The full context package (same for all 3)
- Their specific role and focus area
- Instructions to write analysis to a specific vault path

**Prompt template for each agent:**

```
You are the [ROLE] on a decision council. Your focus: [FOCUS AREA].

## Decision
[The decision]

## Options
[Options A, B, etc.]

## Context
[Full context from vault]

## Your Task
Analyze this decision ONLY from your angle ([FOCUS AREA]).
Be specific — use numbers, dates, and concrete scenarios.
Do NOT try to be balanced or cover all angles. That's the other agents' job.
Your job is to go deep on your specialty.

Write your analysis as markdown with these sections:
- **Assessment** (2-3 paragraphs, your expert view)
- **Key Risk/Opportunity** (the single most important thing from your angle)
- **Recommendation** (what you'd advise, stated clearly)
- **Confidence** (high/medium/low, with reasoning)

Save the analysis to: /Users/terry/notes/council/[SESSION]/[ROLE].md
```

### 3. Synthesize

After all 3 agents complete, read their outputs and create a synthesis:

```markdown
# Council Synthesis: [Decision Topic]
**Date:** [today]

## The Decision
[One sentence]

## Agent Recommendations
| Agent | Recommendation | Confidence |
|-------|---------------|------------|
| Strategist | [recommendation] | [level] |
| Analyst | [recommendation] | [level] |
| Auditor | [recommendation] | [level] |

## Where They Agree
[Points of consensus]

## Where They Disagree
[Explicit disagreements with each side's reasoning]

## Synthesis Recommendation
[Final recommendation, weighted by confidence and reasoning quality]

## What Would Change This
[Conditions that would flip the recommendation]
```

Save to: `/Users/terry/notes/council/[SESSION]/synthesis.md`

### 4. Present to Terry

Show the synthesis in chat. Link to the full agent analyses in vault for deep-dives.

## Session Naming

Use format: `YYYY-MM-DD-[topic-slug]`
Example: `2026-02-06-capco-vs-dbs`

Directory: `/Users/terry/notes/council/2026-02-06-capco-vs-dbs/`

## Example

**Terry:** "Should I negotiate harder on the signing bonus or accept and start early?"

**Council spawns:**
1. **Strategist** — analyzes leverage position, what pushing signals, relationship risk with Gavin
2. **Analyst** — models the financial difference (signing bonus NPV vs. earlier start = earlier comp)
3. **Auditor** — checks contract terms, what happens if they rescind, reputation risk in consulting market

**Synthesis:** "All three agents recommend accepting. Strategist notes low leverage post-signing. Analyst shows the 2-week earlier start nets more than a likely signing bonus. Auditor flags that pushing post-acceptance can signal difficult-to-work-with in consulting."

## Chaining with /frontier-council

For maximum coverage on critical decisions:
1. Run `/parallel-council` first (depth from expert angles)
2. Take the synthesis and run `/frontier-council` on it (stress-test with different models)
3. Final decision note combines both
