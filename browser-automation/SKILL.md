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
- **Profile:** `~/chrome-debug-profile/` — copied from main Chrome profile (trimmed to ~700MB)
- **Always-on CDP:** port 9222 available whenever Chrome is running
- **Original Chrome.app** still installed but not used for daily browsing

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

## Two Modes

| Mode | Command prefix | Use case |
|------|---------------|----------|
| **Headless** | `agent-browser` | Public web, scraping (ephemeral) |
| **Authenticated** | `agent-browser --cdp 9222` | Any site requiring login — LinkedIn, Gmail, career portals, etc. |

**Authenticated mode** is the default for most tasks since CDP is always available.

**Persistent sessions** (`--session <name>`) are a fallback for when CDP Chrome isn't running.

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

## Form Filling: JS eval vs Playwright fill

- **Playwright `fill`** fires proper events that update React/Angular state — prefer this
- **JS `eval`** with `nativeInputValueSetter` updates DOM only — framework state may not sync
- **Workday career portals** block Playwright actions entirely (anti-automation) — see `~/docs/solutions/browser-automation/workday-anti-automation.md`
- For Workday: use automation for login + CV upload + simple fields, manual for dropdowns on later steps

## Shell Quoting for eval

Smart quotes cause SyntaxError. For complex JS, use heredoc:
```bash
cat > /tmp/script.js << 'EOF'
// your JS here
EOF
agent-browser --cdp 9222 eval "$(cat /tmp/script.js)"
```

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
