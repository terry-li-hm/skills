---
name: porta
description: Bridge Chrome cookies into agent-browser profile (solves Google OAuth block)
triggers:
  - porta inject
  - agent-browser google oauth
  - chrome cookies playwright
---

# porta

Bridges Chrome cookies into the agent-browser Playwright persistent profile.
Solves the Google OAuth block (agent-browser can't authenticate via Google SSO).

## Workflow

```
# 1. Log in to the target site in Chrome (normal browser, not headless)
open -a "Google Chrome" "https://site.com/login"
# → user logs in manually

# 2. Bridge cookies to agent-browser profile
porta inject --domain site.com

# 3. Verify headless access works
agent-browser open "https://site.com/dashboard"
agent-browser get url  # should NOT redirect to login
```

## Commands

```bash
# Inject all cookies for a domain
porta inject --domain vercel.com

# Dry-run: see what would be injected
porta inject --domain vercel.com --dry-run

# List cookies for a domain (from Chrome)
porta list --domain vercel.com

# Inject without domain filter (all cookies — use carefully)
porta inject
```

## How it works

1. Copies Chrome's `Default/Cookies` SQLite DB to `/tmp`
2. Decrypts values using `AES-128-CBC` + key from macOS Keychain (`Chrome Safe Storage`)
3. Closes agent-browser and clears `SingletonLock`
4. Uses `uv run playwright` Python to call `ctx.add_cookies()` on the persistent profile
   — required for HttpOnly cookies (JS `document.cookie` can't set them)

## Prerequisites

- `uv` installed
- `playwright` Python package (auto-fetched by `uv run --with playwright`)
- agent-browser profile exists at `~/.agent-browser-profile/`

## Requirements for injection to work

- Chrome must be closed or at least have written the cookies to disk
  (Chrome flushes on close; copying while open usually works but may miss very recent cookies)
- macOS Keychain must be unlocked (`security unlock-keychain` in another tab if locked)

## Install / Update

```bash
cd ~/code/porta && cargo install --path .
```

## Caveats

- Google OAuth cookies are session-bound; they expire after some hours/days
- If Vercel re-prompts for login: re-run `porta inject --domain vercel.com`
- Session cookies (`expires=None`) aren't persisted across browser restarts by Playwright
  by default — test access immediately after injecting

## When porta FAILS — use `browser-login` instead

| Site | Why porta fails | Fix |
|------|----------------|-----|
| **linkedin.com** | `li_at` session is IP + device-fingerprint bound. Injected cookie is silently rejected. | `browser-login` for linkedin.com |
| **cora.computer** | Uses Devise auth (own login form, not Google SSO). No real session cookie in Chrome unless you've logged in there. | `browser-login` for cora.computer |
| Any Google SSO third-party | Google cookies ≠ third-party site session. Injecting .google.com cookies doesn't grant access to the downstream site. | Log in via Google SSO in Chrome first, *then* `porta inject --domain site.com` for that site's cookies |

**Decision rule:** If `agent-browser` redirects to a login page after `porta inject`, the site uses fingerprint-binding or own auth. Switch to `browser-login`.

## Authenticated Sites (via porta)

| Site | Last injected | Status | Notes |
|------|--------------|--------|-------|
| vercel.com | Mar 2026 | ✅ works | Google OAuth, ~20 cookies |
| linkedin.com | Mar 2026 | ❌ fails | IP-bound session |
| cora.computer | Mar 2026 | ⚠️ partial | Cookies inject OK in-context but don't survive profile restart. Fix: `~/scripts/cora_brief.py` |
