---
name: codebase-cleanup
description: Iterative codebase cleanup using OpenCode (GLM-4.7). Runs scan → fix → verify cycles to systematically improve code quality. Use when preparing demos, pre-PR cleanup, or onboarding to unfamiliar codebases.
user_invocable: true
---

# Codebase Cleanup

Systematic codebase improvement through iterative scan → fix → verify cycles using OpenCode (GLM-4.7, unlimited quota, ~$0 cost).

## Usage

```
/codebase-cleanup [path] [--depth quick|medium|thorough] [--focus categories] [--scan-only]
```

**Arguments:**
- `path` - Directory to clean (default: current project)
- `--depth` - Number of rounds: quick (3), medium (5), thorough (8)
- `--focus` - Comma-separated categories to prioritize
- `--scan-only` - Report issues without fixing

**Categories:** `dead-code`, `constants`, `helpers`, `memory`, `css`, `imports`, `performance`, `security`

## Process

Run rounds in this order, stopping when findings become structural/risky:

### Round 1-2: Quick Wins
- Unused imports/variables
- Dead code removal
- Console.log cleanup (wrap in DEBUG flag)

### Round 3-4: Extraction
- Repeated code → helper functions
- Magic numbers → constants
- Hardcoded strings → config

### Round 5-6: Quality
- Error handling (bare except → logged)
- Memory leaks (event listeners, unclosed resources)
- CSS/config duplication

### Round 7-8: Polish
- Complex conditionals → helpers
- Import organization
- List comprehensions, next() patterns

### Stop Conditions
- Findings become structural (functions >50 lines, deep nesting)
- Security audit clean
- Diminishing returns (<3 actionable items per round)

## Implementation

For each round, run two OpenCode commands:

### 1. Scan Phase
```bash
opencode run -m opencode/glm-4.7 --title "Scan round N" "Scan [path] for [category] issues.

Already fixed: [list from previous rounds]

Look for:
1. [specific patterns for this round]
2. [specific patterns]

Scan: [file patterns]
List findings with file, line, issue, fix. Skip trivial findings."
```

### 2. Fix Phase
```bash
opencode run -m opencode/glm-4.7 --title "Fix round N" "Fix these issues:

## 1. [Issue from scan]
[specific fix instructions]

## 2. [Issue from scan]
[specific fix instructions]

Verify syntax after each change."
```

### 3. Verify Phase
```bash
python -m py_compile [files] && node --check [js files] && echo "OK"
```

## Example Session

```
User: /codebase-cleanup ~/my-project --depth medium

Claude: Starting codebase cleanup (medium: 5 rounds)...

Round 1: Dead code scan...
- Found 8 unused imports
- Found 3 unused variables
- Found 12 console.logs
Fixing... Done.

Round 2: Helper extraction...
- Found 4 repeated patterns (3+ occurrences each)
Fixing... Done.

[... continues ...]

Summary:
- 5 rounds completed
- 47 issues fixed
- Files modified: 12
- Syntax verified: All pass

Deploy changes?
```

## Best Practices

1. **Always verify syntax** after each fix round
2. **Track fixed categories** to avoid redundant scans
3. **Stop at structural issues** - long functions and deep nesting are risky to auto-refactor
4. **Deploy incrementally** - can deploy after any round
5. **Use --scan-only first** on unfamiliar codebases

## Cost

- Uses OpenCode with GLM-4.7 (unlimited quota on Coding Max plan)
- ~$0 per cleanup session
- Alternative: `opencode/gemini-3-flash` if speed needed
