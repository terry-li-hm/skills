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
