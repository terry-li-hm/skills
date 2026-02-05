---
name: linkedin-cli
description: LinkedIn CLI for checking messages, searching profiles, and browsing feed. Use when user needs LinkedIn data without browser automation. Requires session cookies.
user_invocable: false
github_url: https://github.com/openclaw/skills/tree/main/skills/arun-8687/linkedin-cli
---

# LinkedIn CLI (lk)

Bird-like CLI for LinkedIn using session cookies. Faster and more reliable than browser automation for basic LinkedIn operations.

## Setup

1. Open LinkedIn in Chrome → DevTools (F12) → Application → Cookies → `www.linkedin.com`
2. Copy `li_at` and `JSESSIONID` values
3. Export to environment:
   ```bash
   export LINKEDIN_LI_AT="your_li_at_value"
   export LINKEDIN_JSESSIONID="your_jsessionid_value"
   ```
4. Add to `~/.zshrc` for persistence (cookies expire periodically — refresh when auth fails)

## Commands

```bash
lk whoami              # Your profile
lk search "AI lead"    # Search people (10 results)
lk profile <public_id> # Detailed profile view
lk messages            # Recent conversations (top 8)
lk feed -n 10          # Timeline posts
lk check               # whoami + messages combo
```

## Integration Notes

- **Cookie expiry:** `li_at` cookies last weeks/months but can expire. If you get auth errors, re-extract from browser.
- **Rate limits:** LinkedIn may throttle or flag automated access. Use sparingly — don't bulk-scrape.
- **Complementary to browser automation:** Use `lk` for reads (messages, profiles, search). Use browser automation for actions (sending messages, applying to jobs).
- **Dependencies:** `pip install linkedin-api`

## When to Use

- Checking LinkedIn messages during `/morning` or `/check-channels`
- Quick profile lookups before interviews or networking
- Searching for people by keywords
- Reading feed without opening browser

## When NOT to Use

- Sending messages (use browser automation — actions need human oversight)
- Applying to jobs (use browser)
- Anything write/action-oriented
