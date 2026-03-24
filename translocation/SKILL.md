---
name: translocation
description: Session-independent AI agent dispatcher — list tasks, dispatch immediately, cancel, view results. Use for any background AI job that should run detached from the current CC session.
context: fork
---

# kinesin — Session-Independent AI Agent Dispatcher

Dispatch any AI agent job detached from the current session — overnight tasks, long research, post-meeting work, slow delegations. Scheduling (if needed) is handled by CalendarInterval LaunchAgents; kinesin itself is scheduling-agnostic.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `kinesin list` | Show all tasks + schedule + status |
| `kinesin run <name>` | Dispatch immediately (detached, survives session close) |
| `kinesin cancel <name>` | Disable task, clear run_now |
| `kinesin results <name>` | Show latest run output |
| `kinesin results` | List all tasks with results |

## Common Patterns

### Dispatch immediately (detached)
```bash
kinesin run vault-health-check
# Survives CC session close — check results after:
kinesin results vault-health-check
```

### Check what's configured
```bash
kinesin list
# Shows: name, backend, status, timeout, schedule (doc only)
```

## Architecture

- **Queue file:** `~/notes/opencode-queue.yaml` — task definitions
- **Scheduling:** individual CalendarInterval LaunchAgents per task (`~/officina/launchd/com.terry.kinesin-*.plist`)
- **Output:** `~/.cache/kinesin-runs/<YYYY-MM-DD-HHMM>/<task>/stdout.txt`
- **Hot dispatch logs:** `~/.cache/kinesin-runs/hot-<name>.log`

## `output_dir` — Auto-Copy Results to Vault

Add `output_dir` to any task definition to auto-copy output files to a persistent location after a successful run:

```yaml
- name: hsbc-desk-research
  output_dir: ~/notes/Capco
  backend: gemini
  ...
```

- If set: copies all files from `~/.cache/kinesin-runs/<timestamp>/<name>/` to `output_dir` on success
- If unset: output stays in cache only (ephemeral — fine for health checks)
- Tilde expansion handled automatically
- Copy failure prints a warning but doesn't fail the run

**Rule of thumb:** health checks → no `output_dir` (disposable). Research deliverables → set `output_dir` (durable).

## Adding a New Task

1. Add entry to `~/notes/opencode-queue.yaml`
2. Create `~/officina/launchd/com.terry.kinesin-<name>.plist` with CalendarInterval
3. `cp ~/officina/launchd/com.terry.kinesin-<name>.plist ~/Library/LaunchAgents/`
4. `launchctl load ~/Library/LaunchAgents/com.terry.kinesin-<name>.plist`
5. Verify: `kinesin list`

## Backend Options
- `opencode` (default) — free, unlimited (GLM-5)
- `claude` — Claude Code CLI, uses Max plan credits
- `gemini` — Gemini CLI, `--yolo` mode, has web access
- `codex` — Codex CLI, `--sandbox danger-full-access`, good for Rust/multi-file

## Gotchas
- **Session independence:** `kinesin run` spawns a detached subprocess. Session can close; job keeps running.
- **CLAUDECODE env:** stripped for Backend::Claude so nested claude invocations aren't blocked.
- **Results location:** `kinesin run` → `hot-<name>.log` (live tail); scheduled → `~/.cache/kinesin-runs/<timestamp>/<name>/stdout.txt`. If `output_dir` set, also copied there.
- **No batch command** — removed. Use `kinesin run <name>` for on-demand dispatch; LaunchAgents handle scheduling.
- **Codex from CC background:** Use `codex exec --full-auto`, NOT interactive `codex "prompt"` (needs TTY). Don't pass `-a never` — conflicts with `--dangerously-bypass-approvals-and-sandbox` in config. See `~/docs/solutions/delegation-reference.md`.
- **Scheduled runs need `kinesin-env` wrapper:** LaunchAgents don't source `.zshenv`, so backends have no API keys. All plists now call `~/bin/kinesin-env` (sources `.zshenv` then exec's kinesin). Fixed Mar 12.

## Source
`~/code/kinesin/` — Rust, clap 4, serde_yaml 0.9. GitHub: `terry-li-hm/kinesin` (private).
