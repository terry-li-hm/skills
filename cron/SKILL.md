---
name: cron
description: List all scheduled automation (LaunchAgents). Use when checking what's running automatically.
user_invocable: true
---

# /cron

List all scheduled automation. All periodic tasks run as LaunchAgents (migrated from cron Feb 2026).

## Usage

```bash
launchctl list | grep com.terry
```

## LaunchAgents

Plists tracked in `~/agent-config/launchd/`, symlinked to `~/Library/LaunchAgents/`.

| Agent | Schedule | Purpose |
|-------|----------|---------|
| `lustro-daily` | 6:30 PM daily | AI news RSS scan → AI News Log |
| `lustro-breaking` | Every 2h, 8am-10pm | Breaking AI news → Telegram |
| `morning-weather` | 6:45 AM daily | HKO weather → Telegram |
| `oura-sync` | 9:00 AM daily | Oura Ring data sync |
| `vault-git-backup` | Every 30 min | Obsidian vault git backup |
| `qmd-reindex` | Every 2h | QMD semantic search re-index |
| `oghma-health` | Every 5 min | Oghma daemon health check |
| `oghma-maintenance` | Sun 6:00 AM | Oghma dedup + purge |
| `wewe-rss-health` | Every 6h | WeWe RSS session health |
| `strip-compaction` | Every 6h | Strip compaction markers from WORKING.md |
| `bread-reminder` | Mon & Wed 6:00 PM | Big Grains bread → Telegram |
| `csb-ai-jobs` | Fri 12:00 PM | CSB AI job vacancies → Telegram |
| `opencode-nightly` | 10:00 PM daily | OpenCode nightly update |
| `update-coding-tools` | 3:00 AM daily | Coding tools update |
| `rotate-logs` | Sun 5:00 AM | Truncate logs to 200 lines |

Logs: `~/logs/`

## Management

```bash
# List all agents
launchctl list | grep com.terry

# Check specific agent
launchctl list com.terry.lustro-daily

# Reload after plist change
launchctl unload ~/Library/LaunchAgents/com.terry.AGENT.plist
launchctl load ~/Library/LaunchAgents/com.terry.AGENT.plist

# Add new agent
# 1. Create plist in ~/agent-config/launchd/
# 2. ln -s ~/agent-config/launchd/com.terry.NAME.plist ~/Library/LaunchAgents/
# 3. launchctl load ~/Library/LaunchAgents/com.terry.NAME.plist
```
