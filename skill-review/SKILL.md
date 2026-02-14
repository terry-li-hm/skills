---
name: skill-review
description: Monthly review of skills for staleness, drift, and gaps. Use on first Friday of month or when skills feel out of sync.
user_invocable: true
---

# Skill Review

Periodic audit to catch skill drift, identify gaps, and prune unused skills.

## Trigger

- First Sunday of the month
- When skills feel stale or routing seems off
- After major vault reorganization

## Workflow

### 1. Inventory Check

```bash
ls -la /Users/terry/skills/*/SKILL.md | wc -l
ls -la /Users/terry/.claude/skills/*/SKILL.md | wc -l
```

Count skills in both locations. Flag any missing symlinks.

### 2. Usage Scan

Search recent chat history for skill invocations:

```bash
grep -h "Using \`/" ~/.claude/history.jsonl | tail -100
grep -h "/[a-z-]*\`" ~/.claude/history.jsonl | tail -100
```

Identify:
- **Frequently used** — Working well, keep
- **Never used** — Consider deprecating or improving description
- **Often corrected** — Needs refinement

### 3. Drift Detection

For each active skill, check:

| Check | How |
|-------|-----|
| **Vault references valid?** | Do paths in skill still exist? |
| **Vocabulary aligned?** | Does skill terminology match current vault notes? |
| **Workflow still accurate?** | Has the process changed since skill was written? |

### 4. Gap Analysis

Review recent sessions for patterns:
- Tasks done manually that could be skills
- Repeated multi-step workflows
- Questions asked that required vault deep-dives

### 5. Output

```markdown
## Skill Review - [Date]

### Healthy (Keep)
- `/skill-name` — Used X times, working well

### Needs Update
- `/skill-name` — Issue: [what's wrong]

### Candidates for Deprecation
- `/skill-name` — Last used: [date], reason to keep/remove

### Gaps Identified
- [Workflow that should be a skill]

### Actions
- [ ] Update X
- [ ] Create Y
- [ ] Deprecate Z
```

### 6. Save to Vault

Save review to `/Users/terry/notes/Skill Review - YYYY-MM.md`

## Quick Checks (Weekly)

Lighter version for weekly reset:

1. Any skills invoked incorrectly this week?
2. Any manual workflows repeated 3+ times?
3. Any skill descriptions that confused routing?

## Related Skills

- `design-skill` — How skills should be structured
- `vault-search` — Finding content skills reference
