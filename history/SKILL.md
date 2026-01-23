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

Run the persistent script at `~/scripts/chat_history.py`:

```bash
# Today's prompts
python ~/scripts/chat_history.py

# Yesterday's prompts
python ~/scripts/chat_history.py yesterday

# Specific date
python ~/scripts/chat_history.py 2026-01-23

# Show all prompts (not just last 50)
python ~/scripts/chat_history.py --full

# Output as JSON (for programmatic use)
python ~/scripts/chat_history.py --json
```

## Output Format

```
Date: 2026-01-19 (HKT)
Total: 142 prompts across 8 sessions
Time range: 09:15 - 23:45

Sessions:
  [797013a0]  12 prompts (07:16-10:05)
  [f4764f0c]   9 prompts (07:20-09:50)
  ...

Recent prompts (last 50):
  09:15 [797013a0] check my gmail...
  09:22 [797013a0] update the note...
  ...
```

## Options

- `--full` — Show all prompts (not just last 50)
- `--json` — Output as JSON for programmatic parsing

## Error Handling

- **If history.jsonl missing**: Returns error message
- **If no prompts for date**: Returns empty results
- **If invalid date format**: Returns "Invalid date. Use YYYY-MM-DD format"

## Notes

- Always uses HKT (UTC+8) for day boundaries
- Timestamps in history.jsonl are in milliseconds
- Script location: `~/scripts/chat_history.py`
- This skill can be called by `/daily` for chat scanning
