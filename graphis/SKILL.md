---
name: graphis
description: Manage Telegram bots — create, delete, list via BotFather. Use when creating a new bot, retiring an old one, or rotating a token. Companion to deltos (sends snippets).
user_invocable: false
---

# graphis

Rust CLI that manages Telegram bots via BotFather using MTProto (grammers crate). No browser needed — talks directly to Telegram as your user account.

Companion to `deltos` (Greek "tablet" → sends snippets). graphis (Greek "stylus" → shapes the bots).

## Commands

```bash
# Create a new bot — tries usernames in order until one is accepted
graphis create "DisplayName" UsernameBot AltUsernameBot FallbackBot

# Delete a bot
graphis delete @TekmarBot

# List your bots
graphis list
```

On successful `create`: token saved to keychain (`telegram-bot-token`), username saved (`telegram-bot-username`). deltos picks these up automatically.

## Prerequisites

```bash
# 1. Get API credentials from https://my.telegram.org → API Development Tools
# Add to ~/.zshenv:
export TELEGRAM_API_ID="12345678"
export TELEGRAM_API_HASH="abc123..."

# 2. First run: interactive auth (phone number + SMS code + optional 2FA)
#    Session persists to ~/.local/share/graphis/session.bin — no re-auth needed after.
graphis list   # triggers auth on first run
```

## Files

- Binary: `~/.local/bin/graphis` → `~/code/target/release/graphis`
- Source: `~/code/graphis/`
- Session: `~/.local/share/graphis/session.bin`

## Rebuild

```bash
cd ~/code/graphis && cargo build --release
```

## Bot token rotation workflow

1. `graphis create "Name" NameBot AltNameBot` — tries candidates, saves token to keychain
2. Send `/start` to the new bot in Telegram (required before bot can message you)
3. Test: `echo "test" | deltos`
4. Old bot: `graphis delete @OldBot`

## Gotchas

- **`TELEGRAM_API_ID` / `TELEGRAM_API_HASH` must be set** — from my.telegram.org, not the bot token. These are your *user* app credentials.
- **First-run auth is interactive** — must run in a real TTY. Run `graphis list` once in terminal before using in scripts.
- **Send `/start` to new bots** — Telegram requires users to initiate contact before a bot can message them. deltos returns "chat not found" until this is done.
- **CamelCase usernames preferred** — e.g. `TekmarBot` not `tekmar_bot`.
- **Popular names are taken** — try 3-4 candidates. StrixBot, SemaBot, PraecoBot, VoxBot, RemaBot all taken (Mar 2026). TekmarBot was available.
- **BotFather parsing** — relies on BotFather's response text. If BotFather changes phrasing, parsing may break.
- **macOS only** — keychain integration uses `security` CLI.

## Browser fallback (if MTProto auth fails)

Chrome CDP approach still works — requires Chrome launched with `--remote-debugging-port=9222`.
Scripts at `~/docs/solutions/telegram-web-cdp-automation.md`.

## Current bot

`@TekmarBot` — Greek *tekmar* "a fixed sign, token". Created Mar 2026.
Token in keychain: `telegram-bot-token`.
