---
name: overnight
description: "Check overnight OpenCode queue results and manage tasks. 'overnight', 'overnight results', 'queue status'"
user_invocable: true
---

# Overnight Queue

Check results from the nightly OpenCode queue and manage tasks.

## Triggers

- `/overnight` — show last run summary
- `/overnight results` — show detailed results from last run
- `/overnight add` — help add a new task to the queue

## Architecture

- **Queue file:** `~/notes/opencode-queue.yaml`
- **Runner:** `~/scripts/opencode-queue.py` (uv script, uses GLM-5)
- **Shell wrapper:** `~/scripts/opencode-nightly.sh`
- **LaunchAgent:** `com.terry.opencode-nightly` — runs at **10pm HKT daily**
- **Output:** `~/notes/opencode-runs/<date>/` — one dir per run, task subdirs with stdout.txt + metadata.json
- **Cron logs:** `~/notes/opencode-runs/cron-<date>.log`

## Default: Show Last Run Summary

```bash
# Find latest run directory
LATEST=$(ls -dt ~/notes/opencode-runs/2026-*/ 2>/dev/null | head -1)
```

1. Read `$LATEST/summary.md` for pass/fail overview
2. Read `$LATEST/morning-dashboard/stdout.txt` for the daily brief
3. If GARP drill exists, mention "5 GARP questions ready" with path

Present as a quick scannable summary. Flag anything marked NEEDS_ATTENTION or CRITICAL.

## Results: Detailed View

Read stdout.txt from each task subdirectory in the latest run. Present findings grouped by:

1. **Action required** — security issues, bugs, broken links
2. **Intel** — regulatory updates, AI news
3. **Study** — GARP drill questions
4. **Maintenance** — dedup, skill health, vault health

## Add: New Task

Walk the user through adding a task to `~/notes/opencode-queue.yaml`:

1. Ask for: name, title, working_dir, timeout, prompt
2. Remind: prompts must be <4K chars, use file paths not inline content
3. Append to the YAML under the appropriate section
4. Verify with: `uv run ~/scripts/opencode-queue.py --list`

## Manual Run

```bash
# Run all enabled tasks now
uv run ~/scripts/opencode-queue.py

# Run specific task
uv run ~/scripts/opencode-queue.py --task garp-drill

# Dry run
uv run ~/scripts/opencode-queue.py --dry-run
```

## Current Enabled Tasks

| Task | What it does | LLM value-add |
|------|-------------|---------------|
| nightly-git-review | Review commits across 7 repos | Judges code quality |
| claude-md-freshness | Spot-check CLAUDE.md paths | Semantic accuracy check |
| weekly-security-scan | CVE + secrets scan | Triages findings |
| skill-health-check | Verify SKILL.md exists | Minimal — could be a script |
| hkma-sfc-sweep | Regulatory developments | Relevance filtering |
| ai-news-digest | AI news summary | Signal vs noise |
| vault-health-check | Broken links, overdue TODOs | Judges staleness |
| garp-drill | Generate 5 practice questions | Core LLM task |
| solutions-dedup | Find duplicate/stale docs | Semantic similarity |
| morning-dashboard | Synthesize all outputs | Prioritization |

## Notes

- GLM-5 is free and unlimited — no cost concern for overnight runs
- OpenCode output capture is unreliable — check session JSON if stdout.txt is empty
- Queue runs sequentially (not parallel) — total runtime ~25-40 min for 10 tasks
- LaunchAgent runs even if Mac is asleep (wakes for scheduled tasks)
