---
name: overnight
description: "Check async queue results and manage tasks. 'overnight', 'overnight results', 'queue status', 'what ran'"
user_invocable: true
---

# Overnight Agent Results

Check results from the overnight legatus runs. Each task runs as its own LaunchAgent on a CalendarInterval schedule — no batch runner, no polling.

## Triggers

- `/overnight` — show morning dashboard brief
- `/overnight results` — drill into individual task outputs
- `/overnight add` — help add a new task to the queue

## Architecture

- **Queue file:** `~/notes/opencode-queue.yaml` — task definitions + schedule documentation
- **Dispatcher:** `legatus run <name>` (pure dispatcher, no scheduling logic)
- **Scheduling:** 7 individual CalendarInterval LaunchAgents in `~/officina/launchd/`
- **Output:** `~/.cache/legatus-runs/<YYYY-MM-DD-HHMM>/<taskname>/` — one dir per dispatch
- **Morning brief:** latest `morning-dashboard` output — see Default section below
- **No Telegram notifications** — surface via `/overnight`, `/auspex`, `/kairos`

## Schedule

| Task | Time | Days |
|------|------|------|
| git-health | 00:30 | Daily |
| vault-health-check | 01:00 | Daily |
| lustro-digest | 01:30 | Daily |
| solutions-dedup | 02:00 | Sunday |
| todo-stale-sweep | 02:15 | Sunday |
| notes-orphan-scan | 02:30 | Sunday |
| morning-dashboard | 03:30 | Daily |

## Default: Show Morning Brief

```bash
overnight-gather brief
```

This finds the latest morning-dashboard output and flags NEEDS_ATTENTION lines. Present as a scannable summary. Use `--json` for structured parsing.

## Results: Drill Into Individual Tasks

```bash
overnight-gather results                  # list all tasks with status
overnight-gather results --task <name>    # read specific task output
overnight-gather list                     # show last 5 runs with pass/fail
```

## Add: New Task

1. Add entry to `~/notes/opencode-queue.yaml` with: name, title, backend, timeout, schedule (doc only), prompt
2. Create a CalendarInterval plist in `~/officina/launchd/com.terry.legatus-<name>.plist`
3. Copy to `~/Library/LaunchAgents/` and `launchctl load`
4. Verify with: `legatus list`

## Manual Dispatch

```bash
legatus run <name>      # fire immediately, detached
legatus list            # show all tasks + schedules
legatus results <name>  # show latest output for a task
legatus cancel <name>   # disable a task
```

## Backends

| Backend | When | Cost |
|---------|------|------|
| `opencode` (default) | File analysis, local tasks | Free (GLM-5) |
| `gemini` | Web synthesis, news, URLs | Free (1500 RPD) |
| `claude` | Vault-aware, complex reasoning | Max20 tokens |
| `codex` | Multi-file code tasks, Rust | Codex credits |
