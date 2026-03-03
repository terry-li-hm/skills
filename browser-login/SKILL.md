---
name: browser-login
description: Save a website login to the agent-browser profile for future headless access.
user_invocable: true
platform: claude-code
trigger_phrases: ["browser login", "save login", "browser-login"]
arguments: "<url>"
---

# Browser Login

Save a website login to the persistent agent-browser profile so future headless access works without re-authenticating.

## Flow

1. Close any existing agent-browser session
2. Open the target URL in **headed** mode (visible Chromium window)
3. User logs in via Jump Desktop / screen sharing
4. Confirm login succeeded
5. Close headed browser — cookies persist for headless use
6. Verify headless access works
7. Update the authenticated sites table below

```bash
# Step 1: Close existing session
agent-browser close

# Step 2: Open login page in visible browser
agent-browser --headed open "<url>"

# Step 3: Tell user to log in via Jump Desktop
# Step 4: User confirms they're logged in

# Step 5: Close headed browser
agent-browser close

# Step 6: Verify headless access
agent-browser open "<url>"
agent-browser get url  # Should NOT redirect to login
agent-browser get title
```

## Post-Login

After successful login, update the authenticated sites table in `~/docs/solutions/agent-browser-paywalled-auth.md`:

```markdown
| Site | Profile Auth | Notes |
|------|-------------|-------|
| <site> | Yes (<month> <year>) | <notes> |
```

## Authenticated Sites (Quick Reference)

| Site | Login URL | Verified |
|------|-----------|----------|
| LinkedIn | linkedin.com/login | Feb 2026 |
| Substack (Latent Space) | substack.com/sign-in | Feb 2026 |
| Taobao/Tmall | login.taobao.com | Feb 2026 |

## Google OAuth Sites — Use `porta` Instead

If a site only supports Google SSO (e.g. Vercel, Google-gated dashboards), the headed Playwright flow will be blocked by Google's bot detection. Use `porta` instead:

```bash
# 1. Open site in regular Chrome and log in via Google
open -a "Google Chrome" "https://site.com/login"

# 2. Bridge Chrome cookies into agent-browser profile
porta inject --domain site.com

# 3. Verify
agent-browser open "https://site.com/dashboard"
agent-browser get url  # should NOT redirect to login
```

`porta list --domain site.com` to preview what cookies would be injected.
Cookies expire — re-run `porta inject` if access stops working.

## Notes

- User must have visual access to the Mac (Jump Desktop, VNC, or physical screen)
- `AGENT_BROWSER_PROFILE` env var points to `~/.agent-browser-profile/` — set in `~/.zshenv`
- Profile backup: `~/agent-config/browser-profile/`
