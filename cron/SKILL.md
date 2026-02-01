---
name: cron
description: List all scheduled automation (system crontab + OpenClaw crons). Use when checking what's running automatically.
user_invocable: true
---

# /cron

List all scheduled jobs across both systems.

## Usage

Run both commands:

```bash
echo "=== System crontab ===" && crontab -l && echo "" && echo "=== OpenClaw crons ===" && openclaw cron list
```

## Management

```bash
# System crontab
crontab -e                      # Edit
crontab -l                      # List

# OpenClaw crons
openclaw cron list              # List all
openclaw cron add --help        # Add new job
openclaw cron remove <id>       # Remove job
openclaw cron disable <id>      # Disable without removing
openclaw cron enable <id>       # Re-enable
openclaw cron run <id>          # Trigger immediately
```
