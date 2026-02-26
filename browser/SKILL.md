---
name: browser
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

**Profile gotcha:** The persistent profile may redirect to previously-open pages (e.g. localhost:8001). For external forms or one-off pages, use a clean browser: `agent-browser close` first, then `AGENT_BROWSER_PROFILE="" agent-browser open <url>` to skip the profile.

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

## Command Sequencing

**Strictly sequential.** Never fire a second command before the first returns — concurrent calls jam the daemon with "Resource temporarily unavailable (os error 35)". If one command hangs, wait or `agent-browser close` before retrying.

## Form Filling: fill vs type vs eval

**Use `fill` for SPA form inputs** (Vue, React, Angular). Both `fill` and `type` use Playwright's native methods that fire proper events, but:

- **`fill <selector> <text>`** — clears field, then sets value. Triggers framework reactivity. Use for most form inputs.
- **`type <selector> <text>`** — appends text character-by-character. Use for autocomplete or when you need keystroke simulation.
- **`eval "input.value = 'x'"`** — **NEVER use for SPA forms.** Bypasses Vue/React reactivity entirely — framework state stays empty even though DOM shows the value.

```bash
# GOOD — Playwright native, triggers Vue/React state updates
agent-browser fill "input" "search term"
agent-browser type "input" "search term"

# BAD — DOM-only, framework state stays empty
agent-browser eval "document.querySelector('input').value = 'x'"
```

Both `fill` and `type` take two positional args: `<selector> <text>`. One arg treats the text as a selector.

**Workday career portals** block Playwright actions entirely (anti-automation) — see `~/docs/solutions/browser-automation/workday-anti-automation.md`. Use automation for login + CV upload + simple fields, manual for dropdowns.

## Refs Shift After Actions

After any action (click, fill, scroll), element refs become stale — DOM mutations invalidate the index. **Always re-snapshot before each action:**

```bash
agent-browser snapshot          # get refs (e.g. @e3, @e7)
agent-browser click "@e3"
agent-browser snapshot          # MUST re-snapshot — refs shifted
agent-browser fill "@e7" "hello"  # now safe with new refs
```

Anti-pattern: chaining multiple actions using refs from a single snapshot.

## eval: Avoid Broad Selectors for Targeted Clicks

When using `eval` to click a button in a specific row, **don't use `querySelectorAll('tr, div')`** — parent containers match too, and `button:last-child` on the parent hits the wrong row's button. Use `snapshot` + `@ref` instead for precise element targeting. If you must use `eval`, scope tightly (e.g. target `tr` only, or match on a unique attribute).

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
- `fill "selector" "text"`, `fill @ref "text"`, `check "#id"`, `check @ref`, `press "Enter"/"Tab"`

### Unreliable
- `select @ref "value"` — hangs on some dropdown implementations (e.g. Cliniko). Use JS eval fallback instead:
  ```bash
  agent-browser eval 'const s = document.querySelectorAll("select")[N]; s.value = "val"; s.dispatchEvent(new Event("change", {bubbles:true}))'
  ```
- `click @ref`, `fill @ref` on complex widgets, `scrollintoview @ref`, `open "url"`

### Never works
- Headless on career sites (anti-bot), JS `.value =` for React state sync

### Fallback Table

| Fails | Do instead |
|-------|-----------|
| `open "url"` timeout | `eval "window.location.href = 'url'"` + `sleep 5` |
| `click @ref` timeout | `eval "document.querySelector('selector').click()"` |
| `eval` value set doesn't sync React | `fill "selector" "text"` (Playwright native) |
| `snapshot` timeout | `eval` to extract form fields directly |
| `select @ref` hangs | `eval` with JS: set `.value` + `dispatchEvent(new Event("change", {bubbles:true}))` |
| `fill @ref` sets wrong field | Native setter: `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(el, text)` + dispatch `input`+`change` events |
| All Playwright actions timeout | Form is automation-proof — manual for submission |

**Quick rule:** `eval` for navigation/reading state, `fill` for text inputs, `click @ref` or `click "selector"` for buttons, `upload` for files, `check "#id"` for checkboxes. Only dropdowns on heavy SPAs need manual interaction.

## Multi-Field Form Filling

Filling long registration forms (e.g. Cliniko, medical intake). Learned patterns:

1. **Use clean browser** for external forms — `AGENT_BROWSER_PROFILE="" agent-browser open <url>`
2. **Fill text fields one at a time** with `fill @ref "value"` — sequential, not chained with `&&`
3. **Dropdowns via JS eval** — `select @ref` hangs on many implementations:
   ```bash
   agent-browser eval 'const s = document.querySelectorAll("select")[INDEX]; s.value = "VALUE"; s.dispatchEvent(new Event("change", {bubbles:true}))'
   ```
4. **Checkboxes** — `check @ref` works reliably
5. **Radio buttons** — `click @ref` works
6. **Screenshot-verify before submit** — scroll top-to-bottom and screenshot each section
7. **If `fill @ref` hits wrong field** — use native setter via eval:
   ```bash
   agent-browser eval 'const el = document.querySelectorAll("input")[0]; Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(el, "text"); el.dispatchEvent(new Event("input", {bubbles:true})); el.dispatchEvent(new Event("change", {bubbles:true}))'
   ```

**Command chaining:** Never chain agent-browser commands with `&&` — the daemon can't handle concurrent requests and throws "Resource temporarily unavailable (os error 35)". Run each command as a separate Bash call.

## Backup: Rodney (simonw/rodney)

Go-based browser automation CLI using Chrome CDP (rod library). Installed at `~/go/bin/rodney`. Use when agent-browser fails or Playwright binaries break.

**Key differences from agent-browser:**
- Persistent Chrome process (client-server model) — each command connects via WebSocket, Chrome keeps running
- Profile data: `~/.rodney/chrome-data/` (cookies/logins persist)
- Accessibility-first: `ax-tree`, `ax-find`, `ax-query` — more robust element targeting than CSS selectors
- No Playwright dependency (pure CDP via rod)

**Quick reference:**
```bash
rodney start [--show]        # launch Chrome (--show = headed)
rodney open <url>            # navigate
rodney text <selector>       # extract text
rodney click <selector>      # click element
rodney input <selector> <text>  # type into input
rodney screenshot [file]     # capture
rodney ax-tree               # accessibility tree (like agent-browser snapshot)
rodney js <expression>       # eval JS
rodney stop                  # shutdown
```

**When to reach for Rodney over agent-browser:**
- Playwright binary installation errors (`launchPersistentContext` failures)
- Element targeting issues where accessibility tree (`ax-find`) would be more robust
- Simpler scripting needs (each command is a separate shell invocation, no session management)

**Limitations (v0.4.0, Feb 2026):** Early-stage. No built-in `fill` equivalent for React state sync. Same CDP fingerprinting issues as agent-browser (Google blocks, anti-bot captchas). No `snapshot`-style ref system — uses CSS selectors or accessibility queries.

## Companion: Showboat (simonw/showboat)

Markdown demo generator for agent work. Not browser automation — pairs with Rodney for screenshots. Useful for creating step-by-step visual proof-of-work documents (e.g., Capco client demos).

```bash
showboat init "Demo Title"       # start doc
showboat note "Explanation..."   # add prose
showboat exec python3 script.py  # run + capture output
showboat image screenshot.png    # embed screenshot
showboat verify                  # re-run all code blocks, diff outputs
```

Not installed yet. Install when needed: `go install github.com/simonw/showboat@latest`

## Known Login Issues

- **Taobao (and likely other Chinese e-commerce):** Triggers anti-bot captcha in headless mode. Use `--headed` for first login + captcha solve, then headless works with persisted cookies.
- **Google:** Blocks Playwright Chromium entirely. Use email/password login, not Google SSO.
- **WeChat Web:** Killed by Tencent — returns "cannot log in to Weixin for Web". Desktop app only.

## Profile Backup

Profile data at `~/.agent-browser-profile/`. Backup location: `~/agent-config/browser-profile/` (Cookies, Local Storage, Sessions).

Restore: `cp -r ~/agent-config/browser-profile/* ~/.agent-browser-profile/`

## Playwright Binaries

After agent-browser updates, Playwright browser binaries may need reinstalling:
```bash
npx playwright install chromium
```
Auto-update script handles agent-browser but not Playwright binaries — fix manually if `launchPersistentContext` errors appear.

## Mobile-Only Sites (Portrait-Only SPAs)

Some ordering/booking platforms (Eats365, etc.) check viewport orientation and refuse to render in landscape. `--viewport 390x844` alone doesn't work — the site checks `isMobile` and touch capability, not just dimensions.

**Fix:** Use `set device` before opening the URL:
```bash
agent-browser close                    # must close first — device applies to new context
agent-browser set device "iPhone 13"   # sets viewport + user agent + isMobile + touch
agent-browser open "https://example.com/menu" --wait 8000
```

**Text extraction from mobile SPAs:** These sites often use inner scroll containers that `scroll down` can't reach. Use JS extraction instead:
```bash
agent-browser eval "document.body.innerText"   # gets ALL rendered text regardless of scroll position
```

This is more reliable than `get text` for SPAs where content loads dynamically into nested scrollable divs.

**Tested working:** Eats365 (restaurant ordering platform used across HK).

## Tips

- `snapshot` over `screenshot` for token efficiency (text vs image tokens)
- `get text "selector"` for element text
- Use `--headed` to see the browser window (debugging or initial login)
- Sessions persist between commands — no need to re-open
- **Keep agent-browser updated:** `pnpm update -g agent-browser`
- **`--profile` flag position:** Either `agent-browser --profile -- open <url>` (with separator) or after the command. Without `--`, `--profile open` treats the URL as an unknown command. If the daemon is already running, `--profile` is ignored with a warning — use `agent-browser close` first to restart with new options.
