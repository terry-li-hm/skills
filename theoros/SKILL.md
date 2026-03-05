---
name: theoros
description: LinkedIn daily feed digest. Run manually or check today's digest. Use when asking about recent LinkedIn activity, job leads, or network updates.
---

# theoros — LinkedIn Feed Digest

Scrapes LinkedIn feed via agent-browser, filters with Claude, writes daily vault note.

## Commands

```bash
theoros run          # full pipeline: scrape → filter → write vault note
theoros fetch        # scrape feed and print raw posts (debug)
theoros fetch -l 5   # limit to 5 posts
theoros --version
```

## Vault Output

Notes written to: `~/notes/LinkedIn/YYYY-MM-DD LinkedIn Digest.md`

Today's digest:
```bash
cat ~/notes/LinkedIn/$(date +%Y-%m-%d)\ LinkedIn\ Digest.md
```

## Schedule

LaunchAgent: `com.terry.theoros` fires at 8am daily.
Log: `~/logs/cron-theoros.log`

## Filter Context

Claude filters for: job leads (DS/AI/AML in HK), industry news (fintech/AML/HKMA), Capco-related posts.

## Gotchas

- agent-browser must be running and LinkedIn session must be active. If session expired, scrape returns login page content (no "Feed post number" markers → 0 posts → empty digest).
- ANTHROPIC_API_KEY must be set in LaunchAgent plist EnvironmentVariables.
- Each agent-browser call is sequential — never parallel.
- Binary: `~/.cargo/bin/theoros`, symlinked to `~/bin/theoros`.
- After `cargo install --path .`, bin updates automatically on reinstall.
