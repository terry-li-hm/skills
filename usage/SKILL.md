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

**Weekly reset:** Saturday ~8pm HKT (shifts slightly week to week).

The equivalent API cost shown by ccusage helps gauge value — if you're consistently using >$200/month equivalent, Max20 is worth it.

## Weekly Limit Tracking

**Calibrated estimate: ~$1,050 equiv** for Max20 weekly cap. Safe daily budget: ~$150/day.

Calibrated Feb 2026: $470-490 equiv spent = 44% per /status → implied cap ~$1,050-1,100.

| % Used | Equiv Cost | Status |
|--------|------------|--------|
| 0-50% | $0-525 | Safe |
| 50-70% | $525-735 | Caution — pace yourself |
| 70-85% | $735-890 | Warning — switch to Sonnet for routine tasks |
| 85%+ | $890+ | Danger — high risk of hitting limit |

**To calculate:** Find last Saturday ~8pm HKT, sum equiv cost since then, show % of ~$1,050 cap.

**User self-check:** `/status` in the Claude Code prompt shows exact usage % and reset times directly (Claude cannot run this — it's an interactive UI command).

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
