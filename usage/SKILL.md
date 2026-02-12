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

**Find limit hits** (must use Python — bash guard blocks grep on `~/.claude/projects`):
```bash
python3 -c "
import glob, json, os
from collections import Counter

hits = []
for f in glob.glob(os.path.expanduser('~/.claude/projects/-Users-terry/*.jsonl')):
    with open(f) as fh:
        for line in fh:
            if 'hit your limit' in line.lower() or \"you've hit\" in line.lower():
                try:
                    data = json.loads(line)
                    ts = data.get('timestamp', '')
                    if ts: hits.append(ts)
                except: pass

hits.sort()
# Count by date (UTC dates shown — add 8h for HKT)
by_date = Counter(h[:10] for h in hits)
print('Limit hits by date:')
for d, c in sorted(by_date.items()):
    print(f'  {d}: {c} events')
print(f'\nTotal: {len(hits)} events across {len(by_date)} days')
print(f'\nNote: A single incident can generate 100+ retry events/sec.')
print('Count distinct time windows, not raw events.')
"
```

## Aliases

- `cu` — Quick current month daily view
- `cm` — Launch live monitor
