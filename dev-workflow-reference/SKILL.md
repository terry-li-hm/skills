---
name: dev-workflow-reference
description: Reference for compound-engineering workflows and review agents. Consult when starting development work.
user_invocable: false
---

# Development Workflow Reference

## Plan Mode vs CE Workflows

Not every task needs compound-engineering. Choose the right weight class:

| Situation | Use | Why |
|---|---|---|
| Single-session, <5 files, need to understand code first | **Claude Code plan mode** (`EnterPlanMode`) | Lightweight, no artifacts, fast in/out |
| "Show me your approach before coding" | **Plan mode** | Zero overhead, just explore + propose |
| Multi-session feature, needs a paper trail | **CE `/workflows:plan`** | Produces a plan document that survives `/clear` |
| Multiple agents will execute the plan | **CE** | Document-driven handoff between sessions |
| Want parallel research via `/deepen-plan` | **CE** | Multi-agent depth that plan mode can't do |

**Default to plan mode.** Reach for CE when the task is big enough to lose context across `/clear` boundaries, or when the plan itself is a deliverable.

## CE Workflow Selection Guide

| Workflow | When to Use | Output |
|----------|-------------|--------|
| `/workflows:brainstorm` | Unclear requirements, exploring WHAT to build | `docs/brainstorms/*.md` |
| `/workflows:plan` | Clear goal, need HOW to implement | `docs/plans/*.md` |
| `/deepen-plan` | Plan exists but needs research depth | Enhanced plan with best practices |
| `/workflows:work` | Plan approved, ready to execute | Code + tests |
| `/workflows:review` | Code complete, quality-critical | Multi-agent review findings |
| `/workflows:compound` | Just solved something tricky | Learning in `~/docs/solutions/` |
| `/lfg` | Full autonomous loop (all above) | End-to-end with video |

**Flow options:**
```
Simple task:
  plan → work → compound (if tricky)

Complex feature:
  brainstorm → plan → deepen-plan → work → review → compound

Full autonomous:
  /lfg (runs the entire chain)
```

## Review Agents

**Review ordering:** Spec compliance BEFORE code quality. Run `pattern-recognition-specialist` (does it match the spec?) before `kieran-*-reviewer` (is it well-built?).

| Agent | Use For |
|-------|---------|
| `code-simplicity-reviewer` | YAGNI check, remove unnecessary complexity |
| `pattern-recognition-specialist` | Spec compliance, anti-patterns, consistency |
| `security-sentinel` | OWASP, secrets, input validation |
| `performance-oracle` | Bottlenecks, scalability concerns |
| `kieran-typescript-reviewer` | High-bar TS review |
| `kieran-python-reviewer` | High-bar Python review |
| `consilium --redteam` | Multi-model security audit (~$1.50). Paste full source into prompt. |

## Git Workflow

Use git worktrees for non-trivial work (see `compound-engineering:git-worktree` skill). Worktree convention: `~/project-worktrees/<branch>/`. Trivial changes (typos, one-line fixes) go directly to main.

## Cross-references

- **Solutions KB:** See `solutions` skill for directory structure and routing rules.
- **Learnings integration:** `/workflows:plan` auto-invokes `learnings-researcher` to check `~/docs/solutions/` for relevant past solutions.
