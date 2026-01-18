# Daily Reflection

End-of-day reflection to capture job search progress, learnings, and mood.

## Trigger

Use when:
- End of day
- User says "daily", "reflect", "end of day", "daily note"

## Steps

1. **Get today's date** in `YYYY-MM-DD` format

2. **Scan chat history** from `~/.claude/history.jsonl`:
   - Filter entries where timestamp falls within today (HKT = UTC+8)
   - Extract user prompts to identify: applications, decisions, tools set up, learnings
   - Use this to prompt Terry or auto-populate sections

   ```python
   import json
   from datetime import datetime

   # Today's timestamp range (HKT)
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

3. **Check for existing note** at `/Users/terry/notes/YYYY-MM-DD.md`

4. **Walk through each section** by asking Terry:

   **Job Search Activity**
   - What did you apply to today?
   - Any status updates on existing applications?
   - What's next in the pipeline?

   **Key Learnings**
   - Anything interesting you learned today?
   - New insights about job search, interviews, or target companies?

   **Tools/Skills**
   - Any new tools set up or skills practiced?

   **Mood Check**
   - How are you feeling? (1-5 or a word)

5. **Create or update the note** with this template:

```markdown
# YYYY-MM-DD

## Job Search Activity
- Applied:
- Status updates:
- Next up:

## Learnings
-

## Tools/Skills
-

## Mood

```

6. **Save to vault** at `/Users/terry/notes/YYYY-MM-DD.md`

## Notes

- Keep it conversational, not interrogative
- If Terry has nothing for a section, that's fine — skip or put "—"
- If note already exists, update rather than overwrite
- **Chat history as memory aid:** Use the extracted prompts to remind Terry of activities he may have forgotten. Surface items like "I see you worked on X today — should we add that?"
