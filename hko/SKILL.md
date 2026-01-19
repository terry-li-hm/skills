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

   temps = {t['place']: t['value'] for t in now['temperature']['data']}
   time = now['temperature']['recordTime'][11:16]
   temp = temps.get('Shau Kei Wan', temps.get('Hong Kong Observatory'))
   today = fnd['weatherForecast'][0]
   lo, hi = today['forecastMintemp']['value'], today['forecastMaxtemp']['value']

   # Check rainfall - look for Eastern District or Chai Wan
   rain = ''
   if 'rainfall' in now and 'data' in now['rainfall']:
       rain_data = {r['place']: r.get('max', 0) for r in now['rainfall']['data']}
       rain_val = rain_data.get('Eastern District', rain_data.get('Chai Wan', 0))
       if rain_val > 0:
           rain = f' 🌧️ {rain_val}mm'

   # Check warnings
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
           # For typhoon, show signal number
           if key == 'WTCSGNL':
               warnings.append(f'{icon} T{code[-1] if code else \"?\"}')
           else:
               warnings.append(f'{icon} {val[\"name\"]}')

   warn_str = ' | ' + ', '.join(warnings) if warnings else ''
   print(f'🌡️ Shau Kei Wan: {temp}°C (Lo {lo}° / Hi {hi}°){rain}{warn_str} as of {time}')
   "
   ```

2. **Present quick one-liner** to user

## Error Handling

- **If API unreachable**: Report error, suggest checking HKO website directly
- **If Shau Kei Wan not available**: Use "Hong Kong Observatory" reading instead

## Output

Quick one-liner (rain/warnings shown only if active):
```
🌡️ Shau Kei Wan: 19°C (Lo 19° / Hi 23°) as of 08:00
🌡️ Shau Kei Wan: 28°C (Lo 27° / Hi 32°) 🌧️ 5mm | 🌀 T8, ⛈️ Amber Rainstorm as of 14:00
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
