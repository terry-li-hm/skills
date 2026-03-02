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

Search recent chat history for skill invocations. **Important:** Count BOTH explicit `/name` invocations AND keyword triggers — most skills are triggered by natural language, not slash commands. Counting only slash invocations drastically undercounts usage (e.g. consilium showed 0 slash but ~300 keyword triggers).

```python
# Slash invocations
import json, re, collections
counts = collections.Counter()
with open('/Users/terry/.claude/anam.jsonl') as f:
    for line in f:
        data = json.loads(line)
        msg = data.get('display', '').lower()
        for m in re.findall(r'(?:^|\s)/([a-z][a-z0-9-]+)', msg):
            counts[m] += 1

# Keyword triggers (add patterns for high-value skills)
keywords = {
    'consilium': r'ask.llms|consilium|multi.llm|council',
    'gmail': r'check.*email|inbox|gmail',
    'whatsapp': r'whatsapp|check.*messages',
    'todo': r'todo|add.*todo|check.*todo',
    'oura': r'oura|sleep.*score|how.*sleep',
    'message': r'draft.*reply|draft.*message',
    'music': r'play.*music|spotify|sonos',
}
```

Identify:
- **Frequently used** — Working well, keep
- **Never used** — Consider deprecating or improving description
- **Often corrected** — Needs refinement

### 3. Memory/Config Bloat Check

```bash
wc -l ~/.claude/projects/-Users-terry/memory/MEMORY.md ~/CLAUDE.md
```

| File | Threshold | Action |
|------|-----------|--------|
| MEMORY.md | >150 lines | Audit for tool-specific content that belongs in skills |
| CLAUDE.md | >160 lines | Audit for detailed content that belongs in skills or docs/solutions |

If over threshold: scan each section and ask "is this a behavioral rule (stays) or tool-specific reference (move to skill)?"

### 4. Drift Detection

For each active skill, check:

| Check | How |
|-------|-----|
| **Vault references valid?** | Do paths in skill still exist? |
| **Vocabulary aligned?** | Does skill terminology match current vault notes? |
| **Workflow still accurate?** | Has the process changed since skill was written? |
| **Context shifted?** | Has a hook, tool, or other skill made parts of this skill redundant? A component can be correct but no longer worth its weight. See `~/docs/solutions/patterns/tightening-pass.md`. |

### 5. Gap Analysis

Review recent sessions for patterns:
- Tasks done manually that could be skills
- Repeated multi-step workflows
- Questions asked that required vault deep-dives

### 6. Output

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

### 7. External Inspiration

Quick skim of releases/READMEs for new patterns worth cherry-picking. Don't adopt wholesale — just note anything novel.

| Repo | What to watch for |
|------|-------------------|
| [obra/superpowers](https://github.com/obra/superpowers/releases) | Skill methodology, discipline enforcement |
| [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | Hook patterns, observability |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Domain-specialized skill design |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | Planning workflows |
| [parcadei/Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) | Context management, state persistence |

### 8. Save to Vault

Save review to `/Users/terry/notes/Skill Review - YYYY-MM.md`

## Quick Checks (Weekly)

Lighter version for weekly reset:

1. Any skills invoked incorrectly this week?
2. Any manual workflows repeated 3+ times?
3. Any skill descriptions that confused routing?

## Related Skills

- `design-skill` — How skills should be structured
- `vault-search` — Finding content skills reference
