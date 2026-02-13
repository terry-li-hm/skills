---
name: browser-automation
description: Reference skill for agent-browser CLI automation. Not user-invocable — use as internal guidance.
user_invocable: false
platform: claude-code
platform_note: Primary browser automation tool. Zero token overhead when idle. Replaces Chrome MCP for most tasks.
---

# agent-browser CLI Reference

Zero token overhead. Invoked via Bash.

## Three Modes

| Mode | Command prefix | Use case |
|------|---------------|----------|
| **Headless** | `agent-browser` | Public web, scraping (ephemeral) |
| **Persistent** | `agent-browser --session <name>` | Sites requiring login via agent-browser (cookies persist across runs) |
| **Authenticated** | `agent-browser --cdp 9222` | LinkedIn, Gmail, WhatsApp, X (Terry's own Chrome) |

**Persistent mode** keeps cookies/state between runs. Use `--headed` for initial login, then headless for subsequent visits. Name sessions by site (e.g., `--session manulife`, `--session workday`).

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

## Persistent Session Workflow

```bash
# First time: headed so user can log in
agent-browser --session manulife --headed open https://careers.manulife.com
# User logs in manually...

# Subsequent runs: headless, cookies remembered
agent-browser --session manulife open https://careers.manulife.com/jobs/12345
agent-browser --session manulife snapshot -i
agent-browser --session manulife fill @ref_3 "answer"
```

**Default to persistent sessions** for any site requiring login. Prefer `--session <site-name>` over ephemeral headless mode when form-filling or applying to jobs.

## Tips

- `snapshot` over `screenshot` for token efficiency (text vs image tokens)
- `get text` is the best way to extract article content
- Use `--headed` to see the browser window (debugging or initial login)
- Sessions persist between commands — no need to re-open
- Persistent sessions (`--session`) persist cookies across separate CLI invocations
- Check `lsof -i :9222` to verify Chrome CDP is running
