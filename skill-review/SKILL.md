---
name: skill-review
description: Review the current conversation to analyze skill usage, extract feedback, and generate iteration checklists. Use after long sessions to capture learnings and improve skills.
---

# Skill Review

Review the current conversation to analyze skill usage, extract feedback and corrections, and generate actionable iteration checklists. Outputs to Obsidian for persistence across sessions.

## When to Use

Use this skill when the user:
- Sends `/skill-review` or `/iteration-checklist`
- Says "review my skills usage" or "what skills need updating"
- Wants to capture learnings after a long Claude Code session
- Needs to iterate on custom skills based on feedback given during conversation

## Instructions

### Step 1: Review the Conversation

Scan the entire conversation history and identify:

1. **Skills invoked** - Both built-in and custom skills used (slash commands, agent types, etc.)
2. **Negative feedback** - Moments where the user corrected, redirected, or expressed frustration
3. **Positive signals** - Things that worked well and should be preserved
4. **Workarounds** - Manual steps the user had to take that a skill could automate

### Step 2: Extract Critical Feedback

For each piece of feedback found, categorize it:

| Category | Description | Example |
|----------|-------------|---------|
| **Procedure Error** | Skill followed wrong steps | "No, don't create a new file, edit the existing one" |
| **Missing Context** | Skill lacked necessary information | "You should have checked the CLAUDE.md first" |
| **Output Format** | Wrong format or structure | "Put this in a table instead" |
| **Trigger Mismatch** | Skill triggered when it shouldn't (or vice versa) | "I didn't want the full analysis, just a quick check" |
| **New Workflow** | User described a process not covered by existing skills | "When I share a LinkedIn job, I want you to..." |

### Step 3: Analyze Iteration Direction

For each feedback item, determine the action:

| Condition | Action |
|-----------|--------|
| Feedback targets specific procedure in existing skill | **Update existing skill** |
| Feedback reveals entirely new workflow | **Create new skill** |
| Feedback is one-time preference or edge case | **No action needed** |
| Feedback applies to multiple skills | **Update CLAUDE.md** (global instructions) |

### Step 4: Generate Output

Create a structured output with two sections:

#### A. Iteration Checklist

```markdown
## Skill Iteration Checklist - [DATE]

### Skills to Update
- [ ] **[skill-name]**: [specific change needed]
  - Feedback: "[quote from conversation]"
  - Location: `[file path if known]`

### New Skills to Create
- [ ] **[proposed-skill-name]**: [what it should do]
  - Trigger: [when to activate]
  - Workflow: [brief description]

### CLAUDE.md Updates
- [ ] [instruction to add/modify]

### No Action (One-time)
- [feedback that doesn't need skill changes]
```

#### B. Save to Obsidian

Write the checklist to the user's Obsidian vault:

```bash
# Save to Obsidian
cat > "/Users/terry/notes/Skill Reviews/$(date +%Y-%m-%d) Skill Review.md" << 'EOF'
[checklist content here]
EOF
```

Create the directory if it doesn't exist:
```bash
mkdir -p "/Users/terry/notes/Skill Reviews"
```

### Step 5: Confirm with User

Present the checklist and ask:
1. Which items should be actioned now?
2. Any feedback to ignore or deprioritize?
3. Should I implement any of the skill updates immediately?

## Example Output

```markdown
## Skill Iteration Checklist - 2026-01-17

### Skills to Update
- [ ] **linkedin-job-analysis**: Add pipeline health check before recommendation
  - Feedback: "Factor in how healthy my pipeline is before recommending PASS"
  - Location: Workflow in CLAUDE.md

### New Skills to Create
- [ ] **skill-review**: Meta-skill to review skill usage (this one!)
  - Trigger: `/skill-review`, `/iteration-checklist`
  - Workflow: Scan conversation → extract feedback → generate checklist

### CLAUDE.md Updates
- [ ] Add instruction: "Always create new browser tab at session start"

### No Action (One-time)
- User wanted table format for one specific comparison (not general preference)
```

## Tips

- Run this at the end of long sessions before context is lost
- The Obsidian note creates a paper trail for skill evolution
- Review past skill review notes periodically to spot patterns
- If the same feedback appears multiple times, prioritize that fix

## Files

- This skill: `/Users/terry/skills/skill-review/SKILL.md`
- Output location: `/Users/terry/notes/Skill Reviews/`

## Reference

Inspired by [@dontbesilent12's Skill Iteration Review concept](https://x.com/dontbesilent12/status/2011828768944636266)
