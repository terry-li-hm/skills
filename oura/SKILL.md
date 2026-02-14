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

Token must be available as `OURA_TOKEN`. Source from the .env file:

```bash
export OURA_TOKEN=$(grep OURA_TOKEN ~/oura-data/.env | cut -d= -f2)
```

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

## Workflow

1. For quick checks: run the CLI command, present output to user
2. For "how's my sleep trending" / analysis: sync DuckDB first if stale, then query
3. For morning briefings: `oura scores` is the quick one-liner

## Error Handling

- **If OURA_TOKEN missing**: Source from `~/oura-data/.env`
- **If CLI not built**: `cd ~/code/oura-cli && cargo build --release`
- **If data empty for today**: Ring may not have synced yet; try `yesterday`
- **If DuckDB stale**: Run `cd ~/oura-data && uv run python scripts/sync.py`
