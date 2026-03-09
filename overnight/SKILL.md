---
name: overnight
description: "Check async queue results and manage tasks. 'overnight', 'overnight results', 'queue status', 'what ran'"
user_invocable: true
---

# Async Agent Queue

Check results from the latest queue run and manage tasks. The queue runs at **noon + 10pm HKT daily** via LaunchAgent.

## Triggers

- `/overnight` — show last run summary
- `/overnight results` — show detailed results from last run
- `/overnight add` — help add a new task to the queue

## Architecture

- **Queue file:** `~/notes/opencode-queue.yaml`
- **Runner:** `legatus batch` (Rust CLI at `~/.cargo/bin/legatus`)
- **Shell wrapper:** `~/scripts/opencode-nightly.sh`
- **LaunchAgent:** `com.terry.opencode-nightly` — fires at **noon + 10pm HKT daily**
- **Output:** `~/.cache/opencode-runs/<YYYY-MM-DD-HHMM>/` — one dir per run, task subdirs with stdout.txt + metadata.json
- **Latest summary:** `~/.cache/opencode-runs/latest-summary.md` — overwritten after each run
- **Rotation:** Runs older than 7 days auto-deleted at start of each run
- **Notification:** `legatus-notify` sends a Telegram ping after each batch completes

## Backends

| Backend | When | Cost | Web access |
|---------|------|------|------------|
| `opencode` (default) | Code review, file analysis, local tasks | Free (GLM-5) | No |
| `gemini` | Web scraping, news, anything needing URLs | Free (1500 RPD) | Yes |
| `claude` | Vault-aware tasks, skill-level reasoning, peira experiments | Max20 tokens | Yes |
| `codex` | Multi-file code tasks, Rust, repo-nav tasks | Codex credits | Yes |

## Default: Show Last Run Summary

```bash
cat ~/.cache/opencode-runs/latest-summary.md
```

1. Read `latest-summary.md` for pass/fail overview
2. Find latest run dir for detail drilling:
   ```bash
   LATEST=$(ls -dt ~/.cache/opencode-runs/2026-*/ 2>/dev/null | head -1)
   ```
3. Read `$LATEST/morning-dashboard/stdout.txt` for the daily brief (if present)
4. If GARP drill exists, mention "5 GARP questions ready" with path

Present as a quick scannable summary. Flag anything marked NEEDS_ATTENTION or CRITICAL.

## Results: Detailed View

Read `stdout.txt` from each task subdirectory in the latest run. Present findings grouped by:

1. **Action required** — security issues, bugs, broken links
2. **Intel** — regulatory updates, AI news
3. **Study** — GARP drill questions
4. **Maintenance** — dedup, skill health, vault health

## Add: New Task

Walk the user through adding a task to `~/notes/opencode-queue.yaml`:

1. Ask for: name, title, backend (opencode/gemini/claude/codex), working_dir, timeout, prompt
2. Remind: OpenCode prompts must be <4K chars, use file paths not inline content
3. Append to the YAML under the appropriate section
4. Verify with: `legatus list`

## Manual Run

```bash
# Run all enabled tasks now
legatus batch

# Run specific task
legatus batch --task garp-drill

# Dry run (preview only)
legatus batch --dry-run

# List queue
legatus list

# Hot dispatch (detached, immediate, no timeout)
legatus run <name>
```

## Peira Experiments (Overnight)

Queue a peira campaign to run autonomously overnight:

```bash
peira init "topic"          # scaffold campaign + brief.md
# fill in brief.md (target, metric, baseline, budget)
peira-queue                 # adds most recent campaign to queue (enabled: true)
peira-queue --list          # show available campaigns
peira-queue --dry-run       # preview the queue entry
```

The experiment runs via `backend: claude` — full Claude reasoning, writes results directly to `~/notes/Experiments/<campaign>/log.md`. Check results with `/overnight results`.

## Current Enabled Tasks

| Task | Backend | What it does |
|------|---------|-------------|
| nightly-git-review | opencode | Review commits across 7 repos |
| claude-md-freshness | opencode | Spot-check CLAUDE.md paths |
| weekly-security-scan | opencode | CVE + secrets scan |
| skill-health-check | opencode | Verify SKILL.md exists |
| hkma-sfc-sweep | gemini | Regulatory developments (needs web) |
| lustro-digest | gemini | AI news summary (needs web) |
| vault-health-check | opencode | Broken links, overdue TODOs |
| garp-drill | opencode | Generate 5 practice questions |
| solutions-dedup | opencode | Find duplicate/stale docs |
| morning-dashboard | opencode | Synthesize all outputs |

## Notes

- GLM-5 is free and unlimited — no cost concern
- Gemini CLI: ~4–8 requests/run, well within 1500 RPD limit
- OpenCode uses lean config (`OPENCODE_HOME=~/.opencode-lean`) — no MCPs, faster startup
- Queue runs sequentially — total runtime ~25–40 min for 10 tasks
- Noon window: good for tasks queued during the morning; 10pm window: classic overnight
