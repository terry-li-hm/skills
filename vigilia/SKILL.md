---
name: vigilia
description: Overnight autonomous sprint — burn tokens while Terry sleeps. Scans TODO.md for all actionable tasks, dispatches parallel agent waves, archives results, sends Telegram morning report. Use when Terry says "going to sleep", "overnight", "burn tokens while I sleep", "vigilia", or any variant of "keep working while I'm away".
user_invocable: true
---

# Vigilia — Overnight Autonomous Sprint

Latin: *vigilia* (night watch). Run when Terry is going to sleep and wants maximum autonomous work done overnight.

**Differs from `/copia`:** Copia is for interactive spare-budget sessions. Vigilia is for unattended overnight runs — no user interaction expected, morning report on completion.

**Field-tested:** First run Mar 18-19 2026. **89 tasks** across 9+ waves, 20+ agents. See `~/notes/TODO Archive.md` March 2026 entries for the full record.

## Protocol

### Phase 1: Triage (2 min)

**Start from North Star, not from TODO.md.** Read `[[North Star]]` first. For each of the 6 priorities, ask: "what would move the needle tonight?" Then check TODO.md for matching tasks. This is top-down (goals → tasks) not bottom-up (backlog → hope it's worthwhile).

1. Run `date` to confirm HKT time
2. Read `~/notes/North Star.md` — what matters most right now?
3. Read `~/notes/TODO.md` — match items to north star priorities
4. Read `~/notes/NOW.md` for active context
5. Classify every unchecked item into:

| Category | Criteria | Action |
|----------|----------|--------|
| **Tonight** | No physical access needed, no Terry judgment needed, no send/push to shared systems | Dispatch |
| **Prep** | Needs Terry's final action but research/drafting is autonomous | Draft and flag for review |
| **Blocked** | Needs physical access, external reply, or Terry's voice | Skip |

5. Prioritize: due soonest > highest impact > `agent:claude` tagged > untagged actionable > someday
6. **Taste filter: read `[[North Star]]` first.** Score each candidate against the 6 north star priorities (Theo, career, health, marriage, finances, knowledge system). Tasks that don't serve any priority are paperclips — skip regardless of due date. No terminal themes when exam prep is pending.
7. **Don't filter too aggressively.** Research, drafting, planning, and design are all fair game even for `agent:terry` items — just flag the output for Terry's review.

### Phase 2: Dispatch Waves

**Maintain 8 agents at all times.** Don't batch into discrete waves — backfill as each agent completes. Think of it as a thread pool, not sequential batches. When agent count drops to 5-6, immediately launch 2-3 more to refill.

**Use standalone background agents by default** (`run_in_background: true`, NO `team_name`). Only use Agent Teams when agents actually need to communicate (pipeline patterns). Standalone agents are headless (no tmux panes), avoid permission prompt issues, and are simpler to manage. **First run mistake:** kept adding agents to a team out of habit when none needed coordination — pure overhead.

**The lead's real job is taste, not logistics.** Agents execute well. The scarce resource is knowing what's worth solving. A researcher can investigate anything — but deciding whether "Perplexity theme" vs "GARP cheat sheet" deserves tokens is a judgment call only the lead (or Terry) can make. Curation > execution.

**Priority queue:**
- **Wave 1:** Highest-priority items (due within 3 days, urgent fixes, code/infra)
- **Wave 2:** Medium-priority (due within 2 weeks, research, GARP/HSBC deep-thinks)
- **Wave 3:** Financial/personal research (insurance, MPF, estate planning — things that take Terry hours but an agent does in minutes)
- **Wave 4+:** Prep docs (Day 1 briefs, cheat sheets, handover docs)
- **Wave 5+:** Someday items, designs, competitive intel, themes, skill improvements

**Overlap waves.** Don't wait for a full wave to finish before launching the next. As soon as ~half of a wave completes, launch the next wave. This maximizes throughput and maintains the session chain.

### Phase 2a: Agent Type Selection

**Standalone background agents** (`run_in_background: true`):
- Best for: independent tasks with no coordination needed
- Pros: headless (no tmux pane), no permission prompt issues
- Cons: can't use TaskList, can't message each other
- **Use for most tasks.** This is the default.

**Agent Teams** (`TeamCreate` + named teammates):
- Best for: coordinated work where agents should claim tasks from a shared list
- Pros: TaskList/TaskUpdate coordination, SendMessage between agents
- Cons: each teammate opens a tmux pane, can get stuck on permission prompts
- **Use sparingly.** Only when 3+ tasks in the same domain benefit from coordination.
- One team per leader — `TeamDelete` before creating a new team.

**Permission prompt handling (teams only):**
- Set `mode: auto` on all teammates to minimize prompts
- If agents get stuck, bulk-approve via tmux:
  ```bash
  # List agent panes
  tmux list-panes -a -F '#{pane_id} #{pane_title}' | grep -v 'Claude Code'
  # Send approval to all
  for p in %64 %65 %66 ...; do tmux send-keys -t "$p" "y" Enter; done
  ```
- Check pane status: `for p in <panes>; do echo "=== $p ===" && tmux capture-pane -t "$p" -p | tail -3; done`
- May need multiple rounds of `Enter` (for "Enter to confirm" dialogs)

### Phase 3: Archive Loop

**Critical — never skip this.** The archive is Terry's morning audit trail.

As each agent completes:
1. Read the result
2. **Classify stakes:**
   - **High** (client-facing, exam prep, financial decisions, code changes): → dispatch quality reviewer before archiving
   - **Medium** (designs, plans, research notes): → spot-check after every 2nd wave
   - **Low** (themes, intel, drafts, maintenance): → trust agent self-report, archive directly
3. **If high-stakes: review first.** Dispatch a reviewer agent with the output files. Reviewer returns PASS/AMBER/RED per item. Fix any AMBER/RED issues before archiving. This caught real errors in the first run (EU AI Act penalty 1%→1.5%, MAS acronym AIRM→AIRG).
4. **Archive first:** Append to `~/notes/TODO Archive.md` under current month (format: `- [x] **Title.** Brief result summary. \`done:YYYY-MM-DD\``)
5. **Then remove from TODO.md:** Delete or update the item (never leave `- [x]` in TODO.md — write-guard hook blocks it)
6. If the task generated a follow-up (e.g., "draft done, needs Terry review"), update the TODO item to reflect new status with `agent:terry`
7. Shut down completed team agents via `SendMessage` with `shutdown_request`

**Archive before remove.** If you try to mark `[x]` in TODO.md directly, the write-guard hook will block you. Always write to Archive first, then delete the line from TODO.

**Concurrent edits:** Agents may modify TODO.md or Archive simultaneously. If an edit fails with "File has been modified since read," re-read the file and retry.

### Phase 4: Budget Check

Between waves, check budget status:
- **Primary signal:** Hook messages include "Budget: green/yellow/red" on each user message
- **Secondary:** Ask Terry to run `/status` before sleeping, note the session % and weekly %
- **Session resets** at a fixed time each day (check via `/status`)
- **If green:** Keep launching waves
- **If yellow:** Finish current wave, don't launch more
- **If red:** Stop immediately, send report

**Rule of thumb from first run:** 9% session / 44% weekly after 42 tasks = very efficient. A full vigilia burns ~10-15% session, ~5-10% weekly.

### Phase 5: Morning Report

When all agents complete (or budget runs out), send via `deltos` (Telegram):

```html
<b>Overnight Sprint Report — N tasks completed</b>

<b>URGENT:</b> (anything needing immediate action today)

<b>Code & Infra (N):</b>
• bullet per completed item

<b>Research & Prep (N):</b>
• bullet per completed item

<b>Designs & Plans (N):</b>
• bullet per completed item

<b>Top 3 actions for today:</b>
1. Most urgent (with specific next step)
2. Second
3. Third
```

**Send the report as soon as the last high-priority wave finishes** — don't wait for someday items to trickle in. Terry will see it when he wakes up.

### Phase 6: Wrap

1. Update `~/notes/NOW.md` with overnight results
2. Clean up: `TeamDelete` if team was used
3. **List tmux panes and ASK Terry before killing any.** Never bulk-kill — Terry has other sessions that look identical to zombie agent panes. First run mistake: killed a live session thinking it was a zombie.
4. If session is still alive, suggest `/legatum checkpoint` for context preservation

## Anti-patterns

- **Don't create busywork.** Only dispatch tasks from TODO.md or clearly derivable from NOW.md. Never invent tasks to keep the chain alive.
- **Don't send messages.** WhatsApp, email, LinkedIn — all draft-only overnight. Never send on Terry's behalf.
- **Don't push to shared repos.** Personal repos (auto-push per CLAUDE.md) are fine.
- **Don't modify CLAUDE.md or settings.json** beyond registering things explicitly planned (like hooks from TODO items).
- **Don't skip archival.** Every completed task must be archived. No exceptions.
- **Don't be conservative.** The whole point is to burn budget productively. Launch 10 agents, not 3.
- **Drop tasks, don't just add them.** The lead's job includes saying "this isn't worth doing." Apply the North Star filter before dispatch — if a task doesn't serve any of the 6 priorities, drop it even if it's in TODO.md. Dropping a `someday` item is free. Dispatching an agent on it costs tokens and attention. First run mistake: launched HPV vaccine research and Pharos migration analysis when both were explicitly "after Capco."

## Session Chain Maintenance

The session stays alive as long as:
- Background agents are running (completions trigger new turns)
- Or there's user interaction

**To maintain the chain:** Always have at least 2-3 agents running. When a wave is ~60% done, launch the next wave. If budget is exhausted and no agents remain, the session naturally ends — that's fine.

## First Run Stats (Mar 18-19 2026)

| Metric | Value |
|--------|-------|
| Total tasks completed | **89** (41 on Mar 18, 48 on Mar 19) |
| Agents spawned | 20+ (standalone v1 + team v2 experiment) |
| Architecture tested | v1 standalone, v2 role-based team, v3 designed |
| Token budget (full run) | ~44% weekly, session reset mid-sprint |
| Quality reviewer dispatched | Yes — caught EU AI Act penalty 1%→1.5% error |

**Domain breakdown (by archive keyword frequency):**

| Domain | Items | Key outputs |
|--------|-------|-------------|
| GARP exam prep | 19 | 6 deep-think notes (500-700 lines each), cheat sheets |
| HSBC deliverables | 15 | 3 comprehensive draft deliverables (Terry review needed) |
| MCP infrastructure | 13 | praeses unified server (17 tools, 5 domains) |
| Skills & tooling | 12 | 15+ skills updated; cibus, vigilia v3, rector, copia |
| Hooks & LaunchAgents | 13 | AKM heartbeat, failures.md hook, meta-spiral guard |
| Consilium port | 10 | Phase 1 (config/model) + Phase 2 (direct API routing) |
| CLI/infra (cibus, qianli, elencho) | 11 | cibus OpenRice CLI, qianli Docker migration |
| Phron/AKM | 7 | AKM heartbeat fixed, phron retrieval hook |

**Session economics:** 89 tasks in ~9 hours unattended. Binding constraint shifted from execution capacity to curation by Wave 4. Quality reviewer ROI was clear — one catch prevented a real exam error.

## Learnings from First Run (Mar 18-19 2026)

1. **Standalone agents > team agents** for independent tasks. Team agents are only worth the tmux overhead when tasks need coordination.
2. **Financial/personal research** is extremely high-value — insurance comparisons, MPF analysis, estate planning that would take Terry hours takes an agent 5 minutes.
3. **"Prep" tasks are the sweet spot** — drafting deliverables, handover docs, cheat sheets, strategy briefs. Terry reviews in 5 min what took an agent 10 min to produce.
4. **GARP-style deep-thinks** work beautifully — agent produces 500-700 line substantive notes, Terry just needs a review pass.
5. **Archive loop is load-bearing** — without it, Terry wakes up to a mess. With it, he has a clean audit trail in TODO Archive.
6. **The session chain works** — agent completions keep triggering turns. No need for artificial keepalive.
7. **Permission prompts are the main risk** for team agents. Always set `mode: auto`. Have the tmux bulk-approve command ready.
8. **Send the Telegram report early** — don't wait for all someday items. The high-priority wave finishing is the natural report trigger.
9. **Diminishing returns are real.** Waves 1-4 = high-value (Terry saves hours). Waves 5-6 = good (designs, cheat sheets). Wave 7+ = marginal (themes, competitive intel). The bottleneck shifts from execution capacity to knowing what's worth completing.
10. **Quality reviewer is high-ROI.** Dispatch after high-priority waves. Caught a real exam-affecting error (EU AI Act 1% → 1.5%) that would have cost marks. Cohors "separation of authority" principle proven.

## Stop Criterion

**After Wave 3, run a value check before launching more.** Ask:

1. **Would Terry pay $1-2 for this output?** GARP cheat sheet = yes. Perplexity terminal theme = no.
2. **Does it save Terry >10 min of work?** Financial research = hours saved. Competitive intel on a startup = nice-to-have.
3. **Is it on the critical path to a deadline?** Due within 2 weeks = yes. Someday = no.

**Decision:**
- All 3 yes → dispatch
- 2 of 3 → dispatch if budget green
- 1 or 0 → stop, send report, wrap

**Alternative: Prospector agent.** Instead of manual judgment, dispatch a scoring agent that reads remaining TODO items and returns a ranked list with Value × Autonomy × Urgency scores. Only execute items scoring above threshold. This is the copia prospector pattern — steal it for vigilia after Wave 3.

## Pipeline Dispatch (agents talking to each other)

Parallel-independent is the default mode. But when tasks have natural input→output dependencies, use **pipeline dispatch** via Agent Teams. Teammates can SendMessage to each other and share TaskList.

### Pattern 1: Research → Synthesis

Use when multiple research outputs feed a single deliverable.

```
Wave A: 3 research agents (each produces a note)
         ↓ each sends key findings via SendMessage to synthesizer
Wave B: 1 synthesis agent (reads messages + notes, produces brief/deliverable)
```

**Setup:**
- Create team, spawn researchers + synthesizer
- Researchers: complete task, then `SendMessage(to="synthesizer", message="Key findings: ...")`
- Synthesizer: TaskList shows its task blocked by researcher tasks. Once unblocked, reads messages for in-context findings, reads full notes for depth.
- Use `addBlockedBy` on the synthesis task to enforce sequencing.

**Example from first run:** GARP deep-think agents → HSBC deliverables agent. Done manually (re-read files). Pipeline would pass findings in-context, saving tokens and improving coherence.

### Pattern 2: Build → Verify

Use when code needs testing after creation.

```
builder agent (writes code, marks task done)
         ↓ SendMessage to tester: "built at ~/code/foo/, run tests"
tester agent (runs tests, reports pass/fail)
         ↓ if fail: SendMessage to builder with error details
builder agent (fixes, re-notifies tester)
```

**Setup:**
- Two teammates: `builder` and `tester`
- Builder's task: implement feature
- Tester's task: blocked by builder's task
- On failure, tester creates new fix task and assigns to builder

### Pattern 3: Scout → Judge → Execute

Use when there are multiple viable approaches and you want evidence-based selection.

```
2 scout agents (research option A and B in parallel)
         ↓ each sends findings to judge
1 judge agent (compares using criteria, picks winner)
         ↓ sends decision to executor
1 executor agent (implements the chosen approach)
```

**Setup:**
- 4 teammates, 3 task dependencies
- Judge task blocked by both scout tasks
- Executor task blocked by judge task

### When to use pipelines vs parallel

| Signal | Use parallel | Use pipeline |
|--------|-------------|--------------|
| Tasks share no data | ✓ | |
| One task's output is another's input | | ✓ |
| Quality improves from feedback loops | | ✓ |
| Tasks are in different domains | ✓ | |
| Order matters (research before implementation) | | ✓ |
| Speed is the priority over quality | ✓ | |

### Practical notes

- Pipelines require Agent Teams (standalone agents can't message each other)
- Set `mode: auto` on all teammates
- Use `addBlockedBy` in TaskUpdate to enforce sequencing — agents won't claim blocked tasks
- Pipeline waves are slower (serial dependency) but produce higher-quality output
- Mix both: parallel for independent tasks, pipeline for dependent chains
- Budget cost: pipelines use slightly more tokens (message overhead) but produce better results

## Role-Based Team (v2 — untested)

Instead of 1-agent-per-task (disposable workers), run a persistent 5-agent team organized by role. Agents stay alive all session, picking tasks from a shared queue by role match.

### Roles

| Role | Model | Prompt focus | Picks tasks tagged |
|------|-------|-------------|-------------------|
| **researcher** | Sonnet | Web search, vault reads, produces structured findings | `role:research` |
| **writer** | Opus | Takes findings, produces client-facing deliverables/notes | `role:write` |
| **reviewer** | Opus | Quality gates: PASS/AMBER/RED per output, fixes before archive | `role:review` |
| **coder** | Sonnet | Implements code changes, builds tools, runs tests | `role:code` |
| **tester** | Sonnet | Smoke-tests code, verifies builds, reports pass/fail | `role:test` |

### Flow

```
Lead reads TODO → creates tasks with role tags → TaskList
  researcher picks research tasks → findings → SendMessage to writer
  writer picks write tasks → draft → SendMessage to reviewer
  reviewer gates → PASS: lead archives / AMBER: SendMessage back to writer
  coder picks code tasks → implementation → SendMessage to tester
  tester verifies → PASS: lead archives / FAIL: SendMessage back to coder
```

### Why this beats 1-agent-per-task

- **Context accumulation.** Researcher learns where things are in the vault. Coder learns codebase patterns. No cold start per task.
- **Built-in quality gate.** Reviewer sees everything before archive — errors caught systematically, not ad-hoc.
- **Less overhead.** 5 persistent agents vs 67 spawn/shutdown cycles.
- **Graceful degradation.** If coordination fails, each agent still completes tasks independently — falls back to v1 pattern.

### Free tool delegation (opifex pattern)

Role agents should prefer free/cheap tools over burning CC tokens:

| Role | Free tool | CC tokens for |
|------|-----------|---------------|
| researcher | `gemini` CLI, `noesis search` ($0.006) | Judgment on source quality |
| coder | `codex exec`, `opencode`, Gemini CLI | Architecture decisions, complex debugging |
| tester | Bash (direct command execution) | Interpreting ambiguous failures |
| writer | CC (needs Opus quality) | Everything — this is where quality matters |
| reviewer | CC (needs Opus judgment) | Everything — this is the quality gate |

Include this in each role's spawn prompt: "Prefer free tools (codex, gemini, opencode) for mechanical work. Use your CC tokens for judgment and quality."

### Setup

```
TeamCreate → "vigilia-roles"
Spawn 5 teammates: researcher, writer, reviewer, coder, tester
Each teammate's prompt: "You are the [role] on team vigilia-roles. Check TaskList for tasks tagged role:[your-role]. When done, SendMessage your output to [downstream role]. Then check TaskList again."
Lead creates all tasks upfront with role tags and blockedBy dependencies.
```

### When to use v1 (standalone) vs v2 (roles)

| Signal | v1 standalone | v2 role-based |
|--------|--------------|---------------|
| All tasks independent | ✓ | |
| Tasks have research→write→review flow | | ✓ |
| Code tasks need testing | | ✓ |
| <10 tasks total | ✓ | |
| >20 tasks, mixed types | | ✓ |
| Terry is asleep (no intervention) | Either — v2 higher quality, v1 higher throughput | |

### Lead discipline

The lead is a **dispatcher and archivist**, not a doer. When a role agent reports an issue:
- Reviewer finds format problem → reviewer fixes it, or messages writer to fix. Lead does NOT fix it manually.
- Tester finds test failure → tester messages coder. Lead does NOT debug.
- The lead's only jobs: create tasks, archive completed work, manage the team.

**First run mistake:** Reviewer reported AMBER issues, lead manually edited the files instead of letting the reviewer or writer handle it. Broke the role separation.

### Dynamic scaling

Not fixed 1-agent-per-role. Scale by queue depth:
- **Queue depth > 3** for a role → spawn a second agent for that role (e.g., `researcher-2`)
- **Queue depth = 0** for a role → let agent idle (it costs nothing idle) or shut it down
- **Reviewer stays at 1** — single reviewer is a feature, not a bottleneck. Forces all output through one quality gate.

Think k8s HPA: monitor queue, scale horizontally within roles, keep total agent count at ~8.

### Keep the pipeline loaded

Each role needs **3+ tasks queued** so no one idles. If a role finishes its task and the queue is empty, the agent goes idle and wastes a tmux pane.

**Rule: when any role's queue drops to 1, create 2 more tasks for that role.** Treat it like a Kanban WIP limit in reverse — minimum queue depth, not maximum.

**Write tasks need blocked-by dependencies.** Writer can't synthesize research that doesn't exist yet. Use `addBlockedBy` so writer tasks auto-unblock when researcher completes.

**Lead's job is queue management.** The lead doesn't do tasks — it watches TaskList and ensures every role always has work. If a role is idle, the lead either creates a new task or reassigns a task from an overloaded role.

### Roles are labels, not capabilities

"Researcher" and "writer" are human-legible labels on identical LLMs. The agent doesn't research better because you called it "researcher." What actually matters:
- **The prompt** (per-task, not per-role)
- **Separation of producer and checker** (different context catches errors self-review misses)

**Simpler architecture for v3:** N generalist workers (pick any task) + 1 check step (any agent reviewing another's output cold). No role labels needed. The check step is the only structural requirement — everything else is queue management.

### v3: Persistent Team (recommended default)

Spawn **once** at session start. Keep alive all session. Replace exhausted workers.

```
/vigilia → TeamCreate "vigilia"
  → spawn 8 generalist workers (Sonnet) + 1 checker (Opus)
  → feed tasks continuously from North Star → TODO.md
  → worker hits context limit (~3% until compact) → spawn replacement, shut down old
  → session end → shutdown all → TeamDelete
```

**Do not create/destroy teams per wave.** One team, always ready. The lead's only jobs: curate the queue, replace exhausted workers, archive results.

### v3 agents: Generalists + Checker

Simplest effective architecture. No roles, no pipelines, no idle time.

```
Lead (curates queue, archives results)
  → N generalist workers (Sonnet, pick any task, use free tools)
  → 1 checker (Opus, reviews high-stakes outputs cold)
```

**Worker prompt:** "Check TaskList. Pick the next unowned task. Complete it. Mark done. Check TaskList again. Use codex/gemini for mechanical work, save CC tokens for judgment."

**Checker prompt:** "Check TaskList for tasks tagged `needs-check`. Read the output file cold — you didn't produce it. Verdict: PASS/AMBER/RED. If AMBER/RED, fix it yourself or create a new fix task."

**Lead tags high-stakes tasks** with `needs-check` at creation time. Low-stakes tasks skip the checker entirely.

### Status: v1 tested Mar 18-19, v2 tested Mar 19, v3 designed Mar 19

Added Mar 19 2026 based on first run analysis. Test on next vigilia run and compare quality/throughput against v1.

## Vision: The Hybrid Agent Company

The end-state architecture for vigilia is a **hybrid agent company** where paid AI (CC) provides judgment and free AI (Codex/Gemini) provides labour.

```
┌─────────────────────────────────────────────────┐
│                    LEAD (CC Opus)                │
│         Taste · Curation · Queue mgmt           │
│              The only human-like job             │
└──────────────────┬──────────────────────────────┘
                   │ creates tasks, archives results
          ┌────────┴────────┐
          ▼                 ▼
┌──────────────┐   ┌──────────────┐
│  WORKERS     │   │   CHECKER    │
│  (CC Sonnet) │   │  (CC Opus)   │
│  N instances │   │  1 instance  │
│              │   │              │
│  • Pick task │   │  • Reviews   │
│  • Read code │   │    output    │
│  • Write spec│   │    cold      │
│  • Delegate→ │   │  • PASS/     │
│  • Review    │   │    AMBER/RED │
│  • Message   │   │  • Fixes or  │
│    checker   │   │    routes    │
└──────┬───────┘   └──────────────┘
       │ delegates mechanical work
       ▼
┌──────────────────────────────────┐
│     FREE LABOUR POOL             │
│                                  │
│  codex exec    (GPT-5.4, free)   │
│  gemini -p     (Gemini, free)    │
│  opencode      (any model, free) │
│                                  │
│  Invoked via subprocess          │
│  No team awareness               │
│  Output reviewed by CC worker    │
└──────────────────────────────────┘
```

### Cost model

| Layer | Token cost | % of work |
|-------|-----------|-----------|
| Lead (Opus) | $$$ | ~5% (curation, archival) |
| Workers (Sonnet) | $$ | ~15% (specs, review, routing) |
| Checker (Opus) | $$$ | ~5% (quality gate) |
| Free tools | $0 | ~75% (mechanical coding, research) |

**Target: 75% of implementation done by free tools, CC tokens spent only on judgment.**

### Worker delegation pattern

```
Worker picks task from queue
  → Reads existing code (CC tokens: understanding)
  → Writes a 3-line spec (CC tokens: judgment)
  → `codex exec --skip-git-repo-check "spec here"` (free)
  → Reviews output, fixes edge cases (CC tokens: review)
  → Messages checker with file paths
  → Checker reads cold, verdicts PASS/AMBER/RED (CC tokens: quality)
```

### What's missing (build incrementally)

1. **Persistent worker memory** — workers forget between sessions. A handoff journal per worker (`~/.agent-journals/worker-last-session.md`) would let context accumulate across vigilia runs.
2. **Cross-session task queue** — currently TaskList dies with the team. A durable TODO.md-backed queue would persist tasks across sessions.
3. **Auto-scaling** — lead manually spawns workers. An auto-scaler that monitors queue depth and spawns/kills workers would complete the "agent company" metaphor.
4. **Free tool routing** — workers should pick the best free tool per task (codex for coding, gemini for research, opencode for multi-file changes). Currently manual.
5. **Cost tracking** — measure actual CC tokens per task vs free tool tokens. Optimize the split.

### Key insight from first run

**Roles are labels, not capabilities.** The agents don't get better at research because you called them "researcher." What matters:
- The prompt (per-task instructions)
- Separation of producer and checker (different context catches errors)
- Delegation to free tools (CC for judgment, free for labour)

**Taste is the bottleneck.** When you can run 80+ tasks overnight, the binding constraint is knowing which tasks are worth running. The lead's job is curation — everything else can be automated.

## Relationship to Other Skills

- **`/copia`** — interactive token burning with prospector agents. Vigilia is unattended and more systematic.
- **`/legatum`** — session wrap. Run after vigilia if session persists.
- **`/kairos`** — situational snapshot. Vigilia's triage is similar but exhaustive.
- **`/overnight`** — async queue results. Check next morning.
