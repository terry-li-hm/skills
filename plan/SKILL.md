---
name: plan
description: Transform feature descriptions into well-structured project plans following conventions. Research, validate, and create actionable plans.
---

# Plan

Transform feature descriptions, bug reports, or improvement ideas into well-structured markdown plans.

## Trigger

Use when:
- User says "plan this" or "create a plan for"
- Starting a new feature
- User has a feature description or idea

## Inputs

- Feature description (required, or ask if missing)
- Plan detail level (minimal/standard/comprehensive - auto-detect based on complexity)

## Workflow

### Phase 1: Idea Refinement

**Check for brainstorm documents first:**

```bash
ls -la docs/brainstorms/*.md 2>/dev/null | head -10
```

If a relevant brainstorm exists (matching topic, within 14 days):
1. Read it
2. Announce: "Found brainstorm from [date]. Using as context."
3. Skip refinement questions

**If no brainstorm, refine via dialogue:**

Ask questions one at a time:
- Purpose: What problem does this solve?
- Constraints: Any hard requirements?
- Success criteria: How do we know it's done?

Continue until clear or user says "proceed".

### Phase 2: Research

**Run parallel subagents:**

```
Task explore("Find relevant files, patterns, and conventions in this codebase for: {feature_description}")
Task explore("Search docs/solutions/ and docs/learn/ for related learnings to: {feature_description}")
```

**Decide on external research:**
- High-risk (security, payments, external APIs) → always research
- Strong local context → skip external
- Uncertainty → research

**If external research needed:**

```
Task general("Research best practices for: {feature_description}. Search for current patterns and gotchas.")
```

### Phase 3: Plan Structure

**Choose detail level:**

| Level | Best For | Sections |
|-------|----------|----------|
| **minimal** | Simple bugs, small improvements | Problem, Acceptance Criteria, Context |
| **standard** | Most features, complex bugs | Overview, Problem, Solution, Technical Considerations, Acceptance Criteria |
| **comprehensive** | Major features, architecture changes | Full structure with phases, alternatives, risk analysis |

**Auto-detect:** If feature description > 100 words or mentions multiple systems → comprehensive. Otherwise standard.

### Phase 4: Create Plan File

**Filename:** `docs/plans/YYYY-MM-DD-<type>-<descriptive-name>-plan.md`

**Example:** `2026-01-29-feat-user-auth-flow-plan.md`

**Template (standard level):**
```markdown
---
title: [Issue Title]
type: [feat|fix|refactor]
date: YYYY-MM-DD
---

# [Issue Title]

## Overview

[Brief description]

## Problem Statement / Motivation

[Why this matters]

## Proposed Solution

[High-level approach]

## Technical Considerations

- Architecture impacts
- Performance implications
- Security considerations

## Acceptance Criteria

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Testing requirements

## References

- Similar code: [file_path:line_number]
- External docs: [url]
```

## Output

1. Write plan to `docs/plans/YYYY-MM-DD-*-plan.md`
2. Present options:
   - Open in editor
   - Run `/work` to start implementing
   - Create GitHub issue

## Examples

```
User: "Plan a user authentication system"
→ Creates docs/plans/2026-01-29-feat-user-auth-plan.md

User: "Plan: fix the race condition in checkout"
→ Creates docs/plans/2026-01-29-fix-checkout-race-plan.md
```
