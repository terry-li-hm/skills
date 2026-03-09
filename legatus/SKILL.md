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

## File Locations
- **Queue:** `~/notes/opencode-queue.yaml`
- **Overnight runner:** `~/scripts/opencode-queue.py --task <name>`
- **Results dir:** `~/.cache/opencode-runs/<YYYY-MM-DD>/<task>/`
- **Hot dispatch logs:** `~/.cache/opencode-runs/hot-<name>.log`

## Backend Options
- `opencode` (default) — free, unlimited
- `claude` — Claude Code CLI, uses Max plan credits
- `gemini` — Gemini CLI, `--yolo` mode

## Gotchas
- **Duplicate names error:** `legatus cancel <name>` first, then re-add
- **Runner script missing:** `~/scripts/opencode-queue.py` must exist for `legatus run` to work
- **`run_now` field:** set by `--now` flag, cleared by `cancel`. Overnight runner also picks up `run_now: true` tasks
- **Log vs results:** `legatus run` → `hot-<name>.log` (live); overnight run → `~/.cache/opencode-runs/<date>/<name>/stdout.txt`
- **Session independence:** `legatus run` spawns a detached subprocess. Session can close; job keeps running.

## Source
`~/code/legatus/` — Rust, clap 4, serde_yaml 0.9. GitHub: `terry-li-hm/legatus` (private).
