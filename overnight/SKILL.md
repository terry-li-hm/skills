---
name: overnight
description: "Check overnight queue results and manage tasks. 'overnight', 'overnight results', 'queue status'"
user_invocable: true
---

# Overnight Queue

Check results from the nightly queue and manage tasks.

## Triggers

- `/overnight` — show last run summary
- `/overnight results` — show detailed results from last run
- `/overnight add` — help add a new task to the queue

## Architecture

- **Queue file:** `~/notes/opencode-queue.yaml`
- **Runner:** `~/scripts/opencode-queue.py` (uv script, supports OpenCode + Gemini CLI backends)
- **Shell wrapper:** `~/scripts/opencode-nightly.sh`
- **LaunchAgent:** `com.terry.opencode-nightly` — runs at **10pm HKT daily**
- **Output:** `~/.cache/opencode-runs/<date>/` — one dir per run, task subdirs with stdout.txt + metadata.json
- **Rotation:** Runs older than 7 days auto-deleted at start of each run
- **Cron logs:** `~/.cache/opencode-runs/cron-<date>.log`

## Backends

| Backend | When | Cost | Web access |
|---------|------|------|------------|
| `opencode` (default) | Code review, file analysis, local tasks | Free (GLM-5) | No |
| `gemini` | Web scraping, news, anything needing URLs | Free (1500 RPD) | Yes |

Set `backend: gemini` on any task in the queue YAML.

## Default: Show Last Run Summary

```bash
# Find latest run directory
LATEST=$(ls -dt ~/.cache/opencode-runs/2026-*/ 2>/dev/null | head -1)
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

1. Ask for: name, title, backend (opencode/gemini), working_dir, timeout, prompt
2. Remind: OpenCode prompts must be <4K chars, use file paths not inline content
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

# List tasks
uv run ~/scripts/opencode-queue.py --list
```

## Current Enabled Tasks

| Task | Backend | What it does |
|------|---------|-------------|
| nightly-git-review | opencode | Review commits across 7 repos |
| claude-md-freshness | opencode | Spot-check CLAUDE.md paths |
| weekly-security-scan | opencode | CVE + secrets scan |
| skill-health-check | opencode | Verify SKILL.md exists |
| hkma-sfc-sweep | **gemini** | Regulatory developments (needs web) |
| lustro-digest | **gemini** | AI news summary (needs web) |
| vault-health-check | opencode | Broken links, overdue TODOs |
| garp-drill | opencode | Generate 5 practice questions |
| solutions-dedup | opencode | Find duplicate/stale docs |
| morning-dashboard | opencode | Synthesize all outputs |

## Notes

- GLM-5 is free and unlimited — no cost concern
- Gemini CLI: ~4-8 requests/night, well within 1500 RPD limit
- OpenCode uses lean config (`OPENCODE_HOME=~/.opencode-lean`) — no MCPs, faster startup
- Queue runs sequentially — total runtime ~25-40 min for 10 tasks
- `uv run --python 3.13` in LaunchAgent to avoid system Python fallback
