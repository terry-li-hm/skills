---
name: copia
description: Token abundance recipe — high-value autonomous research tasks to run when Max20 weekly budget has plenty of room. Use when user says "copia", "burn tokens", "spare tokens", "use up budget", or when /usus shows weekly % < 50% mid-week.
user_invocable: true
---

# Copia — Burning Token Abundance

When Max20 budget is plentiful (weekly % < 50% by Wednesday, or user says so), launch high-value background research that requires zero user involvement.

## Pre-flight

1. Check budget: `/usus` or `/status` — confirm weekly % leaves room for 3-5 parallel agents
2. Check what's stale: scan `~/notes/Research/` — anything >30 days old is a refresh candidate
3. Check NOW.md for open items that benefit from research

## The Menu

Pick based on current priorities. All run as **background agents on Max20** (zero API cost). All save to `~/notes/Research/`.

### Tier 1 — Always High Value
These compound over time. Run whenever budget allows.

| Task | Output | Agent prompt focus |
|------|--------|--------------------|
| **HSBC engagement prep** | `HSBC AI Governance Brief.md` | Annual report, HKMA circulars, AI strategy, key people, Capco opportunities |
| **APAC regulatory landscape** | `APAC AI Regulatory Landscape.md` | Cross-jurisdiction comparison (HKMA, MAS, APRA, JFSA), upcoming regulation, gaps |
| **Competitor intelligence** | `AI Governance Competitor Landscape APAC.md` | McKinsey/Deloitte/Accenture/EY/PwC offerings, APAC presence, differentiation |
| **AI landscape deep-dive** | `AI Landscape Deep Dive.md` | Beyond weekly dialexis — emerging tools, model releases, industry shifts |

### Tier 2 — Situational
Run when the specific context is active.

| Task | When | Output |
|------|------|--------|
| **GARP RAI deep-dives** | Exam approaching | `GARP/` subfolder, one brief per weak domain |
| **Client/prospect research** | Pre-engagement | `Research/<Company> Brief.md` |
| **Garden content mining** | Content drought | Scan vault for 10 post-worthy ideas, draft outlines |
| **Job market intelligence** | Active search | Role patterns, salary benchmarks, demand signals |

### Tier 3 — Maintenance
Low urgency but good use of spare tokens.

| Task | Output |
|------|--------|
| **CLI health sweep** | Parallel agents verify every `~/code/` tool builds, tests pass, skill matches binary |
| **Vault hygiene** | Orphan notes, broken links, stale research, knowledge gaps |
| **Solutions KB refresh** | Verify `~/docs/solutions/` entries still accurate, flag outdated |
| **Skill drift audit** | Compare every skill description against actual binary `--help` output |

## Execution Pattern

```
# Launch 3-5 agents in parallel, all background
Agent(name="research-X", run_in_background=true, model="sonnet")
# Sonnet for research collection, Opus for synthesis/judgment
```

- **Research/collection agents** → `model: "sonnet"` (saves Opus quota for judgment)
- **Synthesis/analysis agents** → `model: "opus"` or inherit parent
- All save to `~/notes/Research/` with date in content (not filename)
- Results: present summary when agent completes, don't wait for user to ask

## After Completion

- Mention key findings in next `/wrap`
- If research surfaces an action item → add to TODO.md or Due
- If research is engagement-relevant → link from `[[Capco Transition]]`

## Anti-patterns

- Don't run research that duplicates what LaunchAgents already do (praeco, speculor, theoros)
- Don't run GARP drilling here — use `/dokime` for that (different modality)
- Don't research topics with no clear consumer — "interesting" isn't enough
