---
name: copia
description: Leverage agent teams to advance north star goals. Use when user says "copia", "burn tokens", "stellae", "expand north stars", "going to sleep", "overnight", "vigilia", or any variant of "burn tokens while I sleep" or "keep working while I'm away". Two modes — interactive (default) and overnight (unattended flywheel).
user_invocable: true
---

# Copia — Agent Teams for North Stars

One pattern: **north stars → division of labour filter → shapes filter → sub-goals → agent teams → results.** Two modes: interactive (Terry at keyboard) and overnight (unattended flywheel).

**Core principle:** The system exists to free Terry's attention for what SHOULD be done by a human — not what can't be automated, but what he chooses to keep. See [[division-of-labour]] for the five categories: Presence, Sharpening, Collaborative, Automated, Dropped. Copia only dispatches Automated tasks. The task space is infinite (north stars are continuous value streams). The stop criterion is budget, not task exhaustion.

## Pre-flight: Consumption Check

```bash
copia-gather preflight
```

This runs all deterministic pre-flight checks: consumption count (review queue), budget, guard status, manifest status, north star loading, TODO `agent:claude` items, and NOW.md state. Use `--json` for structured parsing.

The signal interpretation:

| Review queue | Signal | Action |
|---|---|---|
| **0-3** | Consumed. Produce more. | Run copia normally |
| **4-8** | Backlog building. | Produce only self-sufficient outputs (study materials, research answers). No drafts needing review. |
| **9+** | Overproduction. | **Don't produce.** Help Terry triage the queue — which items are stale? Which can an agent verify instead? Which need 5 min? |

**The goal is ~75% self-sufficient outputs.** If most outputs need review, the agent prompts are wrong — make them more specific so the output is finished on arrival.

**After each run:** Note in the vault report (`~/notes/Copia Reports/`) how many items were produced, how many self-sufficient vs. review-needed. Track the ratio. It should trend toward more self-sufficient over time.

## Core Protocol

### Step 0: Activate Guard

```bash
copia-gather guard on
copia-gather manifest init
```

The guard is a Stop hook (`~/.claude/hooks/copia-guard.py`). While active, the model **cannot stop** (budget green). Separate from the manifest so copia-loop doesn't accidentally activate the guard.

**To deactivate:** `copia-gather guard off` (done automatically in Wrap step, or manually by Terry).

### Step 1: Load Context (parallel reads)

- `~/notes/North Star.md` — the 6 priorities
- `~/notes/Reference/epistemics/north-star-shapes.md` — shapes framework
- `~/notes/Reference/epistemics/division-of-labour.md` — five-category filter
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

### Step 2b: Division of Labour Filter

Before brainstorming tasks, classify each candidate through [[division-of-labour]]:

| Category | Copia action |
|---|---|
| **Presence** (Theo, Tara, being there) | Skip — not agent work |
| **Sharpening** (drilling, reading source texts, forming views) | Skip — Terry does this to stay sharp |
| **Collaborative** (brainstorming, probing drills) | Skip — needs Terry at keyboard |
| **Automated** (research, synthesis, code, monitoring) | **Dispatch** |
| **Dropped** (doesn't serve a north star) | Drop — don't dispatch busywork |

Only Automated tasks enter the dispatch queue.

### Step 3: Brainstorm Sub-Goals

For each high-leverage star, identify sub-goals that:
- Are actionable NOW (not blocked, not future-dated)
- Fall in the Automated category
- Produce a concrete deliverable (research note, practice questions, draft, verification)
- Can be completed by an autonomous agent in one session
- Advance the north star meaningfully (not busywork)

**Sources (in priority order):**
1. TODO.md items tagged `agent:claude` or where research/drafting is the bottleneck
2. What the north stars need right now, even if not in TODO.md
3. External signals (lustro outputs, recent news, calendar proximity)
4. What wave N outputs revealed as the next logical step

The task space is infinite. If TODO.md looks empty, the north stars aren't — ask "what would a good employee working on [star] do next?"

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

After each wave completes, the orchestrator runs two phases:

**Phase A — Compound:** For each output, ask: **what builds on this?**
1. Reads all wave N outputs
2. Updates `~/tmp/copia-session.md` manifest
3. Research → synthesise into brief/draft
4. Draft → extract IP, publish via sarcio
5. Verification flagged issues → fix
6. Output reveals new sub-goal → add to next wave

**Phase B — Scout:** Ask: **what new directions does this reveal?**
1. What did we learn that changes the map? (e.g., theoria taxonomy reveals need for provision validator)
2. What external signals arrived? (check lustro outputs, recent news)
3. Given where we are now, what's the next highest-value Automated task toward each north star?
4. Are there north stars with zero dispatched tasks? Why?

**Compounding chain:** Research → Synthesis → IP/Publish → Verify → Cross-link

**Deliverables are functions, not documents.** If Terry asks for a market intel brief in 3 weeks, produce a fresh one — don't point to the stale file. Outputs represent a point-in-time answer, not a permanent artifact.

**Stop conditions (in order):**
- Budget turns yellow → finish current wave, then stop
- Budget turns red → stop immediately, report
- All remaining tasks require Presence, Sharpening, or Collaborative categories → stop (only human work remains)
- **Task exhaustion is NOT a stop condition.** If the north stars exist, Automated work exists. Scout harder before stopping.

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
| **Mechanism** | This skill (in-session) | `copia-loop` script (fresh session per wave) |
| **Clarifying questions** | Yes (max 1) | Forbidden |
| **Scope** | What user approves | Only what needs zero human judgment |
| **Agents per wave** | 3-5 | 8 (maintain thread pool) |
| **Waves** | 1-2 | Flywheel until budget turns yellow |
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

### Session Chain (interactive mode)

Session stays alive while background agents run. **Maintain 6-8 running at all times.** When count drops below 4, launch next wave immediately. Agent completions trigger new turns.

### Overnight: Use `copia-loop` Instead

For unattended overnight runs, **do not use this skill directly.** Use the `copia-loop` script:

```bash
copia-loop                    # 20 waves, $3/wave, opus
copia-loop --waves 50         # more waves
copia-loop --budget 5.0       # higher per-wave budget
copia-loop --model sonnet     # cheaper
```

**Why:** LLMs lose instruction-following energy as context grows. Each wave in a loop gets a fresh session with full kinetic energy. The manifest (`~/tmp/copia-session.md`) is the memory between waves. The shell loop is the guarantee — code, not a suggestion.

**Architecture:** Shell loop (real orchestrator) → fresh CC session per wave → agents → results → update manifest → exit → next wave. Budget check between waves is real code, not model judgment.

### Budget Checks

- Hook messages include "Budget: green/yellow/red"
- Green → keep launching. Yellow → finish current wave. Red → stop, send report.

### Stopping Gate (mandatory before any stop)

**Your instinct to stop is wrong.** The model's default is to wrap up and report. That instinct serves normal conversations, not overnight copia. You MUST pass this gate before stopping:

```
STOPPING GATE — answer all 6 before you're allowed to stop:

1. Is budget yellow or red?                          → if green, KEEP GOING
2. Have you checked ALL 6 north stars for Automated   → if any unchecked, scout it
   tasks in the last 2 waves?
3. Have you checked lustro/theoria for new signals?   → if not, check now
4. Have you checked the calendar for deadlines         → if not, check now
   within 14 days that need prep?
5. Did the last wave's outputs reveal ANY follow-on?  → if yes, dispatch it
6. Can you honestly say "a good employee serving       → if no, think harder
   these north stars would have nothing to do"?
```

**All 6 must clear to stop.** If even one fails, you have more work. The gate exists because you WILL want to stop before budget runs out. That's the model's conservatism, not judgment.

**Common rationalizations (these are NOT valid stop reasons):**
- "Diminishing returns" → you stopped scouting, not ran out of value
- "Better to wait for Terry's input" → overnight mode means no input. Keep going.
- "I don't want to over-produce" → consumption check handles this. Not your problem.
- "The remaining tasks are lower quality" → scout harder. Check a different north star.
- "I should report what we have" → report AFTER budget turns yellow, not before.

### Wrap

1. Update `~/notes/NOW.md` with results
2. `TeamDelete` if team was used
3. **Delete `~/tmp/.copia-guard-active`** — deactivates the stop guard
4. Archive `~/tmp/copia-session.md` to `~/tmp/copia-session-YYYY-MM-DD.md`
5. **List tmux panes, ASK Terry before killing any** — he has other live sessions

## Anti-Patterns

- **Meta-spiral:** Knowledge system work that doesn't serve stars 1-5
- **Habit displacement:** Building "health tracking" when shape says "go to the gym"
- **Shape mismatch:** Treating checklist as flywheel (over-engineering a finite problem)
- **Ignoring TODO.md:** Best sub-goals are often already queued there
- **Over-scoping agents:** Each agent = ONE deliverable
- **Inventing busywork:** Dispatch from north stars/TODO/scout phase. Tasks are discovered through navigation, not invented — but they must pass the division-of-labour filter (Automated category only)
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
6. **Diminishing returns per wave are real.** Waves 1-3 = high value. Wave 4+ = good. Wave 7+ = marginal. But this reflects poor scouting, not task exhaustion.
7. **Quality gate after Wave 3:** Would Terry pay $1-2 for this output? Does it save >10 min? Is it on the critical path? 2 of 3 = dispatch. 1 or 0 = scout harder before giving up.

### Evening session learnings (Mar 19)

8. **Task space is infinite.** North stars are continuous value streams. "Ran out of tasks" means "stopped looking." The employee analogy: a permanent position always has worthy work because the value stream is continuous.
9. **Scout phase between waves.** Don't just compound — ask "what new directions does this reveal?" Theoria taxonomy → provision validator. HSBC intel → specific vendor positioning. Outputs are navigation waypoints, not endpoints.
10. **Division of labour filter.** Five categories (Presence/Sharpening/Collaborative/Automated/Dropped). Only dispatch Automated. The system exists to free Terry's attention for what SHOULD be done by a human — a choice, not a technical limitation.
11. **Deliverables are functions.** "Give me the latest market intel" should produce a fresh brief, not reference a stale file. Point-in-time, not permanent.
12. **Lustro/theoria are terrain scanners.** They feed the scout phase with external signals. Broken pipelines = navigating by an outdated map.
13. **8 concurrent agents is achievable.** Tonight: 8 dispatched, 8 completed, 0 review items, 2 infra fixes. 100% self-sufficient rate.
