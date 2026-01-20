---
name: history
description: Scan chat history with proper HKT timezone handling. Use when reviewing what was discussed on a specific day.
---

# History

Scan `~/.claude/history.jsonl` with proper HKT (UTC+8) day boundaries.

## Trigger

- `/history` — today's prompts
- `/history yesterday` — yesterday's prompts
- `/history 2026-01-18` — specific date

## Workflow

1. **Parse the date argument**:
   - No argument or "today" → today in HKT
   - "yesterday" → yesterday in HKT
   - `YYYY-MM-DD` → that specific date

2. **Scan history.jsonl with HKT boundaries**:

```python
import json
from datetime import datetime, timedelta, timezone

# HKT is UTC+8
HKT = timezone(timedelta(hours=8))

def scan_history(target_date_str, limit=50):
    """Scan history.jsonl for a specific date in HKT."""
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d').replace(tzinfo=HKT)

    # Day boundaries in HKT → Unix milliseconds
    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    start_ms = int(day_start.timestamp() * 1000)
    end_ms = int(day_end.timestamp() * 1000)

    prompts = []
    sessions = {}

    with open('/Users/terry/.claude/history.jsonl', 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                ts = entry.get('timestamp', 0)
                if not isinstance(ts, int) or not (start_ms <= ts < end_ms):
                    continue

                ts_hkt = datetime.fromtimestamp(ts/1000, tz=HKT)
                sess = entry.get('sessionId', 'unknown')
                prompt = entry.get('display', entry.get('prompt', ''))

                prompts.append({
                    'time': ts_hkt.strftime('%H:%M'),
                    'session': sess[:8],
                    'prompt': prompt[:100].replace('\n', ' ')
                })

                # Track sessions
                if sess not in sessions:
                    sessions[sess] = {'count': 0, 'first': ts_hkt, 'last': ts_hkt}
                sessions[sess]['count'] += 1
                sessions[sess]['last'] = ts_hkt

            except (json.JSONDecodeError, Exception):
                continue

    return {
        'date': target_date_str,
        'total': len(prompts),
        'sessions': [
            {'id': sid[:8], 'count': s['count'],
             'range': f"{s['first'].strftime('%H:%M')}-{s['last'].strftime('%H:%M')}"}
            for sid, s in sorted(sessions.items(), key=lambda x: x[1]['first'])
        ],
        'prompts': prompts[-limit:] if limit else prompts
    }

# Usage
today = datetime.now(HKT).strftime('%Y-%m-%d')
result = scan_history(today)
print(f"Date: {result['date']} (HKT)")
print(f"Total: {result['total']} prompts across {len(result['sessions'])} sessions\n")
print("Sessions:")
for s in result['sessions']:
    print(f"  [{s['id']}] {s['count']:3d} prompts ({s['range']})")
```

3. **Return summary**:
   - Total prompt count
   - Time range (first to last prompt)
   - Sample of prompts (truncated)
   - Optionally group by hour or session

## Output Format

```
## Chat History for 2026-01-19 (HKT)

**Total prompts:** 142
**Time range:** 09:15 - 23:45

### By Hour
- 09:00-10:00: 12 prompts
- 10:00-11:00: 25 prompts
...

### Sample Prompts
- 09:15: "check my gmail..."
- 09:22: "update the note..."
...
```

## Options

- `--full` — Show all prompts (not just sample)
- `--hours` — Group by hour
- `--count` — Just show count, no details

## Error Handling

- **If history.jsonl missing**: Return "No chat history found"
- **If no prompts for date**: Return "No prompts found for [date]"
- **If invalid date format**: Return "Invalid date. Use YYYY-MM-DD format"

## Notes

- Always uses HKT (UTC+8) for day boundaries
- Timestamps in history.jsonl are in milliseconds
- This skill can be called by `/daily` for chat scanning
