---
name: nyx
description: >-
  Sleep health analysis CLI using Oura DuckDB data. Use for weekly sleep
  summary, 30-day trends, before/after event comparisons, and monthly reports.
  Triggers: "nyx", "sleep summary", "sleep trend", "sleep analysis", "how's
  my sleep", "sleep report". NOT for raw Oura API data (use oura skill).
user_invocable: true
---

# Nyx — Sleep Health Analysis

Named for the Greek goddess of Night, mother of Hypnos.
Data source: `~/oura-data/data/oura.duckdb` (populated by oura-data sync).

## Commands

```bash
nyx                          # This week vs 4-week avg (readiness, sleep, HRV, bedtime)
nyx trend                    # 30-day ASCII chart — readiness + bedtime drift
nyx event YYYY-MM-DD label   # 7-day before vs after comparison
nyx monthly [YYYY-MM]        # Monthly report → ~/notes/Sleep/YYYY-MM-nyx.md
```

## Automation

Monthly LaunchAgent (`com.terry.nyx-monthly`) fires on the 1st of each month at 9am.
Reports saved to `~/notes/Sleep/YYYY-MM-nyx.md`.

## Key findings (as of 2026-03-08)

From 60-day historical analysis:
- **Bedtime before 22:30 → readiness avg 82.6** vs after 23:30 → 76.3 (+6 pts)
- **30-day trend:** readiness +6.4 pts, bedtime 38 min earlier
- Wake time has no meaningful signal (80.6 vs 80.7 before/after 7am)
- Bedtime is the lever; wake time is not

## Implementation notes

- `bedtime_start` stored as **local HKT** in DuckDB (no UTC offset, `HKT_OFFSET_HOURS = 0`)
- Rust binary — Cargo source at `~/code/nyx/`, binary installed to `~/bin/nyx`
- Links against **system libduckdb** (`brew install duckdb`) — NOT the bundled crate (avoids 10min C++ compile)
- `.cargo/config.toml` sets `DUCKDB_LIB_DIR`/`DUCKDB_INCLUDE_DIR` — `cargo build --release` just works
- `duckdb` crate feature `chrono` enables `NaiveDate`/`NaiveDateTime` as `FromSql`/`ToSql` directly
- Build time: ~4s cold, ~0.7s incremental
- Repo: `github.com/terry-li-hm/nyx` (private)
