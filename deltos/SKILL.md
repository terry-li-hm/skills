---
name: deltos
description: Send text/code snippets to Telegram as formatted code blocks for mobile copy-paste. Replaces tg-clip bash script.
---

# deltos

Rust CLI that sends text/code to Telegram as HTML code blocks. Primary copy-paste relay — open your Telegram on mobile and tap to copy.

## Usage

```bash
# Pipe content (most common)
echo "text" | deltos
echo "text" | deltos "label"

# Inline arg (TTY only — won't work in scripts)
deltos "text"
deltos "label" "content"

# Plain mode (URLs, no <pre> wrapper)
echo "https://example.com" | deltos --plain "link"
```

## Config

Credentials live in macOS Keychain. Already set from tg-clip era.

```bash
# Verify
security find-generic-password -s telegram-bot-token -w
security find-generic-password -s telegram-chat-id -w

# Set (if needed)
security add-generic-password -s telegram-bot-token -a "$USER" -w "YOUR_TOKEN" -U
security add-generic-password -s telegram-chat-id  -a "$USER" -w "YOUR_CHAT_ID" -U
```

## Gotchas

- **Inline arg only works in a real TTY.** Scripts and agent shells are non-TTY — `deltos "text"` will wait for stdin. Use `echo "text" | deltos` in scripts.
- **Rate limit:** 1s gap enforced via `/tmp/deltos.lock`. Parallel sends will queue.
- **HTML in content:** `&`, `<`, `>` are escaped automatically. No double-escaping needed.

## Source

`~/code/deltos/` — standalone crate (excluded from `~/code/` workspace).

```bash
cd ~/code/deltos && cargo build --release && cp target/release/deltos ~/bin/deltos
```
