---
name: cohors
description: Agent team orchestration heuristics — task decomposition, team topology, context management, quality control, parallelism patterns. Reference skill consulted by copia, rector, mandatum when spawning agent teams.
disable-model-invocation: true
---

# Cohors — Agent Team Orchestration Heuristics

> *Cohors: Latin "cohort" — a unit that fights together.*
> Mined via fodina Tier 1. Field-validate across copia runs and rector delegations.

How to decompose, structure, and run agent teams for maximum throughput and output quality within a token-budgeted orchestrator (Claude Code Max20).

---

## 1. Task Decomposition

### The Right Unit of Work

An agent task should be **one deliverable with one verification criterion**. That's the atomic unit. Everything else is either too big (needs architectural decisions the agent lacks context for) or too small (coordination cost exceeds execution cost).

| Signal | Diagnosis | Action |
|---|---|---|
| Agent makes reasonable-but-wrong structural choices | Task too coarse — architectural decisions delegated | Split: you decide architecture, agent implements within it |
| Agent asks clarifying questions or stalls | Task too coarse OR ambiguous acceptance criteria | Tighten the spec, not the implementation details |
| You specified the function signature in the prompt | Task too fine — you did the intellectual work | Merge into larger deliverable, specify *what* not *how* |
| Agent output needs heavy editing to fit with other outputs | Merge boundary wrong — pieces don't compose cleanly | Redraw boundaries at natural seams (file, module, API surface) |
| Output is correct but disconnected from context | Insufficient context transfer | Add wiring instructions: "this output will be consumed by X" |

### Decomposition Heuristics

- **One output file per agent.** If two agents write to the same file, you need merge logic. Merge logic is where agent teams die.
- **Decompose by output, not by process step.** "Research X" + "Draft Y from research" = sequential dependency. "Draft Y (do your own research)" = single self-contained task. Prefer the latter unless research quality requires dedicated depth.
- **The 20-minute rule.** If a human couldn't verify the output in 20 minutes, the task is too big. If verification takes <1 minute, the task might be too small (unless it's part of a large parallel batch).
- **Dependencies are the enemy.** Every dependency between agents is a serialization point. Design tasks to be embarrassingly parallel. Accept some duplicated research across agents over shared research that serializes them.
- **Fan-out, merge-in.** The natural team shape is: lead decomposes → N agents work in parallel → lead merges. Not: agent A → agent B → agent C (pipeline). Pipelines waste tokens on handoff context.

### What's Too Big vs Too Small

| Too big | Right size | Too small |
|---|---|---|
| "Build the CLI" | "Implement the `--sync` subcommand with these 3 flags" | "Add the `--verbose` flag" |
| "Research AI governance landscape" | "Compare HKMA vs MAS AI guidance: key differences, gaps, timeline" | "Find HKMA's latest AI circular" |
| "Write the blog post series" | "Draft one post: [topic], [audience], [angle], 800-1200 words" | "Write the introduction paragraph" |
| Requires >1 architectural decision | Requires implementation decisions within fixed architecture | Requires no decisions at all |

---

## 2. Team Topology

### Flat vs Hierarchical

| Topology | When | Why |
|---|---|---|
| **Flat** (lead → all workers) | ≤5 agents, independent tasks, single output type | Coordination overhead is minimal; lead can hold all context |
| **Hierarchical** (lead → sub-leads → workers) | >5 agents, OR outputs must be consistent across groups, OR domain-specialist routing needed | Sub-leads enforce local consistency without flooding lead context |
| **Solo** (no team, just delegate) | Task is clearly one unit of work | Teams add coordination cost — don't pay it for single tasks |

**Default: flat.** Hierarchical adds a context-compression layer (sub-lead summarizes for lead), which loses signal. Only use when flat would require the lead to hold too much heterogeneous context.

### When a Team Lead Adds Value

A team lead is worth the overhead when:
- **Outputs must be synthesized**, not just concatenated. (Research from 4 agents → one coherent recommendation.)
- **Quality varies** and someone needs to filter. (3 of 5 drafts are good; lead picks and merges.)
- **Decomposition requires judgment.** (The user said "research X" — lead decides what "research" means for this X.)

A team lead is pure overhead when:
- Tasks are fully independent and outputs go directly to files.
- Verification is mechanical (tests pass, file exists, format correct).
- The user already wrote the full decomposition.

### Model Selection Within Teams

| Role | Model | Why |
|---|---|---|
| Lead / orchestrator | Opus | Judgment, synthesis, decomposition quality |
| Worker / executor | Sonnet | Cost-effective execution, follows specs well |
| Lookup / fact-finding | Haiku | Cheap, fast, good enough for retrieval |
| Reviewer / quality gate | Opus | Catches what Sonnet misses |

**Rule:** Don't use Opus for execution. Don't use Haiku for judgment. Match model capability to the cognitive demand of the role.

---

## 3. Context Management

### The Context Tax

Every token of context you give an agent is a token not spent on reasoning. Context is not free — it's a trade-off against output quality. The goal: **minimum viable context for correct output.**

### What's Load-Bearing vs Noise

| Load-bearing (always include) | Noise (omit unless specifically relevant) |
|---|---|
| Acceptance criteria — what does done look like? | Background on why you're doing this project |
| Constraints — what's off the table? | History of previous attempts |
| Output format — exact structure, filename, frontmatter | Compliments or motivation |
| Wiring — what consumes this output? | General principles the agent already knows |
| Gotchas — non-obvious things that will cause failure | Restating the obvious ("you are an AI assistant...") |

### Context Transfer Patterns

- **Spec-as-prompt.** The task prompt IS the spec. No separate "context" section. Write the prompt as if it's a work order for a contractor who's never met you.
- **File pointers over file contents.** "Read `/path/to/file.md` for the schema" beats pasting the schema into the prompt. Agents can read files; pasting wastes prompt tokens.
- **Output templates.** For structured output, include a literal template with placeholders. Agents follow templates more reliably than prose descriptions of format.
- **Anti-examples.** One example of bad output teaches more than three examples of good output. "Do NOT produce X because Y" is high-signal context.

### The Stranger Test

Before launching an agent, read your prompt and ask: "Would a competent stranger produce the right output from this prompt alone?" If no, the prompt is missing context. If yes but it's 2000 words, you included too much — cut the noise.

---

## 4. Quality Without Review

### Design for Correctness, Not for Catching Errors

Human review is expensive and doesn't scale. The goal is to make bad output structurally impossible, not to catch it after the fact.

| Pattern | How it works | When to use |
|---|---|---|
| **Output schema** | Specify exact structure (frontmatter fields, section headings, JSON shape) | Always for structured output |
| **Acceptance test in prompt** | "Your output must satisfy: [list]. Check each before responding." | Always — self-verification is free |
| **Negative constraints** | "Do NOT include: opinions, recommendations, anything not sourced" | When agent tends to over-generate |
| **Word/line limits** | "800-1200 words" or "≤50 lines" | Prevents verbose drift |
| **Verification command** | "After writing, run `python -c 'import json; json.load(open(\"out.json\"))'`" | For machine-parseable output |
| **Reference file** | "Match the style/structure of `/path/to/example.md`" | When consistency with existing corpus matters |

### Self-Verification Prompts

Embed these in the agent's task prompt:

```
Before finalizing, verify:
1. [ ] Output file exists at the specified path
2. [ ] Frontmatter matches the required schema
3. [ ] No sections are empty or contain placeholder text
4. [ ] Word count is within specified range
5. [ ] All claims have a source or are marked as heuristic
```

**Rule:** If you can't write a verification checklist for the task, the task is under-specified.

### The Calibration Problem

Agent output quality is bimodal: either the agent understood the task (good output) or it didn't (useless output). There's rarely a middle ground. This means:
- **One great prompt beats three mediocre retries.** Invest time in the prompt, not in retry loops.
- **If the first output is wrong, the prompt is wrong.** Don't retry with "try again, but better." Rewrite the prompt.
- **Pilot before parallel.** Run one agent first. If its output is good, fan out the rest with the same prompt pattern. If not, fix the prompt before wasting tokens on N bad outputs.

---

## 5. Parallelism Patterns

### When to Parallelize vs Sequence

| Parallelize | Sequence |
|---|---|
| Independent outputs (different files, different topics) | Output B depends on output A |
| Research on different subtopics | Draft → review → revise cycle |
| Multiple implementations to compare | Architecture decision → implementation |
| Batch processing (same task, different inputs) | When learning from agent A's mistakes improves agent B's prompt |

### File Conflict Avoidance

- **Golden rule: one agent, one file.** Never have two agents write to the same file.
- **If agents must contribute to the same artifact:** each writes a fragment file, lead merges. E.g., `research-agent-1.md`, `research-agent-2.md` → lead produces `research-synthesis.md`.
- **Worktrees for code.** If agents modify code in the same repo, use `lucus` to give each a git worktree. Merge at the git level, not the file level.
- **Append-only shared state.** If agents must share state, use an append-only file (each agent appends, none reads others' entries). This avoids read-write conflicts.

### Optimal Team Size

| Team size | Works for | Fails for |
|---|---|---|
| 1-2 agents | Simple tasks, focused research | Wastes parallelism opportunity |
| 3-5 agents | Sweet spot — manageable coordination, real throughput | Nothing, this is the default |
| 6-10 agents | Large batch jobs (same template, different inputs) | Heterogeneous tasks — lead can't hold context |
| >10 agents | Almost never worth it | Everything — coordination cost dominates |

**Default: 3-5 parallel agents.** This matches Max20's practical concurrency (token throughput, context management overhead).

### The Merge Problem

Merging N agent outputs into one coherent artifact is the hardest part of team orchestration. Heuristics:

- **If outputs are independent (different files), merging = concatenation.** Design for this.
- **If outputs must be synthesized, the lead does it.** Don't delegate synthesis to another agent — synthesis requires the context of all inputs.
- **Rank, don't merge, when outputs are competing.** If you ran 3 agents on the same task to compare approaches, pick the best one. Don't frankenstein them together.
- **Merge immediately.** Don't let fragment files accumulate. Merge as soon as all agents report, then delete fragments.

---

## 6. Failure Modes

### Token Waste Patterns

| Pattern | What happens | How to prevent |
|---|---|---|
| **Context bloat** | Prompt is 50% background the agent doesn't need | Stranger test — cut until it breaks, then add back |
| **Retry loops** | Agent fails, you retry with same prompt + "try harder" | Rewrite prompt, don't retry. If 2 retries fail, the task is wrong |
| **Exploration sprawl** | Agent researches broadly instead of answering narrowly | Constrain scope explicitly: "Only look at X, Y, Z" |
| **Premature parallelism** | 5 agents launch before you know the prompt works | Pilot one agent first, then fan out |
| **Monitoring overhead** | Lead spends more tokens checking on agents than agents spend working | Use TaskOutput, not conversational check-ins. Fire-and-forget with verification |
| **Over-decomposition** | 10 tiny tasks that could have been 3 | Each task should require at least one non-trivial decision by the agent |

### Coordination Overhead

Coordination cost grows superlinearly with team size. At some point, the lead spends more tokens coordinating than workers spend producing.

**Symptoms:**
- Lead's merge/synthesis output is longer than any individual agent's output
- More than 2 rounds of "let me check what agents produced"
- Lead rewrites >30% of merged output

**Fix:** Fewer, larger tasks. Give agents more autonomy, not less.

### Output Drift

Agents in a team produce stylistically inconsistent output. This is fine for independent deliverables but fatal for outputs that must read as one voice.

**Fixes:**
- Reference file: "Match the voice/style of this example"
- Style constraints in prompt: "Formal but not stiff. No bullet points. Active voice."
- Lead rewrites for consistency during merge (budget tokens for this)

### The "Good Enough" Trap

Agent output is often 70-80% of what a focused human session would produce. The question is whether the marginal 20-30% is worth the human time. Usually it isn't — for internal artifacts, knowledge base entries, research briefs, 80% quality at 10% human effort is the right trade.

**Exception:** Client-facing deliverables. These need the human pass. Design agent work to produce a strong draft, not a finished artifact.

---

## 7. The Copia Pattern — Speculative Autonomous Work

### Core Principle

Spare compute budget should be burned on work that compounds: research, knowledge extraction, content drafts, system health checks. The key property: **the task objective is derivable from existing artifacts** (vault, NOW.md, calendar, codebase) — no human input needed at launch time.

### Maximizing Hit Rate

Not all speculative work pays off. Heuristics for picking what to run:

| High hit rate | Low hit rate |
|---|---|
| Research on topics with upcoming deadlines (meetings, onboarding, exams) | Research on vaguely interesting topics with no near-term use |
| Knowledge consolidation of scattered existing notes | Creating new content with no existing raw material |
| System health checks that fix what they find | Audits that only produce reports |
| Drafts with clear audience and purpose | Drafts with "maybe someone will want this" |
| Refreshing stale artifacts (<30 days since last update is too fresh; >6 months is sweet spot) | Creating net-new artifacts with no template or precedent |

### The Bet Mental Model

Copia runs are bets, not assignments. Even if half produce mediocre output, the hits compound. This changes how you evaluate ROI:
- **Don't evaluate individual run quality.** Evaluate portfolio quality over a week.
- **Bias toward runs with learning value.** Even if the output is mediocre, did the process reveal something? (A stale note, a broken tool, a gap in coverage.)
- **Kill fast.** If a copia agent is clearly off-track (wrong interpretation, exploring dead end), TaskStop immediately. Don't let it burn tokens producing garbage.
- **Reuse prompts that worked.** When a copia run produces great output, save the prompt pattern. Next time you have spare budget, run the same pattern on a different topic.

### What to Run When

| Budget level | What to run | Why |
|---|---|---|
| **Flush** (weekly % < 30% by Wednesday) | Full copia menu — research, content, system health, knowledge consolidation | Maximum compound value |
| **Comfortable** (weekly % 30-50%) | Tier 1 research + knowledge consolidation | High-value, low-risk |
| **Tight** (weekly % 50-70%) | System health checks only (they fix things, immediate ROI) | Tangible, verifiable value |
| **Scarce** (weekly % > 70%) | Nothing speculative — reserve for user-directed work | Don't gamble with scarce budget |

### Anti-Patterns in Speculative Work

| Anti-pattern | What happens | Fix |
|---|---|---|
| **Report factory** | Agents produce reports nobody reads | Agents must produce *actionable artifacts* — files in the right place, with wiring to other systems |
| **Busywork disguised as leverage** | Running agents to feel productive | Every copia run must answer: "What decision or action does this enable that wasn't possible before?" |
| **Research without synthesis** | Raw findings dumped into vault | Lead must synthesize — or the research rots. Budget tokens for synthesis in every research copia run |
| **Stale queue** | Same copia items run repeatedly because they're "always relevant" | Rotate the menu. If an item has run 3 times without the output being used, drop it |

---

## Cross-References

- **mandatum** — theory of delegation, spec quality, decomposition depth
- **rector** — the on-ramp that decides when to spawn teams vs solo delegate
- **copia** — the speculative autonomous work menu (consumes cohors heuristics)
- **heuretes** — agent research org pattern (a specific team topology)
- **opifex** — the delegation executor (implements cohors decisions)
- **lucus** — git worktree manager for parallel agent isolation
- **verify** — hard gate for completion claims (quality control layer)
