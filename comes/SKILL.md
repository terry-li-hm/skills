---
name: comes
description: "Personal AI life coach CLI (crate: phron). Health monitoring, morning brief, overnight research, proactive nudges. `comes brief`, `comes health`, `comes overnight`, `comes nudge`"
user_invocable: false
---

# comes — AI Life Coach CLI

Crate: `phron` on crates.io. Binary: `comes`. Source: `~/code/phron/`. GitHub: https://github.com/terry-li-hm/phron

## Commands

| Command | What it does |
|---|---|
| `comes health` | Oura readiness → Green/Yellow/Red + HRV + sleep score |
| `comes brief` | Morning brief: health + calendar (fasti) + LLM synthesis |
| `comes nudge` | If Red: moneo Due reminder + Telegram alert |
| `comes overnight` | OpenRouter research per topic → vault digest → Telegram summary |
| `comes status` | Stub (Phase 3) |

## Config

`~/.config/comes/config.toml` — copy from `~/code/phron/config.toml.example`

Key fields:
- `[vault] path` — Obsidian vault root (e.g. `~/notes`)
- `[vault] overnight_dir` — subdir for overnight digests
- `[llm] synthesis_model` — OpenRouter model ID (e.g. `anthropic/claude-sonnet-4-5`)
- `[research] topics` — list of overnight research topics
- `[thresholds] health_red / health_yellow` — Oura score cutoffs

## Required env vars (injected by 1Password)

- `OURA_TOKEN` — Oura personal access token
- `OPENROUTER_API_KEY` — for all LLM synthesis (brief + overnight)
- `TELEGRAM_BOT_TOKEN` — outbound Telegram alerts
- `TELEGRAM_CHAT_ID` — your personal chat ID

## Gotchas

- **`ANTHROPIC_API_KEY` does NOT work for direct API calls** — it's the Claude Code Max plan key, not a pay-per-token API key. All LLM calls route through OpenRouter (`OPENROUTER_API_KEY`). This is by design.
- **OpenRouter model IDs** use `provider/model` format: `anthropic/claude-sonnet-4-5`, `google/gemini-flash-1.5`. Not the same as Anthropic's native model IDs (`claude-sonnet-4-6`).
- **`moneo add` requires `--sync`** — without it, the reminder never reaches iPhone via CloudKit.
- **LaunchAgents exit 0 always** — nudge and overnight commands catch all errors internally and log to `~/logs/comes-*.log`. Never let LaunchAgent retry on business logic failures.
- **config.toml must exist** — binary panics with a clear error if missing. Run `scripts/setup-config.sh` on first install.
- **`cargo install --path .`** to update the installed binary after code changes. `cargo build --release` alone does NOT update `~/.cargo/bin/comes`.

## LaunchAgents

Templates in `~/code/phron/launchd/`. Install:
```bash
cp ~/code/phron/launchd/com.phron.*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.phron.nudge.plist
launchctl load ~/Library/LaunchAgents/com.phron.overnight.plist
```
Logs: `~/logs/comes-nudge.log`, `~/logs/comes-overnight.log`

## Phase roadmap

- **Phase 1+2 (done):** `comes health`, `comes brief`, `comes nudge`, `comes overnight`
- **Phase 3 (next):** Telegram bot (`comes-bot`) — voice message → Whisper → librosa → Claude critique
- **Phase 4:** Status dashboard, amicus integration, pre-meeting auto-brief

## File paths

- Source: `~/code/phron/`
- Config: `~/.config/comes/config.toml`
- State: `~/.config/comes/state.json`
- Vault output: `~/notes/<vault.overnight_dir>/YYYY-MM-DD-digest.md`
- Logs: `~/logs/comes-*.log`
- Plan: `~/officina/docs/plans/2026-03-06-feat-phron-ai-life-coach-plan.md`
- Brainstorm: `~/officina/docs/brainstorms/2026-03-06-life-coach-brainstorm.md`
