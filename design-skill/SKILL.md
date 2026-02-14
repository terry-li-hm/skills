---
name: design-skill
description: Guide for designing skills. Use when creating new skills, refactoring existing ones, or reviewing skill architecture.
---

# Skills Design Guide

Skills are **abstractions** — just like in software development.

## Skill Types (Abstraction Levels)

| Type | Purpose | `user_invocable` | Example |
|------|---------|------------------|---------|
| **Reference** | Shared knowledge base | `false` | `chrome-automation`, `web-search` |
| **Utility** | Reusable operations | `false` | `judge`, `vault-pathfinding` |
| **Chainable** | Called by other skills | `true` | `evaluate-job` (called by review-saved-jobs) |
| **Workflow** | Orchestrates other skills | `true` | `review-saved-jobs`, `lfg` |
| **Standalone** | Independent operation | `true` | `hko`, `pdf-extract` |

## Skill vs Other Storage

Before creating a skill, check if the knowledge belongs somewhere simpler.

| Signal | Where | Example |
|--------|-------|---------|
| "Always/never do X" (rule) | `CLAUDE.md` | "Never run tccutil reset" |
| "X breaks when Y" (one-line fact) | `MEMORY.md` | "sqlite-vec needs enable_load_extension before load" |
| "When X happens, do steps Y→Z" (procedure with trigger + variants) | **Skill** | `gist-run`: sandbox blocked → create gist → give one-liner |
| "Here's how X works in detail" (deep reference) | `~/docs/solutions/` | Browser automation patterns |

**The test:** If the knowledge fits in one sentence, it's a MEMORY.md bullet. If it has a trigger condition, multiple steps, or variants — it's a skill.

## Design Principles

### 1. DRY — Don't Repeat Yourself
If 3+ skills share the same pattern, extract to a reference skill.

**Examples:**
- Browser automation → `chrome-automation`
- LLM tool selection → `llm-routing` (TODO)
- Vault file paths → `vault-pathfinding` (TODO)

### 2. Chain, Don't Duplicate
Skills should call other skills, not copy their logic.

```
/review-saved-jobs
  └── chains to /evaluate-job
        └── chains to /judge
```

### 3. Reference, Don't Inline
Link to reference skills instead of inlining best practices.

```markdown
## Related Skills
- `chrome-automation` — Browser best practices
```

### 4. Descriptions Carry Instructions
Skill descriptions are seen by all agents. Put "MUST do X" in the description rather than repeating in each agent's instruction file (CLAUDE.md, TOOLS.md, etc). Saves tokens.

**Example:** `/skill-sync` description says "MUST run after creating skills" — no need to repeat in CLAUDE.md.

### 4b. Descriptions = When to Use, NOT What It Does (CSO)

**Tested finding from obra/superpowers:** Descriptions that summarize the skill's workflow cause Claude to follow the description as a shortcut instead of reading the full SKILL.md. A description saying "dispatches subagent per task with code review between tasks" caused Claude to do ONE review, even though the skill's flowchart specified TWO reviews (spec compliance then code quality).

**Fix:** Descriptions should only specify *triggering conditions*. Never summarize the process.

```yaml
# BAD: Summarizes workflow — Claude shortcuts
description: Use when executing plans - dispatches subagent per task with code review between tasks

# GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks in the current session
```

**Audit your skills:** Check descriptions for process summaries and strip them out.

### 5. Close Feedback Loops
Outputs from one skill should feed back into related skills.

```
/debrief → captures interview signals
    ↓
/evaluate-job → uses signals to flag anti-patterns
    ↓
/interview-prep → incorporates learnings
```

### 6. Naming: Verb-First for Actions
- **Action skills** → verb-first: `evaluate-job`, `sync-skills`, `design-skill`
- **Trigger/lookup skills** → short nouns fine: `todo`, `hko`, `morning`

### 7. Self-Contained Skills
Keep scripts/code inside the skill directory, not scattered elsewhere.

**Good:**
```
~/skills/mcp-sync/
  ├── SKILL.md        # Documentation
  └── mcp-sync.py     # Implementation
```

**Bad:**
```
~/skills/mcp-sync/SKILL.md    # Docs here
~/scripts/mcp-sync.py         # Script elsewhere (disconnected)
```

If you need an alias or symlink for convenience, point *from* external location *to* skill:
```bash
ln -sf ~/skills/mcp-sync/mcp-sync.py ~/scripts/mcp-sync.py
```

**Benefits:**
- Version controlled together
- Portable — clone `~/skills` and everything's there
- Single source of truth

## Skill Clusters

### Job Hunting
```
evaluate-job ←→ review-saved-jobs
     ↓              ↓
   judge      chrome-automation
     ↓
  debrief ←→ counter-intel
     ↓
interview-prep → ai-news
```

### Content Extraction
```
evaluate-article
wechat-article     → content-fetch (TODO)
youtube-transcript
pdf-extract
```

### LLM Querying
```
ask-llms ←→ llm-routing (TODO) ←→ llm-council
                ↓
            remote-llm
```

## Reference Skill Template

```yaml
---
name: skill-name
description: Reference for X. Not user-invocable — use as internal guidance.
user_invocable: false
---

# Skill Name

One-line purpose.

## When to Use

- Bullet points

## Patterns

| Pattern | Use Case |
|---------|----------|
| ... | ... |

## Gotchas

| Issue | Solution |
|-------|----------|
| ... | ... |

## Related Skills

- `other-skill` — How it relates
```

## TODO: Reference Skills to Create

| Skill | Purpose | Skills That Benefit |
|-------|---------|---------------------|
| `vault-pathfinding` | Standard file paths, linking conventions | evaluate-job, interview-prep, debrief, counter-intel |
| `llm-routing` | When to use which LLM tool | ask-llms, llm-council, remote-llm |
| `content-fetch` | URL fetching patterns, fallbacks | evaluate-article, wechat-article, youtube-transcript |
| `linkedin-automation` | LinkedIn-specific browser patterns | evaluate-job, review-saved-jobs, counter-intel |

## Audit Findings (Jan 31, 2026)

**High Priority:**
- [x] Create `vault-pathfinding` reference ✓
- [x] Create `llm-routing` reference ✓
- [x] Add feedback loop: debrief signals → evaluate-job ✓

**Medium Priority:**
- [ ] Create `content-fetch` reference
- [ ] Add `/ai-news` reference to `interview-prep`
- [ ] Consolidate job-hunt skills documentation

**Low Priority:**
- [ ] Add `user_invocable: false` to judge, plan, history
- [ ] Add cross-references in skill descriptions
