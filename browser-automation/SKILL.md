---
name: browser-automation
description: Reference skill for agent-browser CLI automation. Not user-invocable — use as internal guidance.
user_invocable: false
platform: claude-code
platform_note: Primary browser automation tool. Zero token overhead when idle.
---

# agent-browser CLI Reference

Zero token overhead. Invoked via Bash.

## Setup

Persistent profile configured via environment variable in `~/.zshenv`:
```
export AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile"
```
Cookies, logins, and local storage persist across sessions automatically.

## Two Modes

| Mode | Command | Use case |
|------|---------|----------|
| **Headless** | `agent-browser open <url>` | Public web, scraping (uses persistent profile) |
| **Headed** | `agent-browser --headed open <url>` | Debugging, initial login to sites |

For first-time login to a site, use `--headed` so you can see and interact with the login flow. After that, cookies persist in the profile.

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

**Warning:** `snapshot <url>` and `open <url>` can snapshot/load the **existing active tab** instead of navigating. Always navigate first via `eval`, then snapshot separately:
```bash
agent-browser eval "window.location.href = 'https://target.com'"
sleep 8
agent-browser snapshot
```

## Login-Required Sites

With the persistent profile, sites stay logged in between sessions. First-time setup:
```bash
agent-browser --headed open https://linkedin.com
# Log in manually in the browser window, then close
```
After that, headless works:
```bash
agent-browser open https://linkedin.com/feed
agent-browser snapshot
```

Common authenticated sites: LinkedIn, X/Twitter, Gmail, career portals.

## Useful Commands

```bash
agent-browser get title          # page title
agent-browser get url            # current URL
agent-browser get text           # full page text
agent-browser get text "article" # text from specific element
agent-browser eval "document.title"  # run JS
agent-browser scroll down 500    # scroll
agent-browser press Enter        # keyboard
agent-browser screenshot         # screenshot to stdout
```

## Form Filling: fill vs type vs eval

**Use `fill`, not `type`** for React/Angular inputs. `type` simulates keystrokes but doesn't trigger React's `onChange` — text appears but submit buttons stay disabled. `fill` fires proper synthetic events.

```bash
# BAD — React won't detect this
agent-browser type --text "my message" --ref "input[0]"

# GOOD — triggers proper React events
agent-browser fill --text "my message" --ref "input[0]"
```

Only use `type` when you need character-by-character simulation (autocomplete testing). Note: `type` APPENDS, `fill` REPLACES.

**Workday career portals** block Playwright actions entirely (anti-automation) — see `~/docs/solutions/browser-automation/workday-anti-automation.md`. Use automation for login + CV upload + simple fields, manual for dropdowns.

## Refs Shift After Actions

After any action (click, fill, scroll), element refs become stale — DOM mutations invalidate the index. **Always re-snapshot before each action:**

```bash
agent-browser snapshot          # get refs
agent-browser click --ref "button[2]"
agent-browser snapshot          # MUST re-snapshot — refs shifted
agent-browser fill --ref "input[0]" --text "hello"  # now safe
```

Anti-pattern: chaining multiple actions using refs from a single snapshot.

## SPA Page Load (Workday, etc.)

Heavy SPAs often timeout on `open` (waits for `load` event). Workaround:
```bash
agent-browser eval "window.location.href = 'https://example.com'"
sleep 5
agent-browser get url  # Verify
```

## Shell Quoting for eval

Smart quotes cause SyntaxError. For complex JS, use heredoc:
```bash
cat > /tmp/script.js << 'EOF'
// your JS here
EOF
agent-browser eval "$(cat /tmp/script.js)"
```

## Reliability Tier List

### Always works
- `get url`, `get title`, `eval "JS"`, `snapshot`, `upload`

### Usually works
- `fill @ref "text"`, `check "#id"`, `select @ref "value"` (simple dropdowns), `press "Enter"/"Tab"`

### Unreliable on heavy SPAs
- `click @ref`, `fill @ref` on complex widgets, `scrollintoview @ref`, `open "url"`

### Never works
- Headless on career sites (anti-bot), JS `.value =` for React state sync

### Fallback Table

| Fails | Do instead |
|-------|-----------|
| `open "url"` timeout | `eval "window.location.href = 'url'"` + `sleep 5` |
| `click @ref` timeout | `eval "document.querySelector('selector').click()"` |
| `fill` doesn't sync React | `fill @ref "text"` + `press "Tab"` (blur triggers state) |
| `snapshot` timeout | `eval` to extract form fields directly |
| All Playwright actions timeout | Form is automation-proof — manual for submission |

**Quick rule:** `eval` for navigation/clicks, `fill @ref` + `Tab` for text inputs, `upload` for files, `check "#id"` for checkboxes. Only dropdowns on heavy SPAs need manual interaction.

## Tips

- `snapshot` over `screenshot` for token efficiency (text vs image tokens)
- `get text "selector"` for element text
- Use `--headed` to see the browser window (debugging or initial login)
- Sessions persist between commands — no need to re-open
- **Keep agent-browser updated:** `pnpm update -g agent-browser`
