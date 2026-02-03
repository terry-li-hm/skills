---
name: sync-ecc
description: Sync everything-claude-code repo and summarize updates. Use when checking for new patterns, hooks, or skills to adopt.
user_invocable: true
github_url: https://github.com/affaan-m/everything-claude-code
---

# Sync Everything Claude Code

Pull updates from the everything-claude-code reference repo and summarize what's new.

## Workflow

### 1. Pull Latest

```bash
cd ~/everything-claude-code && git fetch origin && git log HEAD..origin/main --oneline
```

If there are new commits, pull them:

```bash
git pull origin main
```

### 2. Show Recent Changes

```bash
# Last 30 days of commits
cd ~/everything-claude-code && git log --since="30 days ago" --oneline --stat | head -100
```

### 3. Summarize What's New

Check each category for changes:

```bash
cd ~/everything-claude-code

# New or modified skills
git diff --name-only HEAD~20 -- skills/

# New or modified hooks
git diff --name-only HEAD~20 -- hooks/

# New or modified commands
git diff --name-only HEAD~20 -- commands/

# New or modified agents
git diff --name-only HEAD~20 -- agents/

# Guide updates
git diff --name-only HEAD~20 -- '*.md' | grep -E "(shortform|longform|README)"
```

### 4. Highlight Potentially Useful Changes

For each changed file, briefly describe what's new and whether it's worth adopting.

Focus on:
- **Hooks** — New hook types or patterns
- **Skills** — New workflow patterns
- **Commands** — Useful shortcuts
- **Guides** — New techniques documented

### 5. Compare Against Terry's Setup

Check if updates address gaps in current setup:

| Their Update | Terry's Current | Worth Adopting? |
|--------------|-----------------|-----------------|
| (describe)   | (what exists)   | Yes/No/Maybe    |

### 6. Output

Produce a summary:

```
EVERYTHING-CLAUDE-CODE SYNC
===========================
Last synced: [date]
Commits since last check: [N]

NEW/UPDATED:
- skills/continuous-learning-v2: Added confidence decay
- hooks/hooks.json: New PreCompact pattern
- commands/evolve.md: Cluster instincts into skills

RECOMMENDED TO ADOPT:
1. [specific item] — [why]

SKIP:
- [items that overlap with existing setup]

Next sync reminder: [date + 30 days]
```

## Notes

- This repo is a reference, not installed as a plugin
- Cherry-pick improvements rather than wholesale adopt
- Terry's setup (vault, OpenCode delegation, compound-engineering) takes precedence
- Focus on hooks and learning patterns — agents/skills overlap with existing setup
