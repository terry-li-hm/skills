---
name: daily
description: End-of-day reflection to capture job search progress, learnings, and mood. Use when user says "daily", "end of day", "daily note", or at end of day.
redirect: review --mode=daily
---

# Daily Reflection

> **Note:** This skill has been merged into `/review`. Use `/review --mode=daily` for the same functionality.

End-of-day reflection to capture job search progress, learnings, and mood. Creates or updates daily note in vault.

## Trigger

Use when:
- End of day
- User says "daily", "reflect", "end of day", "daily note"

## Inputs

- **date** (optional): Defaults to today in YYYY-MM-DD format

## Workflow

1. **Get today's date** in `YYYY-MM-DD` format (HKT timezone)

2. **Scan chat history** from `~/.claude/history.jsonl`:
   ```python
   import json
   from datetime import datetime

   today = datetime.now().strftime('%Y-%m-%d')
   today_start = datetime.strptime(f"{today} 00:00:00", '%Y-%m-%d %H:%M:%S').timestamp() * 1000 - (8 * 3600 * 1000)
   today_end = today_start + (24 * 3600 * 1000)

   prompts = []
   with open('/Users/terry/.claude/history.jsonl', 'r') as f:
       for line in f:
           entry = json.loads(line)
           if today_start <= entry.get('timestamp', 0) <= today_end:
               prompts.append(entry.get('display', ''))
   ```

3. **Fetch Oura data** using MCP tools:
   - `mcp__oura__get_today_readiness_data` — get readiness score, HRV, recovery index
   - `mcp__oura__get_today_resilience_data` — get resilience level and stress score

4. **Check for existing note** at `/Users/terry/notes/YYYY-MM-DD.md`

5. **Walk through each section** conversationally:
   - **Job Search Activity**: Applications, status updates, pipeline changes
   - **Key Learnings**: Insights about job search, interviews, companies
   - **Tools/Skills**: New tools set up or skills practiced
   - **Mood Check**: How are you feeling? (1-5 or a word)

6. **Create or update the note** using template below

7. **Save to vault** at `/Users/terry/notes/YYYY-MM-DD.md`

## Error Handling

- **If history.jsonl unreadable**: Skip chat scan, proceed with manual input
- **If Oura data unavailable**: Skip Oura section or note "No data"
- **If note already exists**: Update rather than overwrite
- **If user has nothing for a section**: Skip or put "—"

## Output

**Template:**
```markdown
# YYYY-MM-DD

## Oura

- **Readiness:** [score]
- **Resilience:** [level]
- **Stress:** [score]
- **HRV balance:** [score]
- **Recovery index:** [score]

## Job Search Activity

- Applied:
- Status updates:
- Next up:

## Learnings

-

## Tools/Skills

-

## Mood

[Include Oura context in mood assessment]
```

**Location:** `/Users/terry/notes/YYYY-MM-DD.md`

## Examples

**User**: "daily"
**Action**: Scan chat history, ask about job activity, create note
**Output**: Daily note saved to vault with structured reflection
