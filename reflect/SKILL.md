---
name: reflect
description: End-of-session reflection to capture mistakes, preferences, daily updates, workflow improvements, and follow-up tasks. Use at the end of conversations to compound learnings.
redirect: review --mode=session
---

# Reflect

> **Note:** This skill has been merged into `/review`. Use `/review --mode=session` for the same functionality.

End-of-session reflection that reviews the conversation and updates relevant files with anything worth capturing.

## When to Use

- End of a productive session
- After discovering something that should be documented
- When Terry says "let's wrap up" or "end of session"
- Proactively suggest at natural stopping points

## What to Capture

### 1. Mistakes to Record

Things Claude got wrong that should go in CLAUDE.md's "Record Mistakes Here" section.

Look for:
- Corrections Terry made ("No, do it this way...")
- Repeated clarifications needed
- Wrong assumptions or approaches
- Tools used incorrectly

**Format for CLAUDE.md:**
```
- [Brief description of mistake and correction]
```

### 2. Preferences Learned

Patterns in how Terry likes things done that aren't already documented.

Look for:
- Explicit preferences stated ("I prefer X")
- Implicit patterns (consistently choosing one approach over another)
- Format or style preferences
- Tool preferences

**Add to relevant CLAUDE.md section or create new one if needed.**

### 3. Daily Note Updates

Activity worth logging in the daily note (`/Users/terry/notes/YYYY-MM-DD.md`).

Categories:
- **Job search activity** — applications sent, responses received, interviews scheduled
- **Key learnings** — technical insights, career realizations
- **Tools/skills set up** — new capabilities configured
- **Mood check** — optional, only if naturally came up

### 4. Workflow Improvements

Skills, patterns, or automations worth documenting.

Look for:
- Multi-step processes that could become skills
- Workarounds that should be formalized
- Successful patterns to replicate

**Action:** Create new skill or update existing one, or add to CLAUDE.md.

### 5. Follow-up Tasks

Things to do next session or soon.

Look for:
- Unfinished work
- "We should do X later" mentions
- Blocked tasks waiting on external input
- Ideas to explore

**Add to daily note or a dedicated follow-ups section.**

## Instructions

### Step 1: Scan Conversation

Review the full conversation and extract items for each category above. Be selective — only capture things that are:
- Recurring (happened more than once)
- Significant (would meaningfully improve future sessions)
- Actionable (can be documented or fixed)

### Step 2: Present Summary

Show Terry what you found:

```
## Session Reflection

### Mistakes to Record
- [item] → will add to CLAUDE.md

### Preferences Learned
- [item] → will add to [location]

### Daily Note Updates
- [items for today's note]

### Workflow Improvements
- [item] → [proposed action]

### Follow-up Tasks
- [item]

Proceed with updates?
```

### Step 3: Apply Updates (after confirmation)

1. **CLAUDE.md mistakes** — Append to "Record Mistakes Here" section
2. **CLAUDE.md preferences** — Add to relevant section
3. **Daily note** — Create or update `/Users/terry/notes/YYYY-MM-DD.md`
4. **Skills** — Create/update in `/Users/terry/skills/`
5. **Follow-ups** — Add to daily note under "## Follow-ups"

### Step 4: Commit Changes

```bash
# If CLAUDE.md changed
cd ~/claude-config && git add -A && git commit -m "Update CLAUDE.md from session reflection" && git push

# If skills changed
cd ~/skills && git add -A && git commit -m "Update skills from session reflection" && git push
```

## Tips

- Run this before ending long sessions to avoid losing context
- If nothing significant happened, say so — don't force updates
- Keep entries concise and actionable
- Daily notes don't need git commits (Obsidian vault)

## Files

- This skill: `/Users/terry/skills/reflect/SKILL.md`
- CLAUDE.md: `/Users/terry/CLAUDE.md`
- Daily notes: `/Users/terry/notes/YYYY-MM-DD.md`
- Skills: `/Users/terry/skills/`
