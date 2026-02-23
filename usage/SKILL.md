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
- The Sonnet cap is a **ceiling** (prevents filling all-models quota with cheap Sonnet tokens), not a separate pool

## Weekly Limit Tracking (All Models)

**Calibrated estimate: ~$1,100 equiv** for Max20 weekly all-models cap.

Calibration data (Feb 2026):
- Data point 1: $470-490 equiv = 44% → implied cap ~$1,070-1,115
- Data point 2: $200-260 equiv = 20% → implied cap ~$1,000-1,300
- Best estimate: **~$1,100** (midpoint of overlapping range)

Safe daily budget: ~$155/day (7-day week).

| % Used | Equiv Cost | Status |
|--------|------------|--------|
| 0-50% | $0-550 | Safe |
| 50-70% | $550-770 | Caution — pace yourself |
| 70-85% | $770-935 | Warning — shift routine tasks to Sonnet |
| 85%+ | $935+ | Danger — Sonnet/Haiku only |

**To calculate:** Find last Saturday ~8pm HKT, sum equiv cost since then, show % of ~$1,100 cap.

## Model Mix & Cost (Feb 2026 baseline)

**Opus dominates: 96% of equiv cost — despite Anthropic recommending Sonnet 4.6 as default.** Per the [Sonnet 4.6 announcement](https://www.anthropic.com/news/claude-sonnet-4-6) (Feb 17, 2026): Sonnet 4.6 is the recommended default for Claude Code. Opus 4.6 should be reserved for deepest reasoning only (refactoring, multi-agent, "getting it just right"). Users preferred Sonnet 4.6 over Opus 4.5 59% of the time in testing.

| Model | Daily Avg | % of Total | Role |
|-------|-----------|------------|------|
| Opus | ~$140 | 96% | Primary — all interactive work |
| Sonnet | ~$5 | 3.5% | Subagents, routine tasks |
| Haiku | ~$0.77 | 0.5% | Lookups only |

**Monthly run rate:** ~$146/day equiv → ~$3,350/month (16.8x the $200 plan cost).

**Sonnet 4.6 trend (arrived ~Feb 18):**
- Before: Opus $145/day, Sonnet $0.8/day
- After: Opus $124/day, Sonnet $17.6/day
- Sonnet share rising as more work shifts off Opus

**Heaviest days** (>$200 equiv): driven entirely by Opus-heavy sessions. The top 5 days averaged $256 equiv — all 95%+ Opus.

**Cost lever:** Opus is ~5x more expensive per token than Sonnet. Each $100 of Opus work shifted to Sonnet saves ~$80 equiv. A 30% shift would save ~$235/week — roughly 21% of the weekly cap. This is the primary knob for staying under limits.

## Extra Usage

$50/month cap. Tracks actual spend (not equiv). Resets 1st of month. Once depleted, likely rate-limited until reset. Monitor via `/status`.

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
