---
name: legatus
description: Manage the background AI agent job queue — add tasks, list status, dispatch immediately, cancel, view results. Use when queueing a task for the overnight runner or dispatching a hot (session-independent) job via `legatus run`.
---

# legatus — Background Agent Queue Manager

Manages `~/notes/opencode-queue.yaml`. Hot dispatch via `legatus run <name>` spawns a detached subprocess that survives session close.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `legatus list` | Show all tasks + status |
| `legatus add "<prompt>"` | Add to overnight queue |
| `legatus add "<prompt>" --now` | Add + mark for immediate dispatch |
| `legatus run <name>` | Dispatch immediately (detached, survives session close) |
| `legatus batch` | Run all enabled tasks sequentially (overnight runner) |
| `legatus batch --task <name>` | Run a single task synchronously |
| `legatus batch --dry-run` | Preview what would run, no execution |
| `legatus cancel <name>` | Disable task, clear run_now |
| `legatus results <name>` | Show latest run output |
| `legatus results` | List all tasks with results |

## Common Patterns

### Queue a task for tonight's overnight run
```bash
legatus add "audit MEMORY.md for hook candidates" --backend claude --name memory-audit
```

### Dispatch immediately (no overnight wait)
```bash
legatus add "summarise ~/docs/solutions/ changes this week" --name weekly-summary --now
legatus run weekly-summary
# Survives CC session close — check results after:
legatus results weekly-summary
```

### Dispatch + forget
```bash
legatus add "review ~/skills/ for staleness" --name skill-review --backend claude --now
legatus run skill-review
# Results land in ~/.cache/opencode-runs/hot-skill-review.log
```

## Batch Runner

`legatus batch` is the synchronous overnight runner — replaces `opencode-queue.py`. Called by the LaunchAgent via `~/scripts/opencode-nightly.sh`.

- Runs enabled tasks sequentially with per-task timeout (default 300s)
- Writes `stdout.txt`, `stderr.txt`, `metadata.json` per task
- Writes `run-summary.json` + `summary.md` across all tasks
- Rotates runs older than 7 days automatically
- `--task <name>`: run a single named task (regardless of enabled flag)
- `--dry-run`: print what would run, no subprocess spawned, no files written

```bash
# Manual overnight run
legatus batch

# Test a specific task
legatus batch --task memory-audit

# Preview the queue
legatus batch --dry-run
```

## File Locations
- **Queue:** `~/notes/opencode-queue.yaml`
- **Batch results:** `~/.cache/opencode-runs/<YYYY-MM-DD-HHMM>/<task>/`
  - `stdout.txt`, `stderr.txt` — raw output
  - `metadata.json` — status, duration, exit code
  - `<name>.md` — stdout copy for Claude/Gemini backends
- **Batch summary:** `~/.cache/opencode-runs/<timestamp>/summary.md`
- **Hot dispatch logs:** `~/.cache/opencode-runs/hot-<name>.log`

## Backend Options
- `opencode` (default) — free, unlimited
- `claude` — Claude Code CLI, uses Max plan credits
- `gemini` — Gemini CLI, `--yolo` mode
- `codex` — Codex CLI, `--sandbox danger-full-access`, good for multi-file/Rust tasks

## Gotchas
- **Duplicate names error:** `legatus cancel <name>` first, then re-add
- **`run_now` field:** set by `--now` flag, cleared by `cancel`. Overnight batch also picks up `run_now: true` tasks
- **Log vs results:** `legatus run` → `hot-<name>.log` (live); batch → `~/.cache/opencode-runs/<timestamp>/<name>/stdout.txt`
- **Session independence:** `legatus run` spawns a detached subprocess. Session can close; job keeps running.
- **Timeout + orphans:** `legatus batch` SIGKILLs the direct child on timeout. Grandchildren spawned by claude/gemini/opencode are not reaped — they may outlive the timeout.
- **CLAUDECODE env:** stripped for Backend::Claude so nested claude invocations aren't blocked.
- **Post-run reporting:** `legatus-notify` runs automatically after each batch window — writes `~/.cache/opencode-runs/latest-summary.md` and sends a Telegram ping. Run manually: `legatus-notify`.

## Source
`~/code/legatus/` — Rust, clap 4, serde_yaml 0.9. GitHub: `terry-li-hm/legatus` (private).
