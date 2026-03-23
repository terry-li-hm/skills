---
name: arousal
description: "Check async queue results and manage tasks. 'arousal', 'overnight results', 'queue status', 'what ran'"
model: sonnet
user_invocable: true
---

# Overnight Agent Results

## Triggers

- `/arousal` — show morning dashboard brief
- `/arousal results` — drill into individual task outputs
- `/arousal add` — help add a new task to the queue

## Default: Show Morning Brief

```bash
overnight-gather brief
```

Finds the latest morning-dashboard output and flags NEEDS_ATTENTION lines. Present as a scannable summary.

## Results: Drill Into Individual Tasks

```bash
overnight-gather results                  # list all tasks with status
overnight-gather results --task <name>    # read specific task output
overnight-gather list                     # show last 5 runs with pass/fail
```

## Manual Dispatch

```bash
kinesin run <name>      # fire immediately, detached
kinesin list            # show all tasks + schedules
kinesin results <name>  # show latest output for a task
kinesin cancel <name>   # disable a task
```

## Add: New Task

1. Add entry to `~/notes/opencode-queue.yaml` (name, title, backend, timeout, schedule, prompt)
2. Create CalendarInterval plist in `~/officina/launchd/com.terry.kinesin-<name>.plist`
3. Copy to `~/Library/LaunchAgents/` and `launchctl load`
4. Verify with `kinesin list`
