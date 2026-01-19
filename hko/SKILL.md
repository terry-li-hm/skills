---
name: hko
description: Check current temperature, rain, and weather warnings (typhoon, rainstorm, etc.) from HK Observatory API. Use when user says "hko", "weather", "temperature", "typhoon", or "天氣".
---

# Hong Kong Observatory Weather

Check current temperature, rainfall, forecast, and active weather warnings from HK Observatory API, focusing on Shau Kei Wan (Island East).

## Trigger

Use when:
- User says "hko", "weather", "temperature", "typhoon", "天氣", "颱風"
- Morning check-ins

## Inputs

- **location** (optional): Defaults to "Shau Kei Wan", falls back to "Hong Kong Observatory"

## Workflow

1. **Fetch current conditions, forecast, and warnings**:
   ```bash
   curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en" -o /tmp/hko_now.json && \
   curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en" -o /tmp/hko_fnd.json && \
   curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en" -o /tmp/hko_warn.json && \
   python3 -c "
   import json
   with open('/tmp/hko_now.json') as f: now = json.load(f)
   with open('/tmp/hko_fnd.json') as f: fnd = json.load(f)
   with open('/tmp/hko_warn.json') as f: warn = json.load(f)

   # Current conditions
   temps = {t['place']: t['value'] for t in now['temperature']['data']}
   time = now['temperature']['recordTime'][11:16]
   temp = temps.get('Shau Kei Wan', temps.get('Hong Kong Observatory'))

   # Humidity
   humidity = now.get('humidity', {}).get('data', [{}])[0].get('value', '?')

   # UV index
   uv = now.get('uvindex', {}).get('data', [{}])
   uv_val = uv[0].get('value', '') if uv else ''
   uv_str = f' | UV {uv_val}' if uv_val else ''

   # Today's forecast
   today = fnd['weatherForecast'][0]
   tomorrow = fnd['weatherForecast'][1]
   lo, hi = today['forecastMintemp']['value'], today['forecastMaxtemp']['value']
   forecast_desc = today.get('forecastWeather', '')

   # Tomorrow
   tom_lo, tom_hi = tomorrow['forecastMintemp']['value'], tomorrow['forecastMaxtemp']['value']
   tom_desc = tomorrow.get('forecastWeather', '')
   tom_date = tomorrow.get('week', '')

   # Rainfall - Eastern District or Chai Wan
   rain_str = ''
   if 'rainfall' in now and 'data' in now['rainfall']:
       rain_data = {r['place']: r.get('max', 0) for r in now['rainfall']['data']}
       rain_val = rain_data.get('Eastern District', rain_data.get('Chai Wan', 0))
       if rain_val > 0:
           rain_str = f'🌧️ Rainfall: {rain_val}mm in past hour'

   # Warnings
   warnings = []
   warn_icons = {
       'WTCSGNL': '🌀',  # Typhoon signal
       'WRAIN': '⛈️',    # Rainstorm
       'WHOT': '🥵',     # Very hot
       'WCOLD': '🥶',    # Cold
       'WFROST': '❄️',   # Frost
       'WMSGNL': '💨',   # Strong monsoon
       'WTS': '⚡',      # Thunderstorm
       'WFIRE': '🔥',    # Fire danger
       'WL': '⛰️',       # Landslip
       'WTMW': '🌊',     # Tsunami
   }
   for key, val in warn.items():
       if isinstance(val, dict) and 'name' in val:
           icon = warn_icons.get(key, '⚠️')
           code = val.get('code', '')
           if key == 'WTCSGNL':
               warnings.append(f'{icon} Typhoon Signal {code}')
           else:
               warnings.append(f'{icon} {val[\"name\"]}')

   # Output
   print(f'## Shau Kei Wan Weather (as of {time})')
   print()
   print(f'**Now:** {temp}°C | Humidity {humidity}%{uv_str}')
   print(f'**Today:** {lo}°-{hi}°C — {forecast_desc}')
   print(f'**{tom_date}:** {tom_lo}°-{tom_hi}°C — {tom_desc}')

   if rain_str:
       print()
       print(rain_str)

   if warnings:
       print()
       print('**⚠️ Active Warnings:**')
       for w in warnings:
           print(f'  • {w}')
   "
   ```

2. **Present the weather summary** to user

## Error Handling

- **If API unreachable**: Report error, suggest checking HKO website directly
- **If Shau Kei Wan not available**: Use "Hong Kong Observatory" reading instead

## Output

**Normal day:**
```
## Shau Kei Wan Weather (as of 08:00)

**Now:** 24°C | Humidity 78% | UV 6
**Today:** 23°-28°C — Cloudy with sunny intervals
**Tuesday:** 24°-29°C — Mainly fine
```

**Bad weather day:**
```
## Shau Kei Wan Weather (as of 14:00)

**Now:** 27°C | Humidity 95%
**Today:** 26°-30°C — Squally showers and thunderstorms
**Wednesday:** 25°-28°C — Rain with thunderstorms

🌧️ Rainfall: 15mm in past hour

**⚠️ Active Warnings:**
  • 🌀 Typhoon Signal TC8NE
  • ⛈️ Amber Rainstorm Warning Signal
  • ⚡ Thunderstorm Warning
```

## Warning Types

| Icon | Warning |
|------|---------|
| 🌀 | Typhoon signal (T1, T3, T8, T9, T10) |
| ⛈️ | Rainstorm (Amber/Red/Black) |
| 🥵 | Very Hot Weather |
| 🥶 | Cold Weather |
| ❄️ | Frost |
| 💨 | Strong Monsoon |
| ⚡ | Thunderstorm |
| 🔥 | Fire Danger |
| ⛰️ | Landslip |
| 🌊 | Tsunami |
