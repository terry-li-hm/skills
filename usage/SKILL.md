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

## Weekly Limit Tracking

Anthropic doesn't disclose the exact weekly cap, but community reports suggest **~$600 equiv** for Max20 before throttling.

**Estimated thresholds:**
| % Used | Equiv Cost | Status |
|--------|------------|--------|
| 0-70% | $0-420 | ✅ Safe |
| 70-85% | $420-510 | ⚠️ Caution — pace yourself |
| 85-95% | $510-570 | 🟠 Warning — consider switching to Sonnet |
| 95%+ | $570+ | 🔴 Danger — likely to hit limit |

**To calculate weekly usage:**
1. Find last Saturday 6pm HKT
2. Sum equiv cost since then
3. Calculate days until next Saturday 6pm
4. Show % of estimated cap and burn rate

## Aliases

These are defined in ~/.zshrc:
- `cu` — Quick current month daily view
- `cm` — Launch live monitor

---

# Prompt

## Step 1: Get usage data

```bash
ccusage daily -s $(date -v-sat +%Y%m%d) --breakdown
```

(This gets usage since last Saturday. If today IS Saturday, adjust to previous week's Saturday.)

## Step 2: Calculate weekly status

1. **Find last reset:** Most recent Saturday 6pm HKT before now
2. **Sum equiv cost** since that reset
3. **Calculate % of estimated $600 cap**
4. **Days remaining** until next Saturday 6pm HKT

## Step 3: Summarize with weekly warning

Output format:

```
**Weekly Limit Status**
- Reset: [last Sat date] 6pm → [next Sat date] 6pm HKT
- Days remaining: X.X days
- Used this week: $XXX equiv (~XX% of est. cap)
- Status: [✅ Safe | ⚠️ Caution | 🟠 Warning | 🔴 Danger]
- Burn rate: $XX/day → projected $XXX by reset

**This Month**
| Day | Tokens | Cost |
...

**Recommendation:** [Pace advice based on status]
```

## Thresholds

- ✅ **Safe** (0-70%, <$420): No concerns
- ⚠️ **Caution** (70-85%, $420-510): Pace yourself, avoid heavy sessions
- 🟠 **Warning** (85-95%, $510-570): Switch to Sonnet for routine tasks
- 🔴 **Danger** (95%+, >$570): High risk of hitting limit, use Haiku/Sonnet only
