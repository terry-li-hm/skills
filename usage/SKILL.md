---
name: usage
description: Check Claude Code Max plan usage stats and token consumption. "usage"
user_invocable: true
---

# Claude Code Usage Check

Check token usage and equivalent costs for Claude Code Max plan.

## Quick Usage Check

**For current usage percentage:** Just run `/status` in Claude Code — it shows session %, weekly %, and exact reset times. This is the authoritative source.

## Detailed Breakdown (ccusage)

ccusage adds equivalent API cost tracking and historical analysis that `/status` doesn't provide.

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
3. If user wants live tracking, suggest running `claude-monitor --plan max20` in a separate terminal

## Max Plan Context

| Plan | Monthly Cost | Token Allowance |
|------|--------------|-----------------|
| Max5 | $100 | ~88K tokens/5min window |
| Max20 | $200 | ~220K tokens/5min window |

**Weekly reset:** Saturday ~8pm HKT (check `/status` for exact time — it shifts slightly).

The equivalent API cost shown by ccusage helps gauge value — if you're consistently using >$200/month equivalent, Max20 is worth it.

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
