---
name: browser-automation
description: Reference skill for agent-browser CLI automation. Not user-invocable — use as internal guidance.
user_invocable: false
platform: claude-code
platform_note: Primary browser automation tool. Zero token overhead when idle. Replaces Chrome MCP for most tasks.
---

# agent-browser CLI Reference

Zero token overhead. Invoked via Bash.

## Two Modes

| Mode | Command prefix | Use case |
|------|---------------|----------|
| **Headless** | `agent-browser` | Public web, scraping |
| **Authenticated** | `agent-browser --cdp 9222` | LinkedIn, Gmail, WhatsApp, X |

**Authenticated mode** connects to Terry's running Chrome via CDP.
Chrome must be launched with: `open -a "Google Chrome" --args --remote-debugging-port=9222`

## Core Workflow

```bash
agent-browser open https://example.com    # navigate
agent-browser wait 2000                    # let it load
agent-browser snapshot                     # accessibility tree with @refs
agent-browser click @ref_3                 # interact by ref
agent-browser fill @ref_7 "search term"   # clear + type
agent-browser get text                     # extract page text
agent-browser screenshot out.png           # visual capture
agent-browser close                        # cleanup
```

## Authenticated Workflow

```bash
# Prefix every command with --cdp 9222
agent-browser --cdp 9222 open https://linkedin.com/feed
agent-browser --cdp 9222 snapshot
agent-browser --cdp 9222 get text
```

## Login-Required Sites

Always use `--cdp 9222`:
- LinkedIn
- X/Twitter
- WhatsApp Web
- Gmail (some operations)

## Useful Commands

```bash
agent-browser get title          # page title
agent-browser get url            # current URL
agent-browser get text           # full page text (like get_page_text)
agent-browser get text "article" # text from specific element
agent-browser eval "document.title"  # run JS
agent-browser scroll down 500    # scroll
agent-browser press Enter        # keyboard
agent-browser screenshot         # screenshot to stdout
```

## Tips

- `snapshot` over `screenshot` for token efficiency (text vs image tokens)
- `get text` is the best way to extract article content
- Use `--headed` to see the browser window (debugging)
- Sessions persist between commands — no need to re-open
- Check `lsof -i :9222` to verify Chrome CDP is running
