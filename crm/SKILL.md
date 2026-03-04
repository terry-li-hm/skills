---
name: crm
description: Personal CRM CLI — relationship intelligence from Gmail + Calendar. Use when checking stale contacts, looking up who someone is, or getting pre-meeting context.
user_invocable: true
---

# crm — Personal CRM CLI

Local SQLite CRM built from Gmail + Calendar via `gog`. No cloud.

## Location

`~/code/crm/` — Python 3.13, Typer, uv. DB at `~/.crm/crm.db`.

## Commands

```bash
crm sync [--dry-run]       # Scan 365d Gmail + Calendar + Google Contacts → DB
crm lookup "name"          # FTS search: profile + last 5 interactions
crm stale [--days 30]      # Contacts not reached in N days
crm dossier --today        # Today's calendar attendees with CRM profiles
crm stats                  # Summary + top 10 most active contacts
```

## First Run

```bash
crm sync          # takes a few minutes on first run (365d of email)
crm stats         # verify contacts loaded
```

## Auspex Integration

`crm dossier --today` is called at step 10b of `/auspex`. Outputs plain text (no ANSI) when non-TTY — safe to pipe into briefing narrative.

## Gotchas

- **GOG_KEYRING_PASSWORD** — set automatically from Keychain at import time in sync.py. No manual setup needed.
- **`crm sync` is idempotent** — safe to re-run; deduplicates by email + thread hash.
- **Filtered contacts** (`is_filtered=1`) are excluded from `crm stale` but still in DB. Filter patterns: `noreply@`, `no-reply@`, `notifications@`, `billing@`, `support@`, `donotreply@`, `automated@`, `mailer@`, `bounce@`, or >10 recipients.
- **Timestamps** stored as UTC, displayed as HKT.
- **Re-install after code changes**: `cd ~/code/crm && uv tool install .`

## Weekly Use

- `crm stale` every Friday during `/weekly` — who to ping before the week closes
- `crm dossier --today` fires automatically in `/auspex` when meetings exist

## Rebuild / Reinstall

```bash
cd ~/code/crm
uv lock && uv tool install .
```
