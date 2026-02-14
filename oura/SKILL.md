---
name: oura
description: Oura Ring health data — sleep, readiness, activity, HRV, stress. "oura", "how did I sleep", "health scores"
user_invocable: true
---

# Oura Ring Health Data

Quick access to Oura health metrics via the `oura` CLI (`~/code/oura-cli`), plus DuckDB for historical analysis.

## Trigger

Use when:
- User says "oura", "sleep score", "how did I sleep", "readiness", "hrv", "health scores"
- Morning briefings that include health data
- Any question about sleep quality, activity, or stress

## Quick Access (CLI)

`OURA_TOKEN` is set in `~/.zshenv` — always available, no need to export.

### Commands

```bash
oura                          # today's scores (sleep + readiness + activity)
oura scores [DATE]            # same, with optional date
oura sleep [DATE]             # detailed sleep breakdown
oura readiness [DATE]         # readiness score + contributors
oura activity [DATE]          # steps, calories, movement
oura hrv [DATE]               # HRV, HR, breath rate from sleep
oura stress [DATE]            # daily stress summary
oura json <ENDPOINT> [DATE]   # raw JSON for any API endpoint
```

`DATE` accepts `YYYY-MM-DD`, `today`, or `yesterday`. Defaults to today.

### Binary Location

- Debug: `~/code/oura-cli/target/debug/oura`
- Release: `~/code/oura-cli/target/release/oura`
- After `cargo install --path ~/code/oura-cli`: available as `oura` on PATH

## Historical Analysis (DuckDB)

For trends, correlations, and multi-day queries, use the synced DuckDB database:

```bash
cd ~/oura-data && uv run python scripts/sync.py          # sync last 7 days
cd ~/oura-data && uv run python scripts/sync.py --backfill 30  # backfill 30 days
```

```python
import duckdb
con = duckdb.connect('/Users/terry/oura-data/data/oura.duckdb', read_only=True)
# Example: weekly HRV trend
con.execute("""
    SELECT day, average_hrv, efficiency
    FROM sleep WHERE day >= CURRENT_DATE - 7
    ORDER BY day
""").fetchall()
```

Key tables: `sleep`, `readiness`, `daily_activity`, `daily_stress`, `daily_sleep`, `workout`, `daily_spo2`. See `~/oura-data/scripts/sync.py` for full schema.

## Interpretation

**Readiness > Sleep.** Readiness is the headline metric — composite of sleep, HRV, temperature, activity balance, recovery. Sleep score only measures one night. When presenting data, lead with readiness. The default `oura` (no args) now shows scores + readiness contributors.

## Workflow

1. For quick checks: `oura` (shows scores + readiness contributors)
2. For "how's my sleep trending" / analysis: sync DuckDB first if stale, then query
3. For morning briefings: `oura` is the one-liner (richer than `oura scores`)

## Error Handling

- **If OURA_TOKEN missing**: Should be in `~/.zshenv`. Fallback: `export OURA_TOKEN=$(grep OURA_TOKEN ~/oura-data/.env | cut -d= -f2)`
- **If CLI not built**: `cd ~/code/oura-cli && cargo build --release && cargo install --path .`
- **If detailed breakdown missing**: Normal early morning — `sleep` periods sync later than `daily_sleep` scores. CLI now shows score + contributors as fallback
- **If DuckDB stale**: Run `cd ~/oura-data && uv run python scripts/sync.py`
