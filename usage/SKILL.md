---
name: usage
description: Check Claude Code Max plan usage stats. Use when user says "usage", "check usage", "how much have I used", "token usage", or wants to see Claude Code consumption.
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

## Aliases

These are defined in ~/.zshrc:
- `cu` — Quick current month daily view
- `cm` — Launch live monitor

---

# Prompt

Run this command to get current month usage:

```bash
ccusage daily -s $(date +%Y%m01) --breakdown
```

Then summarize with:
1. **Table** showing daily tokens and equivalent cost
2. **Model mix** — % Opus vs Haiku vs Sonnet
3. **Value assessment** — Compare equiv cost to Max20 ($200/mo) to show ROI
4. **Tip** — Mention `cm` alias for live monitoring if user wants real-time tracking
