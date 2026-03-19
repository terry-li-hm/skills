---
name: copia
description: Leverage agent teams to advance north star goals. Use when user says "copia", "burn tokens", "stellae", "expand north stars", "going to sleep", "overnight", "vigilia", or any variant of "burn tokens while I sleep" or "keep working while I'm away". Two modes — interactive (default) and overnight (unattended flywheel).
user_invocable: true
---

# Copia — Agent Teams for North Stars

One pattern: **north stars → shapes filter → sub-goals → agent teams → results.** Two modes: interactive (Terry at keyboard) and overnight (unattended flywheel).

## Pre-flight: Consumption Check

Before producing anything, measure whether previous output was consumed:

```bash
grep -c 'agent:terry.*Review' ~/notes/TODO.md
```

Count only genuine review items (tagged `agent:terry` AND contain "Review"). Physical actions, study tasks, and passive tracking don't count — they're normal TODOs.

| Review queue | Signal | Action |
|---|---|---|
| **0-3** | Consumed. Produce more. | Run copia normally |
| **4-8** | Backlog building. | Produce only self-sufficient outputs (study materials, research answers). No drafts needing review. |
| **9+** | Overproduction. | **Don't produce.** Help Terry triage the queue — which items are stale? Which can an agent verify instead? Which need 5 min? |

**The goal is ~75% self-sufficient outputs.** If most outputs need review, the agent prompts are wrong — make them more specific so the output is finished on arrival.

**After each run:** Note in the vault report (`~/notes/Copia Reports/`) how many items were produced, how many self-sufficient vs. review-needed. Track the ratio. It should trend toward more self-sufficient over time.

## Core Protocol

### Step 1: Load Context (parallel reads)

- `~/notes/North Star.md` — the 6 priorities
- `~/notes/Reference/epistemics/north-star-shapes.md` — shapes framework
- `~/notes/NOW.md` — current state
- `~/notes/TODO.md` — actionable items (head 80 lines)
- `date` — current time

### Step 2: Map & Filter by Shape

| Shape | Agent Leverage | Action |
|---|---|---|
| **Flywheel** | High | Produce, compound, measure |
| **Checklist** | High | Research sprint, then done |
| **Decision** | Medium | Research phase only |
| **Habit** | Near-zero | **SKIP** — do the thing |
| **Attention** | Near-zero | **SKIP** — be present |

Current star→shape mapping:

| North Star | Shape | Typical agent work |
|---|---|---|
| Career worth having | Flywheel | IP production, engagement prep, exam materials, research briefs |
| Financial resilience | Checklist | Fund verification, migration research, one-shot then done |
| Raise Theo well | Decision + Attention | School research (decision phase only) |
| Protect health | Habit | **SKIP** |
| Strengthen marriage | Attention | **SKIP** |
| Knowledge system | Meta-flywheel | Only if it serves stars 1-5 |

### Step 3: Brainstorm Sub-Goals

For each high-leverage star, identify 1-2 sub-goals that:
- Are actionable NOW (not blocked, not future-dated)
- Produce a concrete deliverable (research note, practice questions, draft, verification)
- Can be completed by an autonomous agent in one session
- Advance the north star meaningfully (not busywork)

Prioritise TODO.md items tagged `agent:claude` or where research/drafting is the bottleneck.

### Step 4: Align & Dispatch

**Interactive:** Show mapping table, ask ONE clarifying question if ambiguity would waste an agent run. Cap at 3-5 teams.

| Team | North Star | Shape | Sub-goal | Deliverable |
|---|---|---|---|---|

**Overnight:** Classify TODO items into Tonight (fully autonomous) / Prep (draft for Terry review) / Blocked (skip). Dispatch autonomously — no questions.

### Step 5: Execute Wave

Launch agents with `run_in_background: true`, `mode: bypassPermissions`.

Each agent prompt includes:
- Clear deliverable (file path + format)
- Context file paths to read
- `Read ~/tmp/copia-session.md first. Do not duplicate completed work.`
- Whether to research-only or write code
- Output format (frontmatter, structure, length target)

**Model routing:**
- Research/collection → `model: "sonnet"`
- Content/synthesis/judgment → `model: "opus"`
- System audits → `model: "sonnet"`

**File scoping:** Non-overlapping. One agent, one output file. No parallel edits to same file.

### Step 6: Flywheel (Overnight Mode)

After each wave completes, the orchestrator:

1. Reads all wave N outputs
2. Updates `~/tmp/copia-session.md` manifest
3. For each output, asks: **what compounds from this?**
   - Research → synthesise into brief/draft
   - Draft → extract IP, publish via sarcio
   - Verification flagged issues → fix
   - Output reveals new sub-goal → add to next wave
4. If viable wave N+1 tasks exist → dispatch next wave
5. If not → stop, report

**Compounding chain:** Research → Synthesis → IP/Publish → Verify → Cross-link

**Stop conditions:**
- No wave N output produces a viable wave N+1 task (work exhausted)
- Budget turns yellow/red
- Quality gate fails on critical output
- Max waves safety cap (~5-6)

### Step 7: Route Outputs

**Default: self-sufficient.** Most agent output should be usable on arrival — no review needed. Design agent prompts to produce finished work, not drafts-awaiting-approval.

```
Agent completes
  ├─ Self-sufficient (the default — ~75% of outputs)
  │     Study materials → use directly (GARP drills, cheat sheets)
  │     Research answers → reference (IBKR verification, intel briefs)
  │     Meeting prep → read on phone before meeting
  │     Archive to TODO Archive.md. No TODO item.
  │
  └─ Needs Terry's judgment (~25% of outputs)
        Only when: Terry's voice (content to publish), Terry's memory
        (verify facts only he knows), or Terry's hands (physical action).
        → vault note exists (the deliverable)
        → add TODO item: "Review: [title]. [path]. [what to check]." agent:terry
```

**`agent:terry` is expensive.** Every tagged item competes for Terry's attention with real work. Before tagging, ask: could another agent verify this instead? Is this really review, or is it studying/doing? If an agent can handle it, the agent should handle it.

**What is NOT `agent:terry`:**
- Study tasks ("test exam recall") → belongs in study schedule, not review queue
- Mechanical verification ("run lacuna preflight") → agent can do this
- Physical actions ("book physio") → normal TODO, no agent tag needed
- Passive tracking ("field validation over 4 weeks") → not a TODO at all

**Agents never block on Terry's review.** The flywheel keeps spinning. Wave 2 uses wave 1 outputs as-is — if Terry corrects later, the correction propagates forward naturally.

**One inbox:** TODO.md is the only review queue. Terry processes `agent:terry` items in priority order alongside everything else.

### Step 8: Session Report (vault)

At end of run, write `~/notes/Copia Reports/YYYY-MM-DD.md`:

```markdown
---
title: "Copia Report — [date]"
date: [ISO date]
tags: [copia, report]
waves: [N]
items_produced: [N]
items_for_review: [N]
---

# Copia Report — [date]

## Produced
- [file path] — one-line summary. Status: ✓ archived / 🔍 review queued

## Review Queue (in TODO.md)
- Review: [title] — what Terry should check

## Flywheel Trace
Wave 1 → [what was produced]
Wave 2 → [what compounded from wave 1]
...

## Quality Gate Results
[PASS/PARTIAL/FAIL per wave]
```

**No TG.** TODO.md is the one inbox. Terry finds review items there alongside everything else. No separate notification channel.

## Mode Differences

| | Interactive | Overnight |
|---|---|---|
| **Trigger** | "copia", "burn tokens", "stellae" | "overnight", "vigilia", "going to sleep" |
| **Clarifying questions** | Yes (max 1) | Forbidden |
| **Scope** | What user approves | Only what needs zero human judgment |
| **Agents per wave** | 3-5 | 8 (maintain thread pool) |
| **Waves** | 1-2 | Flywheel until work exhausts |
| **Shared systems** | Ask first | Never touch (no sends, no pushes) |
| **Output routing** | Same (vault + TODO) | Same (vault + TODO) |
| **Report** | Vault note (inline summary optional) | Vault note only |
| **Archive** | Optional | Mandatory (TODO Archive.md) |

## Manifest — Coordination Across Waves

`~/tmp/copia-session.md` — ephemeral, one per run. The orchestrator maintains it; every agent reads it first.

```markdown
# Copia Session — [date]
## Completed
- [wave 1] ~/notes/Research/X.md — topic summary ✓
- [wave 1] ~/notes/GARP/Y.md — 25 MCQs ✓
## In Progress
- [wave 2] Synthesizing X → garden post
## Not Started
- LinkedIn draft from garden post
```

Every agent prompt starts: **"Read ~/tmp/copia-session.md. Do not duplicate completed work. Build on listed outputs."**

## Quality Gate

Run after each wave, before flywheel check. **Mandatory for:** exam prep, client-facing research, skill files, anything published without human review. **Optional for:** system checks, drafts marked for editing.

Dispatch a Sonnet verification agent. Checks five dimensions:

| Dimension | PASS | FLAG | FAIL |
|---|---|---|---|
| **Source fidelity** | All claims sourced | 1-2 unsourced but plausible | Fabricated citations |
| **Internal consistency** | No contradictions | Legitimate nuance | Direct contradiction |
| **Hallucination scan** | All verifiable | Unable to verify | Invented citation |
| **Obsidian hygiene** | Links resolve, tags match | 1-2 broken links | Systematic errors |
| **Domain accuracy** | Matches authoritative sources | Simplification | Wrong exam answer |

Verdict routing: PASS → proceed. PARTIAL → proceed, flag for Terry. FAIL → quarantine (`_UNVERIFIED` prefix), report.

## Execution Patterns

**Standalone background agents (default).** `run_in_background: true`, no team. Best for independent tasks. Headless, no tmux panes, no permission issues.

**Agent Teams** (when agents need coordination). `TeamCreate` + named teammates. Use for pipeline patterns (research → synthesis → review). Set `mode: auto` on all teammates.

**Hard numbers (from field testing):**
- Opus lead + Sonnet workers = +90.2% over single Opus
- 3-4 workers max before coordination overhead eats gains
- Task sweet spot: 5-15 min per task
- A full overnight run burns ~10-15% session, ~5-10% weekly

**Pipeline dispatch** (when wave outputs feed other agents):
```
Research agents → SendMessage findings → Synthesis agent → Checker
```
Use `addBlockedBy` on dependent tasks. Pipelines are slower but higher quality.

## Overnight Specifics

### Archive Loop (never skip)

As each agent completes:
1. Read result, classify: **self-sufficient** or **needs review**
2. High-stakes → dispatch quality reviewer first
3. Self-sufficient → archive to `~/notes/TODO Archive.md`, remove from TODO.md
4. Needs review → add `- [ ] **Review: [title].** [path]. [what to check]. \`agent:terry\`` to TODO.md
5. Update manifest (`~/tmp/copia-session.md`)
6. **Keep going.** Never wait for Terry to review before starting next wave.

**Archive before remove.** Always. Write-guard blocks `[x]` in TODO.md.

### Session Chain

Session stays alive while background agents run. Maintain 2-3 running at all times. When count drops to 1, launch next wave. Agent completions trigger new turns — no artificial keepalive needed.

### Budget Checks

- Hook messages include "Budget: green/yellow/red"
- Green → keep launching. Yellow → finish current wave. Red → stop, send report.

### Wrap

1. Update `~/notes/NOW.md` with results
2. `TeamDelete` if team was used
3. **List tmux panes, ASK Terry before killing any** — he has other live sessions

## Anti-Patterns

- **Meta-spiral:** Knowledge system work that doesn't serve stars 1-5
- **Habit displacement:** Building "health tracking" when shape says "go to the gym"
- **Shape mismatch:** Treating checklist as flywheel (over-engineering a finite problem)
- **Ignoring TODO.md:** Best sub-goals are often already queued there
- **Over-scoping agents:** Each agent = ONE deliverable
- **Inventing work:** Only dispatch from north stars/TODO. Never create tasks to keep the chain alive
- **Sending messages:** WhatsApp, email, LinkedIn — draft-only. Never send.
- **Pushing to shared repos:** Personal repos fine. Shared = ask first.
- **Skipping archive (overnight):** Every completed task must be archived

## Field-Tested Learnings (Mar 18-19 2026)

First vigilia run: **89 tasks**, 9+ waves, 20+ agents, ~44% weekly budget.

1. **Standalone > team** for independent tasks. Teams only when coordination needed.
2. **Financial/personal research** = extremely high-value. Hours of Terry's time → 5 min agent work.
3. **Prep tasks are the sweet spot** — drafts, handovers, cheat sheets. Terry reviews in 5 min.
4. **Taste is the bottleneck.** After Wave 3, the constraint is knowing what's worth running.
5. **Quality reviewer is high-ROI.** Caught EU AI Act penalty error (1%→1.5%) before it entered vault.
6. **Diminishing returns are real.** Waves 1-3 = high value. Wave 4+ = good. Wave 7+ = marginal.
7. **Stop criterion after Wave 3:** Would Terry pay $1-2 for this output? Does it save >10 min? Is it on the critical path? 2 of 3 = dispatch. 1 or 0 = stop.
