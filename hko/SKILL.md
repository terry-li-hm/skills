---
name: hko
description: HK Observatory weather — temperature, rain, typhoon/rainstorm warnings. "weather", "天氣"
user_invocable: true
---

# Hong Kong Observatory Weather

Check current temperature, rainfall, forecast, and active weather warnings from HK Observatory API, focusing on Shau Kei Wan (Island East).

## Trigger

Use when:
- User says "hko", "weather", "temperature", "typhoon", "天氣", "颱風"
- Morning check-ins

## Workflow

1. **Fetch data and run weather script**:
   ```bash
   curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en" -o /tmp/hko_now.json && \
   curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en" -o /tmp/hko_fnd.json && \
   curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en" -o /tmp/hko_warn.json && \
   python3 /Users/terry/skills/hko/weather.py
   ```

2. **Present the output** to user. Script produces messaging-ready format.

## Output Format

Optimized for Telegram/WhatsApp — uses `•` bullets, bold for emphasis, warnings first. Compact: 5-7 lines on normal days. Includes fun commentary based on conditions.

## Error Handling

- **If API unreachable**: Report error, suggest checking HKO website directly
- **If Shau Kei Wan not available**: Falls back to "Hong Kong Observatory" reading

## Warning Types

🌀 Typhoon (T1-T10) · ⛈️ Rainstorm (Amber/Red/Black) · 🥵 Very Hot · 🥶 Cold · ❄️ Frost · 💨 Strong Monsoon · ⚡ Thunderstorm · 🔥 Fire Danger · ⛰️ Landslip · 🌊 Tsunami
