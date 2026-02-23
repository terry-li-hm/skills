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

**Key insight:** Sonnet has its own weekly quota separate from the all-models cap. Shifting work to Sonnet doesn't just reduce all-models % — it draws from a mostly-untouched pool.

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

## Extra Usage

$50/month cap. Tracks actual spend (not equiv). Resets 1st of month. Once depleted, likely rate-limited until reset. Monitor via `/status`.

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
