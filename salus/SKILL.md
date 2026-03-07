---
name: salus
description: Manulife health insurance claims checker CLI. Use when checking claim status, reimbursement amounts, or claim history. Commands: salus claims, salus claims --all.
---

# salus — Manulife Claims Checker

Binary: `~/bin/salus` (symlink to `~/code/target/debug/salus`)
Source: `~/code/salus/`

## Commands

```bash
salus claims        # Show last 10 claims (page 1)
salus claims --all  # Paginate through all 24+ claims
```

## How it works

Shells out to `agent-browser` to automate Manulife website. Uses persistent profile (`AGENT_BROWSER_PROFILE`) so session cookies carry over — login only needed when session expires.

Password fetched from 1Password: `op item get "Manulife" --vault Personal --fields password`

## Known Gotchas

**Login selectors may need updating.** The Manulife login page has a radio button + email field flow that may not respond to `input[type='email']` CSS selectors. If login fails, the flow may need `agent-browser eval` with coordinate-based clicks (see session notes from Mar 7 2026 — used `eval` to click at coordinates 157,521 to select email radio, then filled email field).

**Session persistence.** If already logged in (URL contains "portal"), login is skipped. Run `porta inject --browser chrome --domain manulife.com.hk` first if the session is stale.

**OTP not handled.** If Manulife requires OTP at login, salus will fail with "Login failed". Use `iris verify --from manulife` in a second terminal to relay the OTP link.

**Pagination.** The `--all` flag uses `href*='page=N'` link detection — may break if Manulife changes pagination markup.

**Claims URL.** Direct navigation to `/eservice/claimRecords.action` after login — may redirect to portal home if session expired mid-run.

## Output

Fixed-width table, ANSI-bold on PAID column:
```
DATE         CLAIM#        MEMBER              BENEFIT                        CCY   CLAIMED    PAID    STATUS
24 Feb 2026  260532053A    LI HO MING TERRY    Routine Physical Examination   HKD   3,638.00   840.00  Processed
```

## Benefit Cap Gotcha

Body checks submitted as "Others" in SimpleClaim are classified as **Routine Physical Examination** — sub-benefit with its own annual cap (~$840), separate from Plan C's general limit. See `~/docs/solutions/operational/manulife-simpleclaim-gotchas.md`.
