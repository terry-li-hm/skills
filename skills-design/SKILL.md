---
name: skills-design
description: Reference for designing skills as abstractions. Consult when creating new skills or refactoring existing ones.
user_invocable: false
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

### 4. Close Feedback Loops
Outputs from one skill should feed back into related skills.

```
/debrief → captures interview signals
    ↓
/evaluate-job → uses signals to flag anti-patterns
    ↓
/interview-prep → incorporates learnings
```

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
