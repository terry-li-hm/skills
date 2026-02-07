---
name: chrome-automation
description: Reference skill for browser automation via agent-browser CLI. Not user-invocable — use as internal guidance.
user_invocable: false
platform: claude-code
platform_note: Reference for agent-browser CLI. Chrome MCP disabled to save ~15-18K tokens/turn.
---

# Browser Automation Reference

Uses `agent-browser` CLI via Bash. Zero token overhead when idle.

## Two Modes

| Mode | Command | Use case |
|------|---------|----------|
| **Public web** | `agent-browser open <url>` | Scraping, public pages |
| **Authenticated** | `agent-browser --cdp 9222 open <url>` | LinkedIn, Gmail, WhatsApp Web |

Authenticated mode requires Chrome launched with `--remote-debugging-port=9222`.

## Core Commands

```bash
# Navigate
agent-browser open https://example.com

# Read page (accessibility tree with refs — best for AI)
agent-browser snapshot

# Extract text content
agent-browser get text

# Click by ref (from snapshot)
agent-browser click @ref_12

# Type into element
agent-browser type @ref_5 "hello world"

# Fill (clear first, then type)
agent-browser fill @ref_5 "hello world"

# Screenshot
agent-browser screenshot /path/to/file.png

# Get page title/URL
agent-browser get title
agent-browser get url

# Wait for element or time
agent-browser wait 2000
agent-browser wait "button.submit"

# Scroll
agent-browser scroll down 500

# Run JavaScript
agent-browser eval "document.title"
```

## Workflow Pattern

```bash
# 1. Open page
agent-browser open https://example.com

# 2. Wait for load
agent-browser wait 2000

# 3. Get structure (snapshot = accessibility tree with refs)
agent-browser snapshot

# 4. Interact using @ref from snapshot
agent-browser click @ref_3
agent-browser fill @ref_7 "search term"
```

## Authenticated Sessions

```bash
# Connect to running Chrome via CDP
agent-browser --cdp 9222 open https://linkedin.com/feed
agent-browser --cdp 9222 snapshot
agent-browser --cdp 9222 get text
```

Chrome must be launched with: `open -a "Google Chrome" --args --remote-debugging-port=9222`

## Login-Required Sites

These need `--cdp 9222` (authenticated mode):
- LinkedIn
- X/Twitter
- WhatsApp Web
- Gmail (some operations)

## Tips

- `snapshot` > `screenshot` for token efficiency (text vs image)
- `get text` for article extraction (like `get_page_text` was)
- Use `--headed` flag to see the browser window for debugging
- Sessions persist — no need to re-open between commands
- `agent-browser close` to clean up when done
