---
name: oura-sync
description: Sync Oura Ring data to local DuckDB and backup CSV to GitHub. Use when user says "sync oura", "backup oura data", "oura stats", or wants to query their sleep/readiness/resilience data.
---

# Oura Data Sync

Sync sleep, readiness, and resilience data from Oura Ring API to local DuckDB, with CSV backup to private GitHub repo.

## Repository

- **Repo:** `~/oura-data` (https://github.com/terry-li-hm/oura-data)
- **Database:** `~/oura-data/data/oura.duckdb` (local only)
- **Backup:** `~/oura-data/exports/*.csv` (tracked in git)
- **Token:** `~/oura-data/.env`
- **Analysis:** `[[Oura Data Analysis]]` in vault

## Commands

### Sync Data

```bash
cd ~/oura-data

# Sync last 7 days (default)
uv run python scripts/sync.py

# Backfill N days
uv run python scripts/sync.py --backfill 30

# Full historical sync
uv run python scripts/sync.py --backfill 1825
```

### Export & Backup to GitHub

```bash
cd ~/oura-data
uv run python scripts/sync.py --export
git add exports/
git commit -m "Backup oura data $(date +%Y-%m-%d)"
git push
```

### Query Data

```bash
cd ~/oura-data
uv run python -c "
import duckdb
con = duckdb.connect('data/oura.duckdb')
for row in con.execute('SELECT day, efficiency, average_hrv FROM sleep ORDER BY day DESC LIMIT 7').fetchall():
    print(row)
"
```

## Full Workflow (Periodic)

Run this monthly to ensure complete backup:

1. **Sync all data:** `uv run python scripts/sync.py --backfill 1825`
2. **Export CSV:** `uv run python scripts/sync.py --export`
3. **Backup to GitHub:** `git add exports/ && git commit -m "Backup" && git push`
4. **Update analysis:** Run queries and update `[[Oura Data Analysis]]` in vault

## Storage Strategy

| Location | Contents | Purpose |
|----------|----------|---------|
| `data/oura.duckdb` | Full database | Fast local queries |
| `exports/*.csv` | All tables | Git backup (human-readable, diffable) |

**Why CSV backup?**
- Human-readable, portable
- Git can diff changes
- Protection if Oura API disappears
- Can regenerate DuckDB from CSV if needed

## Available Tables

| Table | Key Fields |
|-------|-----------|
| `sleep` | day, efficiency, average_hrv, average_heart_rate, deep/light/rem_sleep_duration |
| `readiness` | day, score, temperature_deviation, contributors |
| `resilience` | day, level, contributors |

## Analysis Queries

When user asks for analysis, run these and save to `[[Oura Data Analysis]]`:

```sql
-- Yearly trends
SELECT EXTRACT(year FROM day) as year,
    ROUND(AVG(average_hrv), 1) as avg_hrv,
    ROUND(AVG(efficiency), 1) as efficiency
FROM sleep WHERE efficiency > 10 GROUP BY year ORDER BY year;

-- HRV vs efficiency correlation
SELECT CASE
    WHEN average_hrv < 50 THEN 'HRV <50'
    WHEN average_hrv < 70 THEN 'HRV 50-70'
    WHEN average_hrv < 90 THEN 'HRV 70-90'
    ELSE 'HRV 90+'
END as hrv_bucket,
ROUND(AVG(efficiency), 1) as avg_efficiency
FROM sleep WHERE efficiency > 10 AND average_hrv > 0
GROUP BY hrv_bucket;

-- Optimal bedtime
SELECT EXTRACT(hour FROM bedtime_start) as bed_hour,
    ROUND(AVG(efficiency), 1) as efficiency
FROM sleep WHERE efficiency > 10
GROUP BY bed_hour HAVING COUNT(*) >= 20
ORDER BY bed_hour;

-- Day of week pattern
SELECT CASE EXTRACT(dow FROM day)
    WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue'
    WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri'
    WHEN 6 THEN 'Sat' END as weekday,
ROUND(AVG(efficiency), 1) as efficiency
FROM sleep WHERE efficiency > 10
GROUP BY EXTRACT(dow FROM day) ORDER BY EXTRACT(dow FROM day);
```

## Workflow Summary

| User Says | Action |
|-----------|--------|
| "sync oura" | Run sync with default 7 days |
| "sync all oura data" | Run `--backfill 1825` |
| "backup oura" | Export + git commit + push |
| "oura stats" / "how's my sleep" | Query DuckDB, show recent data |
| "analyze oura data" | Run full analysis, save to vault |
