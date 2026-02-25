---
name: usage
description: Check Claude Code Max plan usage stats and token consumption. "usage"
user_invocable: true
---

# Claude Code Usage Check

Check token usage and equivalent costs for Claude Code Max plan.

## Quick Commands

```bash
# Current month daily breakdown with model mix
ccusage daily -s $(date +%Y%m01) --breakdown

# Monthly summary
ccusage monthly

# Per-session breakdown
ccusage session -s $(date +%Y%m01)

# Live monitoring (run in separate terminal)
claude-monitor --plan max20
```

## Procedure

1. Run `ccusage daily -s $(date +%Y%m01) --breakdown` for current month with model breakdown
2. Summarize key stats:
   - Total tokens used this month
   - Equivalent API cost (for context on value extracted)
   - Daily average
   - Model mix (Opus vs Haiku vs Sonnet)
3. Calculate weekly usage (see below)
4. If user wants live tracking, suggest running `claude-monitor --plan max20` in a separate terminal

## Max Plan Context

| Plan | Monthly Cost | Token Allowance |
|------|--------------|-----------------|
| Max5 | $100 | ~88K tokens/5min window |
| Max20 | $200 | ~220K tokens/5min window |

**User self-check:** `/status` in the Claude Code prompt shows exact usage % and reset times directly (Claude cannot run this — it's an interactive UI command).

## Usage Counters (/status)

Max20 has **four independent counters** visible via `/status`:

| Counter | Scope | Reset Cycle | Notes |
|---------|-------|-------------|-------|
| Session | Per-session | ~4pm HKT daily | Least important — resets frequently |
| Weekly (all models) | Opus + Sonnet + Haiku | Saturday ~8pm HKT | **Primary limiter** |
| Weekly (Sonnet only) | Sonnet usage only | ~Sunday 1pm HKT (different cycle) | Separate Sonnet quota |
| Extra usage | Monthly spend cap | 1st of month | $50 hard cap, shows $/$ spent |

**How the counters interact** ([source](https://github.com/anthropics/claude-code/issues/12487)):
- Sonnet usage counts against **both** "Sonnet only" AND "All models"
- Opus usage counts against "All models" **only**
- When "All models" hits 100%, everything is blocked — even if "Sonnet only" shows 2%
- The Sonnet cap is a **ceiling** (prevents filling all-models quota with cheaper Sonnet tokens), not a separate pool

## Weekly Limit Tracking (All Models)

**Calibrated estimate: ~$1,350 equiv** for Max20 weekly all-models cap.

**Important caveat:** The weekly cap is in Anthropic's internal token units, not dollars. The ccusage equiv cost shifts when API pricing changes (e.g., Opus 4.5 → 4.6 dropped from $15/$75 to $5/$25). Earlier data points from the Opus 4.5 era underestimated the dollar-equivalent cap because the same internal quota now maps to more dollars at lower per-token prices.

Calibration data (Feb 2026):
- Data point 1 (early Feb, Opus 4.5 era): $470-490 equiv = 44% → implied cap ~$1,070-1,115
- Data point 2 (early Feb, Opus 4.5 era): $200-260 equiv = 20% → implied cap ~$1,000-1,300
- Data point 3 (Feb 25, Opus 4.6 era): ~$717-767 equiv = 54% → implied cap ~$1,330-1,420
- Best estimate: **~$1,350** (Data point 3 is most reliable — largest spend, current pricing)

Safe daily budget: ~$193/day (7-day week).

| % Used | Equiv Cost | Status |
|--------|------------|--------|
| 0-50% | $0-675 | Safe |
| 50-70% | $675-945 | Caution — pace yourself |
| 70-85% | $945-1,148 | Warning — shift routine tasks to Sonnet |
| 85%+ | $1,148+ | Danger — Sonnet/Haiku only |

**To calculate:** Find last Saturday ~8pm HKT, sum equiv cost since then, show % of ~$1,350 cap. Note: recalibrate if model pricing changes again — the dollar figure is a proxy, not the actual limit.

## Model Mix & Cost (Feb 2026 baseline)

**Opus dominates but Sonnet share growing.** `/model` shows Opus 4.6 as "Default (recommended)" for Max users. Shifting to Sonnet is a cost lever for quota management, not a quality correction.

**Full month (Feb 1-25):**

| Model | Daily Avg | % of Total | Role |
|-------|-----------|------------|------|
| Opus | ~$138 | 90% | Primary — all interactive work |
| Sonnet | ~$12 | 8% | Subagents, compound-engineering, routine tasks |
| Haiku | ~$1 | <1% | Lookups only |

**Monthly run rate:** ~$153/day equiv → ~$4,600/month (23x the $200 plan cost).

**Model transition visible in data:**
- Opus 4.5 → 4.6: ~Feb 6
- Sonnet 4.5 → 4.6: ~Feb 18

**Sonnet 4.6 adoption (post-Feb 18):**
- Before: Sonnet $0-2/day
- After: Sonnet $5-48/day (highly variable — $48 on Feb 21 was an outlier)
- Opus share dropped from 96% to ~85% on Sonnet-heavy days

**Daily variance is 4x:** $84 (Feb 7) to $364 (Feb 2). Heavy days are nearly all Opus-dominant.

**Cache efficiency:** Cache read tokens are ~25x cache create tokens. Compaction and context reuse working well.

**Cost lever:** Opus 4.6 is ~1.67x more expensive per token than Sonnet 4.6 ($5/$25 vs $3/$15). Each $100 of Opus work shifted to Sonnet saves ~$40 equiv. A 30% shift would save ~$17/day → ~$117/week (~9% of weekly cap). Meaningful but not transformative — the pricing gap closed significantly with Opus 4.5+.

## Extra Usage

$50/month cap. Tracks **actual API-equivalent spend**, not ccusage equiv. Resets 1st of month. Once depleted, likely rate-limited until reset. Monitor via `/status`.

**What triggers it:** Extended context (>200K tokens in a request), which bills all tokens at premium rates ($10/$37.50 Opus, $6/$22.50 Sonnet per Mtok). Context compaction is the primary way to avoid this.

**Feb 2026 observation:** $13.97 spent by Feb 25 (28%). Correlates with heavy Opus sessions — likely auto-compaction occasionally crossing 200K before kicking in. Not yet a constraint but worth monitoring on heavy weeks.

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
