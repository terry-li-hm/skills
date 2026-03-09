---
name: somnus
description: EightSleep sleep data CLI — sync nightly sleep sessions to local DuckDB, show last night's stats, weekly table, and trend averages. Use when checking EightSleep sleep data, sleep scores, HRV, or comparing with Oura.
---

# somnus — EightSleep Sleep Data CLI

## Commands

| Command | Description |
|---------|-------------|
| `somnus auth` | Store credentials + authenticate (run once) |
| `somnus sync` | Sync last 30 nights to DuckDB (default) |
| `somnus sync --days 90` | Sync last 90 nights |
| `somnus today` | Last night's detail (score, HRV, HR, stages) |
| `somnus week` | Last 7 nights as a table |
| `somnus trend --days 30` | 30-day averages |

## Setup

1. `somnus auth` — enter email + password once; stored in macOS Keychain under `somnus`
2. `somnus sync --days 90` — initial backfill
3. Daily sync fires automatically at 08:00 HKT via `com.terry.somnus-sync` LaunchAgent

## File Paths

- **Binary:** `~/bin/somnus`
- **DB:** `~/.local/share/somnus/somnus.duckdb`
- **LaunchAgent:** `~/Library/LaunchAgents/com.terry.somnus-sync.plist`
- **Log:** `~/tmp/somnus-sync.log`
- **Source:** `~/code/somnus/`

## Gotchas

- **Token expiry:** Access tokens expire in ~1h. `somnus sync` on 401 -> run `somnus auth` again.
  Future: add auto-refresh using stored email + password from Keychain.
- **Short intervals filtered:** `sync` skips sessions <1h (naps, accidental readings).
- **Rate limits:** Don't call `sync` more than once per hour — EightSleep rate-limits the intervals endpoint.
- **API is unofficial:** The `client-api.8slp.net` endpoint is reverse-engineered from the mobile app.
  If EightSleep updates their app, credentials or endpoints may change. Reference: `lukas-clarke/pyEight`.
- **LaunchAgent needs HOME:** Keychain access requires `HOME` env var set — plist sets it explicitly.
- **DuckDB bundled:** uses `duckdb` crate with `bundled` feature; first `cargo build` is slow (~2min).
