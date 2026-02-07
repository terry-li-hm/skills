---
name: usage
description: Check Claude Code Max plan usage stats and token consumption. "usage"
user_invocable: true
---

# Claude Code Usage Check

Check token usage and equivalent costs for Claude Code Max plan.

## Tools Available

- **ccusage** — Static reports (daily, monthly, session, blocks)
- **claude-monitor** — Live dashboard (realtime tracking)

## Quick Commands

```bash
# Current month daily breakdown
ccusage daily -s $(date +%Y%m01)

# Monthly summary
ccusage monthly

# With model breakdown
ccusage daily -s $(date +%Y%m01) --breakdown

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

**Terry's weekly reset:** Saturday 6pm HKT

The equivalent API cost shown by ccusage helps gauge value — if you're consistently using >$200/month equivalent, Max20 is worth it.

## Weekly Limit Tracking

**Calibrated estimate: ~$800 equiv** for Max20 weekly cap. Safe daily budget: ~$115/day.

| % Used | Equiv Cost | Status |
|--------|------------|--------|
| 0-60% | $0-480 | ✅ Safe |
| 60-75% | $480-600 | ⚠️ Caution — pace yourself |
| 75-90% | $600-720 | 🟠 Warning — switch to Sonnet for routine tasks |
| 90%+ | $720+ | 🔴 Danger — high risk of hitting limit |

**To calculate:** Find last Saturday 6pm HKT, sum equiv cost since then, show % of ~$800 cap.

**Find limit hits:**
```bash
grep -rh '"text":"You'\''ve hit your limit' ~/.claude/projects/-Users-terry/*.jsonl 2>/dev/null | \
  grep -o '"timestamp":"[^"]*"\|"text":"[^"]*"' | paste - - | sort -u | tail -5
```

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
