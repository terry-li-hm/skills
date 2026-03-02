---
name: caelum
description: HK Observatory one-line weather summary CLI. Fetches live HKO data, formats as emoji + temp range + conditions.
user_invocable: false
---

# caelum

Rust CLI that fetches HK Observatory weather and prints a single formatted line.

## Usage

```bash
caelum
# ⛈️ 16–23°C, cloudy with occasional showers. A few thunderstorms later, muggy
```

No arguments, no subcommands. Output goes to stdout; errors to stderr (exit 1).

## What it fetches

Three HKO opendata endpoints (always fresh — no /tmp caching):
- `rhrread` — current temperature, humidity, rainfall, UV
- `fnd` — 9-day forecast (temperature range + description)
- `warnsum` — active warning signals

## Output format

```
[⚠️ Warning1 • Warning2]
{emoji} {lo}–{hi}°C, {forecast_desc}[, {rain}mm rain][, UV N][, muggy]
```

Emoji priority: 🌀 typhoon → 🌧️ rain warning/heavy rain → ⛈️ thunder → 🌦️ shower → ☁️ cloudy → ☀️ sunny/fine → 🌤️ default

- Temperature station: Shau Kei Wan (fallback: Hong Kong Observatory)
- Forecast: matches today by `forecastDate` (YYYYMMDD), falls back to [0]
- Rainfall: Eastern District (fallback: Chai Wan), `max` field
- Muggy: humidity ≥ 90%
- UV suffix: only if UV index ≥ 6

## Where it's used

- `/auspex` morning brief — replaces the old `curl × 3 + python3 weather.py` chain
- `/hko` skill — single command now

## Gotchas

- The old `weather.py` read from `/tmp/hko_*.json` pre-cached files — stale data caused wrong temps. `caelum` always fetches fresh.
- `forecastDate` is an integer in the JSON (e.g., `20260303`) — matched as string after `.to_string()`.
- Unused variable `_temp` in source: current station temp is fetched but not shown in output (only forecast lo/hi are shown). This matches the Python original.

## Repo

`~/code/caelum/` · crates.io: `caelum`
