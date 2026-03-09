---
name: nauta
description: Reference skill for web browser automation via agent-browser/Playwright/CDP. Not user-invocable — use as internal guidance.
user_invocable: false
platform: claude-code
platform_note: Primary browser automation tool. Zero token overhead when idle.
---

# agent-browser CLI Reference

> **Why reference, not invocable (Feb 2026):** Browsing isn't a workflow — it's a toolbox. A `/browse <url>` command would be too narrow (just open + screenshot) or too vague (what to do with the page). `/summarize` and `/analyze` already cover URL extraction. This skill loads patterns into context; agent-browser commands handle the rest.

Zero token overhead. Invoked via Bash.

## Setup

Persistent profile configured via environment variable in `~/.zshenv`:
```
export AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile"
```
Cookies, logins, and local storage persist across sessions automatically.

**Fixed (Feb 2026):** `AGENT_BROWSER_PROFILE` is set in `~/.claude/settings.json` `env` field, so it's available in all Bash calls automatically. No manual prefix needed. If it ever breaks: never use `AGENT_BROWSER_PROFILE=1` — that creates a profile at literal path "1".

## When agent-browser Gets Blocked (Public Sites)

Some public sites (e.g. MTR) return "Access Denied" based on Playwright's user-agent — no login involved, so `porta inject` won't help. Clean profile (`AGENT_BROWSER_PROFILE=""`) also doesn't help if the block is server-side.

**Pattern:** Don't fight the block — find an alternative source.
- MTR journey planner blocked → piliapp.com has the same data and isn't protected
- Search for "[site] data alternative" or "[data type] tool" to find a proxy site

**For map-based SPAs** where stations/items aren't in the snapshot refs (rendered as SVG/canvas):
```bash
# Find element by exact text, get its ID
agent-browser eval "[...document.querySelectorAll('*')].filter(e => e.textContent.trim() === 'Wu Kai Sha').map(e => e.tagName + ' id=' + e.id).join('\n')"
# → SPAN id=t103

# Click it
agent-browser eval "document.getElementById('t103').click(); 'clicked'"

# Read sibling value
agent-browser eval "[...document.querySelectorAll('*')].filter(e => e.textContent.trim() === 'Kwun Tong').map(e => e.nextSibling && e.nextSibling.textContent).join('')"
# → "39"
```

## Two Modes

| Mode | Command | Use case |
|------|---------|----------|
| **Headless** | `agent-browser open <url>` | Public web, scraping (uses persistent profile) |
| **Headed** | `agent-browser --headed open <url>` | Debugging, initial login to sites |

For first-time login to a site, use `--headed` so you can see and interact with the login flow. After that, cookies persist in the profile.

**macOS gotcha:** On this machine, `--headed` still spawns `chrome-headless` processes — no visible window appears even via Jump Desktop screen share. For an actual visible browser, use `rodney start --show` instead. For credential injection on login-gated sites, use `op item get "<item>" --fields password --reveal` piped to `agent-browser fill`.

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

## Multi-Tab Flows (same-browser-session verification)

Some sites (e.g. Stripe) require verification to be completed "in another tab of the same browser." The pattern:

```bash
# Tab 0: start the action (e.g. key rotation dialog waiting)
agent-browser open https://site.com/action --profile

# Trigger the action — site sends a verification email/link
agent-browser click @eXX   # starts the flow

# Get the verification link from email (gog/stilus)
LINK=$(gog gmail search "from:site subject:verify" --limit 1 | ...)

# Tab 1: open the link in the SAME browser session
agent-browser tab 1        # switch to existing tab 1 (or creates it)
agent-browser open "$LINK" # navigate tab 1 to the verification link

# Verification succeeds — return to tab 0 to complete
agent-browser tab 0
agent-browser click @eXX   # continue the original flow
```

**Key commands:**
- `agent-browser tab list` — list all open tabs with index
- `agent-browser tab N` — switch active tab to index N
- `agent-browser tab new <url>` — open URL in a new tab (browser must already be running)

**Why `tab new` fails mid-session:** `agent-browser tab new <url>` requires the browser to already be running. If the session died, relaunch with `open --profile` first, then use `tab list`/`tab N` to manage existing tabs.

**Don't use `window.open()` via eval** — agent-browser follows focus to the new window, abandoning the original dialog context. Use `tab N` + `open <url>` instead.

**Stripe-specific (Mar 2026):** Email verification link must be opened in the same browser session as the dashboard. After verification, a TOTP dialog may appear — get the code via `op item get "Stripe" --vault Agents --otp` (requires TOTP field in 1Password item).

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

**LinkedIn profile editing (confirmed Mar 2026):** Navigate directly to edit URLs (e.g. `/in/terrylihm/edit/about/`). Edit modal loads with a `<textarea>` — use native value setter + `input`/`change` events to update content, then click Save ref. About section, name field, and certifications all editable this way.

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

Smart quotes cause SyntaxError. **Heredoc does NOT reliably fix this** — `agent-browser eval "$(cat /tmp/script.js)"` still fails with exit code 1 when the JS contains quotes or special chars. Use Python subprocess instead — bypasses shell interpretation entirely:

```python
import subprocess, json

def ab_eval(js):
    r = subprocess.run(['agent-browser', 'eval', js], capture_output=True, text=True)
    return r.stdout.strip()

# Safe string interpolation into JS:
value = "text with 'quotes' and \"doubles\""
js = f'document.querySelector("input[name=\\"epName\\"]").value = {json.dumps(value)};'
ab_eval(js)
```

## Date Picker Fields — `fill` Doesn't Stick

Some date inputs have calendar pickers that override typed values on blur/change.
`agent-browser fill @ref "21/12/2023"` appears to work but resets to today's date.

**Fix:** Use native value setter via JS + dispatch both events:
```python
js = """
var el = document.querySelector('input[name="dateField"]');
el.value = '21-12-2023';
el.dispatchEvent(new Event('input', {bubbles:true}));
el.dispatchEvent(new Event('change', {bubbles:true}));
"""
subprocess.run(['agent-browser', 'eval', js], capture_output=True, text=True)
```

**Always inspect the date format first** (screenshot + read) — sites vary between DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD.

## Select Option Values — Inspect Before Setting

`select.value = 'Verifiable'` silently fails if the actual option value is `'3'`.
Always inspect first:

```python
js = """
const selects = document.querySelectorAll('select');
const result = [];
selects.forEach((s, i) => {
  const opts = [...s.options].map(o => o.value + ':' + o.text);
  result.push(i + ': ' + opts.join(', '));
});
result.join(' | ');
"""
# Then set using the actual numeric/string value:
# document.querySelectorAll('select')[2].value = '3'
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

## When User Needs to See the Browser (CAPTCHA, Jump/remote desktop)

`agent-browser` is **headless — invisible on screen**, even via Jump Desktop. If the user needs to watch or interact (CAPTCHA, visual confirm), use **osascript JS injection into visible Chrome** instead.

**Workflow:**
1. `open "https://..."` → opens URL in user's visible Chrome
2. Query field names/IDs via osascript
3. Inject values via osascript JS
4. User handles CAPTCHA + final submit

```bash
# Step 1: open URL in visible Chrome
open "https://example.com/register"

# Step 2: discover field names
osascript << 'EOF'
tell application "Google Chrome"
  execute active tab of front window javascript "
    var r = [];
    document.querySelectorAll('input,select').forEach(function(el) {
      r.push(el.tagName+'|'+el.type+'|'+el.name+'|'+el.id);
    });
    r.join('\\n');
  "
end tell
EOF

# Step 3: fill all fields in one injection
osascript << 'EOF'
tell application "Google Chrome"
  execute active tab of front window javascript "
    function setVal(el, val) {
      var s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
      if (s) s.set.call(el, val);
      el.dispatchEvent(new Event('input', {bubbles: true}));
      el.dispatchEvent(new Event('change', {bubbles: true}));
    }
    setVal(document.getElementById('firstname'), 'Terry');
    setVal(document.getElementById('lastname'), 'Li');
    document.getElementById('salutation').value = 'Mr';
    document.getElementById('salutation').dispatchEvent(new Event('change', {bubbles:true}));
    // Uncheck marketing opt-ins:
    ['opt1','opt2'].forEach(function(id) {
      var cb = document.getElementById(id);
      if (cb && cb.checked) cb.click();
    });
    'done';
  "
end tell
EOF
```

**Take a screenshot to verify before telling user to submit:**
```bash
screencapture -x /tmp/form_check.png
# Then Read /tmp/form_check.png to visually confirm
```

**Limitation:** Works on plain HTML forms. React/Angular state-synced forms may not respond — fall back to agent-browser `fill @ref + Tab`.

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

## LinkedIn-Specific Patterns (Mar 2026)

**`wait --load networkidle` times out.** Use fixed-ms wait:
```bash
agent-browser open "https://www.linkedin.com/jobs/view/4380373181/"
agent-browser wait 4000
agent-browser snapshot
```

**Notification onboarding loop.** After a fresh profile, LinkedIn cycles every navigation through notification preference pages. Escape:
```bash
agent-browser close
porta inject --browser chrome --domain linkedin.com   # pull fresh cookies from Chrome
agent-browser open "https://www.linkedin.com/..."
agent-browser wait 4000
agent-browser snapshot
```

**Verify navigation succeeded** before trusting the snapshot:
```bash
agent-browser eval "document.title + ' | ' + window.location.href"
# If still on mypreferences/ URL, repeat the escape pattern
```

**Per-session profiles (Mar 2026).** `~/.zshrc` now sets `AGENT_BROWSER_SESSION=cc-$TMUX_WINDOW` and `AGENT_BROWSER_PROFILE=~/.agent-browser-profile-$WINDOW` per tmux window. Each Claude Code session has its own daemon + profile — no cross-session interference. Run `porta inject` once per window before hitting authenticated sites.

## Profile Backup

Profile data at `~/.agent-browser-profile/`. Backup location: `~/officina/browser-profile/` (Cookies, Local Storage, Sessions).

Restore: `cp -r ~/officina/browser-profile/* ~/.agent-browser-profile/`

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

## URL Discovery on CMS/Wix Sites

Never guess URL paths on Wix, Squarespace, or other CMS-built sites — slugs are often long and non-obvious (e.g. `/physiotherapy-hong-kong-price` not `/price`). Always discover nav links via snapshot first:

```bash
agent-browser open "https://site.com"
agent-browser wait 3000
agent-browser snapshot   # look for nav links with /url: fields — use those exact hrefs
agent-browser eval "window.location.href = 'https://site.com/full-slug-here'"
```

Burned: Jeff Law Physio pricing at `/physiotherapy-hong-kong-price` — guessing `/price` 404s silently.

## Known Footguns

- **`screencapture` returns black when display is sleeping.** The command succeeds but captures nothing. Wake first with `caffeinate -u -t 5`, then screencapture **immediately** — no sleep in between or the display goes back to sleep before the capture fires.

- **osascript JS injection doesn't trigger React state.** `element.value = x` sets the DOM but React ignores it — form submits empty. Use `System Events keystroke` to type into fields instead; keystrokes trigger proper React event handlers.

- **osascript JS injection blocked by site CSP for write operations.** `execute javascript` via osascript works for reading DOM on most sites, but security-conscious sites (X/Twitter, banking) block clicks and form submissions. Fall back to native System Events: `keystroke`, `click at {x, y}`, or `key code`.

- **`--wait` flag creates a directory in CWD.** `agent-browser open "url" --profile --wait 8000` creates a browser profile directory named `--wait/` in the current working directory. Use `sleep` between commands instead of `--wait`.

## Tips

- `snapshot` over `screenshot` for token efficiency (text vs image tokens)
- `get text "selector"` for element text
- Use `--headed` to see the browser window (debugging or initial login)
- Sessions persist between commands — no need to re-open
- **Keep agent-browser updated:** `pnpm update -g agent-browser`
- **`--profile` flag position:** Either `agent-browser --profile -- open <url>` (with separator) or after the command. Without `--`, `--profile open` treats the URL as an unknown command. If the daemon is already running, `--profile` is ignored with a warning — use `agent-browser close` first to restart with new options.

## When agent-browser Is Blocked — Find the Hidden API

Sites that block headless browsers often have unprotected internal API endpoints.
Pattern (used to crack MTR journey planner):

```bash
# 1. Fetch page source directly (curl bypasses bot-blocking)
curl -s "https://site.com/page" | grep -o 'src="[^"]*\.js[^"]*"'

# 2. Grep JS files for API endpoints
curl -s "https://site.com/main.js" | grep -o '"[^"]*\.php[^"]*"\|api/[^"]*"'

# 3. Find AJAX calls to discover params
curl -s "https://site.com/main.js" | grep -B2 -A8 "\.ajax\|fetch("

# 4. Probe the endpoint — error messages reveal correct params
curl -s "https://site.com/api/route/?from=1&to=1"
# → {"errorCode":"3","errorMsg":"The values of o and d cannot be the same"}
# Reveals: params are `o` and `d`, not `from`/`to`
```

Real example: MTR journey planner blocks agent-browser, but
`https://www.mtr.com.hk/share/customer/jp/api/HRRoutes/?o=103&d=15`
returns full route JSON with no auth — discovered via jp_router.js grep.
