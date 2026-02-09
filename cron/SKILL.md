---
name: cron
description: List all scheduled automation (system crontab + cron scripts). Use when checking what's running automatically.
user_invocable: true
---

# /cron

List all scheduled cron jobs.

## Usage

```bash
echo "=== System crontab ===" && crontab -l
```

## Cron Scripts

Custom cron scripts live in `~/scripts/crons/`:

| Script | Schedule | Purpose |
|--------|----------|---------|
| `morning-weather.sh` | 6:45 AM daily | HKO weather → Telegram |
| `capco-morning-brief.sh` | 8:55 AM daily | Capco onboarding prep → Telegram |
| `weekly-capco-brief.sh` | Sun 8:00 PM | Weekly Capco intel → Telegram |

Logs: `~/logs/cron-weather.log`, `~/logs/cron-capco.log`, `~/logs/cron-weekly.log`

## Management

```bash
# System crontab
crontab -e                      # Edit
crontab -l                      # List

# Test a cron script manually
~/scripts/crons/morning-weather.sh
```
