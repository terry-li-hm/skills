---
name: browser-automation
description: Reference skill for agent-browser CLI automation. Not user-invocable — use as internal guidance.
user_invocable: false
platform: claude-code
platform_note: Primary browser automation tool. Zero token overhead when idle. Replaces Chrome MCP for most tasks.
---

# agent-browser CLI Reference

Zero token overhead. Invoked via Bash.

## Chrome CDP Setup

Terry's daily Chrome runs with CDP enabled via a wrapper app:

- **App:** `/Applications/Chrome CDP.app` — launches Chrome with `--remote-debugging-port=9222`
- **Profile:** `~/chrome-debug-profile/` — copied from main Chrome profile (trimmed)
- **Always-on CDP:** port 9222 available whenever Chrome is running
- **Launch script:** `/Applications/Chrome CDP.app/Contents/MacOS/launch.sh`
- **Extensions:** Stripped to 5 (1Password, iCloud Passwords, AdGuard, Cookie Dismisser, Obsidian Clipper). Uses `--disable-extensions-except` flag. Reduced CDP targets from 16 to 2-3, eval latency from 1,220ms to 3.5ms avg.
- **Performance flags:** `--disable-background-networking --disable-sync --disable-client-side-phishing-detection` etc.

### Anti-bot pages poison CDP globally
XHS and Zhihu anti-bot JS blocks websocket `recv()` for ALL tabs, not just their own. Always close these pages after use. Stale anti-bot tabs cause all CDP commands to hang.

**Profile refresh:** If cookies/logins get stale, re-copy from main profile:
```bash
osascript -e 'tell application "Chrome CDP" to quit'
rsync -a \
  --exclude='OptGuideOnDeviceModel' \
  --exclude='optimization_guide_model_store' \
  --exclude='extensions_crx_cache' \
  --exclude='component_crx_cache' \
  --exclude='Safe Browsing' \
  --exclude='WasmTtsEngine' \
  --exclude='Crashpad' \
  --exclude='Default/File System' \
  --exclude='Default/Service Worker' \
  --exclude='Default/GPUCache' \
  "$HOME/Library/Application Support/Google/Chrome/" \
  "$HOME/chrome-debug-profile/"
```

## Pre-flight Check

Always verify Chrome CDP is running before any CDP operation:
```bash
pgrep -f "Chrome CDP" >/dev/null || open "/Applications/Chrome CDP.app" && sleep 5
```
Without this, commands timeout with unhelpful errors (`Timeout 10000ms exceeded. waiting for locator(':root')`).

## Two Modes

| Mode | Command prefix | Use case |
|------|---------------|----------|
| **Headless** | `agent-browser` | Public web, scraping (ephemeral) |
| **Authenticated** | `agent-browser --cdp 9222` | Any site requiring login — LinkedIn, Gmail, career portals, etc. |

**Authenticated mode** is the default for most tasks since CDP is always available.

**Persistent sessions** (`--session <name>`) are a fallback for when CDP Chrome isn't running.

## Core Workflow

```bash
agent-browser open https://example.com    # navigate (may timeout on SPAs)
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
agent-browser --cdp 9222 eval "window.location.href = 'https://target.com'"
sleep 8
agent-browser --cdp 9222 snapshot
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
- External career portals (Manulife, Workday, etc.)

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

## Multi-Tab Handling

CDP connects to the active tab. To switch tabs or find a specific one:
```bash
# List all tabs
curl -s http://localhost:9222/json/list | python3 -c "
import sys, json
for t in json.load(sys.stdin):
    if t.get('type') == 'page':
        print(f\"{t['id'][:12]}  {t['url'][:100]}\")
"

# Navigate current tab to target (switches context)
agent-browser --cdp 9222 open "https://target-url.com"
```

## SPA Page Load (Workday, etc.)

Heavy SPAs often timeout on `open` (waits for `load` event). Workaround:
```bash
agent-browser --cdp 9222 eval "window.location.href = 'https://example.com'"
sleep 5  # Wait for SPA to render
agent-browser --cdp 9222 get url  # Verify
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

**JS `eval`** with `nativeInputValueSetter` updates DOM only — framework state may not sync. Use as last resort.

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

## Shell Quoting for eval

Smart quotes cause SyntaxError. For complex JS, use heredoc:
```bash
cat > /tmp/script.js << 'EOF'
// your JS here
EOF
agent-browser --cdp 9222 eval "$(cat /tmp/script.js)"
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

## Playwright CDP Fallback

When agent-browser commands hang or timeout repeatedly, bypass it and connect via Playwright directly:
```python
from playwright.async_api import async_playwright
async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]  # or [-1] for last tab
    text = await page.evaluate("document.body.innerText")
```
Use `curl localhost:9222/json/list` to identify which tab index to target. More reliable than agent-browser for bulk text extraction.

## Tips

- `snapshot` over `screenshot` for token efficiency (text vs image tokens)
- `get text "selector"` for element text (v0.9.3 requires selector arg)
- Use `--headed` to see the browser window (debugging or initial login)
- Sessions persist between commands — no need to re-open
- Check `lsof -i :9222` to verify Chrome CDP is running
- Chrome CDP requires non-default `--user-data-dir` — that's why we use `~/chrome-debug-profile/`
- If no tabs open: `curl -s -X PUT "http://localhost:9222/json/new?about:blank"` to create one
- Close unused tabs to save RAM: `curl -s "http://localhost:9222/json/close/<TAB_ID>"`
- **Keep agent-browser updated:** `pnpm update -g agent-browser` (v0.9.3 fixed EAGAIN errors on 8GB Macs)

## Performance Tiers (Feb 2026)

| Approach | eval latency | snapshot latency | token cost/turn | Use case |
|---|---|---|---|---|
| **Direct CDP websocket** | 3-8ms | 38ms | 0 | Scraping (qianli), speed-critical |
| **Playwright Python** | 17ms | 1,174ms | 0 | Programmatic automation |
| **agent-browser CLI** | 275ms | 1,500ms | 0 | Interactive from Claude Code |
| **Playwright MCP** | ~17ms | ~1,174ms | ~3,700 | Not recommended always-on |

Direct CDP is 349x faster than agent-browser for page eval. Use direct CDP for extraction, agent-browser for interactive actions.

Full comparison: `~/docs/solutions/browser-automation-comparison.md`
