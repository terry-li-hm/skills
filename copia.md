---
name: copia
description: Token abundance recipe — high-value autonomous tasks (research, content, knowledge consolidation, pre-drafting, audits) to run when Max20 budget is plentiful. Use when user says "copia", "burn tokens", "spare tokens", "use up budget", or when weekly % < 50% mid-week.
user_invocable: true
---

# Copia — Burning Token Abundance

When Max20 budget is plentiful (weekly % < 50% by Wednesday, or user says so), launch high-value autonomous work that requires zero user involvement. The key property: **objective is derivable from vault/NOW.md/calendar — no Terry input needed.**

## Pre-flight

1. Check budget: `/usus` or `/status` — confirm weekly % leaves room for 3-5 parallel agents
2. Check what's stale: scan `~/notes/Research/` — anything >30 days old is a refresh candidate
3. Check NOW.md for open items that benefit from research

## Step 0 — Prospecting (meta-burn)

Don't pick from the menu blindly. **Dispatch 2 prospector agents first** to find the highest-value work:

1. **Vault prospector** (Opus) — scans TODO.md, NOW.md, daily notes, Capco Transition, GARP/, solutions KB, skills/, Research/, LinkedIn Content Ideas. Scores each candidate on Value (1-5) × Autonomy (1-5). Returns ranked top 10 with ready-to-dispatch prompts.

2. **Activity prospector** (Opus) — scans git logs (last 2 weeks across officina, skills, ~/code/*), recent session history (~/.claude/projects/), stale branches, recurring friction patterns. Finds abandoned threads and unfinished work. Same scoring.

Both run ~2-3 min. Merge their lists, dedupe, pick the top 5-6 to dispatch. This avoids burning tokens on "looks useful" when "actually needed" items exist.

**Scoring dimensions:**
- **Value** (1-5): How much does completing this help right now?
- **Autonomy** (1-5): Can an agent do this without human input?
- **Compound potential** (1-3): Does the output feed future burns? 1 = terminal (read once, done), 2 = reusable (reference material), 3 = generative (seeds new work, enriches prospector scans, creates new tasks). Weight: V × A × C.

**Model routing by taste requirement:**
- **Sonnet** → clear spec, binary success (compile, find, format, collect)
- **Opus** → output needs judgment (when to deviate from prompt), taste (noticing what's missing), or voice (human reads without editing). If the output would embarrass Terry in front of a client or on LinkedIn, it needs Opus.

**When to skip prospecting:** If Terry names specific tasks, or if budget is tight (<20% remaining) — just pick from the menu directly.

## The Menu

Pick based on current priorities. All run as **background agents on Max20** (zero API cost). Bet mentality: even if half the output is mediocre, the hits compound.

### Tier 1 — Always High Value
These compound over time. Run whenever budget allows.

| Task | Output | Agent prompt focus |
|------|--------|--------------------|
| **HSBC engagement prep** | `HSBC AI Governance Brief.md` | Annual report, HKMA circulars, AI strategy, key people, Capco opportunities |
| **APAC regulatory landscape** | `APAC AI Regulatory Landscape.md` | Cross-jurisdiction comparison (HKMA, MAS, APRA, JFSA), upcoming regulation, gaps |
| **Competitor intelligence** | `AI Governance Competitor Landscape APAC.md` | McKinsey/Deloitte/Accenture/EY/PwC offerings, APAC presence, differentiation |
| **AI landscape deep-dive** | `AI Landscape Deep Dive.md` | Beyond weekly dialexis — emerging tools, model releases, industry shifts |

### Content Generation
Garden is zero-touch. Objective derivable from vault. Save to `~/notes/Writing/Blog/Published/` via `sarcio new`.

| Task | Source | Output |
|------|--------|--------|
| **Garden batch** | Scan vault for insights that deserve posts | 3-5 draft posts via `sarcio new`, `draft: false` |
| **LinkedIn posts from garden** | Recent garden posts | 2-3 LinkedIn drafts amplifying published posts |
| **Consulting thought pieces** | Research briefs → opinionated takes | Garden posts positioned for Capco credibility |

### Knowledge Consolidation
Turn scattered notes into structured references. Fully autonomous — objective = "connect what's fragmented."

| Task | Source | Output |
|------|--------|--------|
| **Topic consolidation** | 5-10 fragmented notes on same topic | One coherent reference note with dense wikilinks |
| **Framework extraction** | Repeated patterns across vault | Standalone framework note (e.g., governance patterns, regulatory comparison templates) |
| **Stale note refresh** | Notes >6mo old with active topics | Updated content, new links, pruned dead references |

### Pre-drafting
Artifacts Terry will need soon. Objective derivable from calendar + `[[Capco Transition]]` + NOW.md.

| Task | When | Output |
|------|------|--------|
| **Capco intro talking points** | Pre-onboarding | `~/notes/Capco/Intro Talking Points.md` |
| **Engagement frameworks** | Post-research | Templates: discovery questions, governance assessment checklist |
| **Meeting prep packs** | Before known meetings | Combine research + vault context into pre-read |
| **GARP RAI deep-dives** | Exam approaching | `GARP/` subfolder, one brief per weak domain |

### Situational Research
Run when specific context is active.

| Task | When | Output |
|------|------|--------|
| **Client/prospect research** | Pre-engagement | `Research/<Company> Brief.md` |
| **Job market intelligence** | Active search | Role patterns, salary benchmarks, demand signals |

### System Self-Healing
Low urgency but good use of spare tokens. Agents that fix, not just flag.

| Task | Output |
|------|--------|
| **CLI health sweep** | Parallel agents verify every `~/code/` tool builds, tests pass, skill matches binary — fix what they can |
| **Vault link repair** | `nexis` scan → agents fix broken wikilinks, not just report |
| **Solutions KB refresh** | Verify `~/docs/solutions/` entries still accurate, update outdated ones |
| **Skill drift fix** | Compare skill description vs binary `--help`, update mismatches |

## Execution Pattern

**Desktop (Ghostty/tmux): use agent teams.** One team lead (Opus) dispatches 3-4 workers. Lead manages coordination, file scope, and task assignment. See `cohors` skill for full orchestration heuristics.

**Blink/mobile: use in-process teams.** Set `"teammateMode": "in-process"` in settings or launch with `claude --teammate-mode in-process`. Same team coordination, no tmux panes — teammates run inline. Shift+Down to cycle between them.

```
# 1. Create team
TeamCreate(team_name="copia", description="Token burn session")
# 2. Create tasks from menu above
TaskCreate(subject="...", description="...")  # one per item
# 3. Spawn lead agent with team_name="copia"
Agent(name="lead", team_name="copia", run_in_background=true)
# Lead spawns its own workers
```

**Hard numbers (from research):**
- Opus lead + Sonnet workers = +90.2% over single Opus
- 3-4 workers max before coordination overhead eats gains
- 2 diverse models > 16 homogeneous (uncorrelated errors matter more than count)
- Task sweet spot: 5-15 min per task, 5-6 tasks per teammate
- Expect ~15x tokens vs single chat; plan budget accordingly

**Model routing:**
- **Research/collection** → `model: "sonnet"` (saves Opus quota)
- **Content/synthesis/judgment/mining** → `model: "opus"`
- **System audits** → `model: "sonnet"` (mechanical but needs tool access)

**File scoping (critical):** Assign each agent a non-overlapping file scope. One agent, one directory. No parallel edits to same file.

**Output routing:** Research → `~/notes/Research/`. Content → `sarcio new`. Consolidation → vault in-place. Skills → `~/skills/`.

**Results:** Present summary when agent completes — don't wait for user to ask.

## Quality Gate

Every copia wave must pass verification before output is treated as trusted. Unverified agent output entering the vault as "truth" is the worst failure mode — it compounds silently.

### When to Run

Run the quality gate **after each wave of workers completes, before the lead synthesises or the orchestrator reports results.** The gate is mandatory for:
- GARP study notes (exam-critical claims have zero error tolerance)
- Research briefs that will inform client conversations
- Skill files that change orchestration behaviour
- Any note that will be published or sent without further human review

The gate is optional (but recommended) for:
- System health checks (self-verifying — tests pass or they don't)
- Content drafts marked for human editing
- Knowledge consolidation of already-verified source notes

### How It Works

1. **Dispatch a Sonnet verification agent** after each wave. Use the `censura` skill template (`~/skills/censura.md`). Sonnet is correct here — verification is mechanical (rubric-based), not taste-dependent.

2. **The verifier receives:**
   - List of output files produced by the wave
   - The original task prompts (what was each agent asked to do?)
   - Source material pointers (what should the agents have cited?)
   - For GARP notes: path to `~/notes/GARP/` for cross-reference

3. **The verifier checks five dimensions:**

| Dimension | What it checks | PASS / FLAG / FAIL criteria |
|---|---|---|
| **Source fidelity** | Do factual claims trace to cited sources? Are quotes accurate? | PASS: all claims sourced. FLAG: 1-2 unsourced but plausible. FAIL: fabricated citations or misattributed claims. |
| **Internal consistency** | Do outputs from this wave contradict each other or existing vault notes? | PASS: no contradictions. FLAG: tension that might be legitimate nuance. FAIL: direct contradiction on material facts. |
| **Hallucination scan** | Are cited frameworks, regulations, papers, people real? Do dates and versions match? | PASS: all verifiable. FLAG: unable to verify (no web access). FAIL: demonstrably invented citation. |
| **Obsidian hygiene** | Wikilinks resolve to existing notes. Tags match vault conventions. Frontmatter schema is correct. | PASS: all links resolve, tags consistent. FLAG: 1-2 broken links (target may not exist yet). FAIL: systematic formatting errors. |
| **Domain accuracy** (GARP only) | Exam-critical claims match known correct positions (SR 11-7 definitions, regulatory jurisdiction assignments, framework attributions). | PASS: matches authoritative sources. FLAG: simplification that could mislead on exam. FAIL: wrong answer to an exam-testable claim. |

4. **The verifier produces:** `_verification-report.md` saved alongside the wave output (same directory). One report per wave, not per file. Format:

```markdown
---
title: "Copia Verification Report — [wave description]"
date: [ISO date]
tags: [copia, verification]
verdict: PASS | PARTIAL | FAIL
---

# Verification Report

**Wave:** [description]
**Files checked:** [list]
**Verdict:** PASS / PARTIAL (has FLAGs) / FAIL

## Per-File Results

### [filename]
- **Source fidelity:** PASS/FLAG/FAIL — [detail]
- **Internal consistency:** PASS/FLAG/FAIL — [detail]
- **Hallucination scan:** PASS/FLAG/FAIL — [detail]
- **Obsidian hygiene:** PASS/FLAG/FAIL — [detail]
- **Domain accuracy:** PASS/FLAG/FAIL — [detail if GARP]

### [filename]
...

## Flags Requiring Human Review
[List any FLAG items with enough context for Terry to make a judgment call]

## Failed Items
[List any FAIL items — these should NOT be trusted until corrected]

## Cross-File Consistency Notes
[Any contradictions or tensions between files in this wave, or between wave output and existing vault notes]
```

### Routing After Verification

| Verdict | Action |
|---|---|
| **PASS** | Output trusted. Lead may synthesise. Report to user. |
| **PARTIAL** | Output usable but FLAGged items need human review. Lead synthesises PASS items; FLAGs queued for Terry. |
| **FAIL** | Failed items are quarantined — rename with `_UNVERIFIED` prefix. Do NOT merge into vault as-is. Report failures to user with enough context to decide: fix, retry, or discard. |

### Integration with Team Flow

```
Lead decomposes → Workers execute (parallel) → QUALITY GATE → Lead synthesises
                                                     ↓
                                            _verification-report.md
                                                     ↓
                                          PASS → proceed
                                          PARTIAL → proceed with caveats
                                          FAIL → quarantine + report
```

The verification agent runs as a **peer of the workers**, not as the lead. The lead dispatches it after collecting worker outputs but before synthesising. Budget ~2-3 min for verification (it reads files + cross-checks, no web search needed).

### Budget Impact

Verification adds ~10-15% token overhead per wave (Sonnet reading + checking N files). This is cheap insurance. A hallucinated regulatory citation that enters the vault and later appears in a client conversation costs infinitely more than a Sonnet verification pass.

## After Completion

- Mention key findings in next `/wrap`
- If research surfaces an action item → add to TODO.md or Due
- If research is engagement-relevant → link from `[[Capco Transition]]`
- **Retro:** Note what was high-value vs waste → refine the menu for next session

## Anti-patterns

- Don't run research that duplicates what LaunchAgents already do (praeco, speculor, theoros)
- Don't run GARP drilling here — use `/dokime` for that (different modality)
- Don't research topics with no clear consumer — "interesting" isn't enough
- Content: don't write posts that need Terry's personal experience — stick to analytical/framework pieces
- Consolidation: don't merge notes that are intentionally separate (check for `[[` cross-references first)
- Pre-drafting: don't pre-draft client emails or anything that needs Terry's voice calibration
