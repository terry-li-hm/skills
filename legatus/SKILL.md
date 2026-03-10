---
name: legatus
description: Manage the background AI agent job queue — list tasks, dispatch immediately, cancel, view results. Use when dispatching a session-independent AI job via `legatus run`.
---

# legatus — Background Agent Dispatcher

Pure dispatcher for session-independent AI agent jobs. Scheduling is handled by individual CalendarInterval LaunchAgents — legatus itself has no scheduling logic.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `legatus list` | Show all tasks + schedule + status |
| `legatus run <name>` | Dispatch immediately (detached, survives session close) |
| `legatus cancel <name>` | Disable task, clear run_now |
| `legatus results <name>` | Show latest run output |
| `legatus results` | List all tasks with results |

## Common Patterns

### Dispatch immediately (detached)
```bash
legatus run vault-health-check
# Survives CC session close — check results after:
legatus results vault-health-check
```

### Check what's configured
```bash
legatus list
# Shows: name, backend, status, timeout, schedule (doc only)
```

## Architecture

- **Queue file:** `~/notes/opencode-queue.yaml` — task definitions
- **Scheduling:** individual CalendarInterval LaunchAgents per task (`~/officina/launchd/com.terry.legatus-*.plist`)
- **Output:** `~/.cache/opencode-runs/<YYYY-MM-DD-HHMM>/<task>/stdout.txt`
- **Hot dispatch logs:** `~/.cache/opencode-runs/hot-<name>.log`

## Adding a New Task

1. Add entry to `~/notes/opencode-queue.yaml`
2. Create `~/officina/launchd/com.terry.legatus-<name>.plist` with CalendarInterval
3. `cp ~/officina/launchd/com.terry.legatus-<name>.plist ~/Library/LaunchAgents/`
4. `launchctl load ~/Library/LaunchAgents/com.terry.legatus-<name>.plist`
5. Verify: `legatus list`

## Backend Options
- `opencode` (default) — free, unlimited (GLM-5)
- `claude` — Claude Code CLI, uses Max plan credits
- `gemini` — Gemini CLI, `--yolo` mode, has web access
- `codex` — Codex CLI, `--sandbox danger-full-access`, good for Rust/multi-file

## Gotchas
- **Session independence:** `legatus run` spawns a detached subprocess. Session can close; job keeps running.
- **CLAUDECODE env:** stripped for Backend::Claude so nested claude invocations aren't blocked.
- **Results location:** `legatus run` → `hot-<name>.log` (live tail); scheduled → `~/.cache/opencode-runs/<timestamp>/<name>/stdout.txt`
- **No batch command** — removed. Use `legatus run <name>` for on-demand dispatch; LaunchAgents handle scheduling.

## Source
`~/code/legatus/` — Rust, clap 4, serde_yaml 0.9. GitHub: `terry-li-hm/legatus` (private).
