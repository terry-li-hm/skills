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

Anthropic doesn't disclose the exact weekly cap. Based on Terry's actual limit hits:
- **Jan 23:** Hit limit ~$800-1000 into the week
- **Jan 30:** Hit limit ~$700-900 into the week

**Calibrated estimate: ~$800 equiv** for Max20 weekly cap.

**Safe daily budget:** ~$115/day for full 7-day week. Days over $300 need balancing with light days.

**Subjective calibration:** When you *feel* 75% used, you're probably 85-90%. Gut feel underestimates actual usage.

**Thresholds (calibrated to Terry's data):**
| % Used | Equiv Cost | Status |
|--------|------------|--------|
| 0-60% | $0-480 | ✅ Safe |
| 60-75% | $480-600 | ⚠️ Caution — pace yourself |
| 75-90% | $600-720 | 🟠 Warning — switch to Sonnet for routine tasks |
| 90%+ | $720+ | 🔴 Danger — high risk of hitting limit |

**Historical limit hits (from ~/.claude logs):**
- 2026-01-23 12:07 HKT — "resets Jan 24 6pm"
- 2026-01-30 07:28 HKT — "resets 6pm" (Saturday)

**To calculate weekly usage:**
1. Find last Saturday 6pm HKT
2. Sum equiv cost since then
3. Calculate days until next Saturday 6pm
4. Show % of estimated $800 cap and burn rate

**To find historical limit hits:**
```bash
grep -rh '"text":"You'\''ve hit your limit' ~/.claude/projects/-Users-terry/*.jsonl | grep -o '"timestamp":"[^"]*"\|"text":"[^"]*"' | paste - - | sort -u
```

## Aliases

These are defined in ~/.zshrc:
- `cu` — Quick current month daily view
- `cm` — Launch live monitor

---

# Prompt

## Step 1: Get usage data + limit history

```bash
# Current month usage
ccusage daily -s $(date +%Y%m01) --breakdown

# Recent limit hits (last 5)
grep -rh '"text":"You'\''ve hit your limit' ~/.claude/projects/-Users-terry/*.jsonl 2>/dev/null | \
  grep -o '"timestamp":"[^"]*"\|"text":"[^"]*"' | paste - - | sort -u | tail -5
```

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
- Days elapsed / remaining: X.X / X.X days
- Used this week: $XXX equiv (~XX% of ~$800 cap)
- Status: [✅ Safe | ⚠️ Caution | 🟠 Warning | 🔴 Danger]
- Daily burn rate: $XX/day (safe: ~$115/day)
- Days at current pace: X.X days until cap
- Projected by reset: $XXX

**Recent Limit Hits**
- [date] — hit at ~$XXX, reset [time]
- [date] — hit at ~$XXX, reset [time]

**This Month**
| Day | Tokens | Cost |
...

**Recommendation:** [Pace advice based on status and history]
```

## Thresholds (calibrated)

- ✅ **Safe** (0-60%, <$480): No concerns
- ⚠️ **Caution** (60-75%, $480-600): Pace yourself, avoid heavy sessions
- 🟠 **Warning** (75-90%, $600-720): Switch to Sonnet for routine tasks
- 🔴 **Danger** (90%+, >$720): High risk of hitting limit, use Haiku/Sonnet only
