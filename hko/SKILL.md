---
name: hko
description: HK Observatory weather — temperature, rain, typhoon/rainstorm warnings. "weather", "天氣"
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
   import random
   with open('/tmp/hko_now.json') as f: now = json.load(f)
   with open('/tmp/hko_fnd.json') as f: fnd = json.load(f)
   with open('/tmp/hko_warn.json') as f: warn = json.load(f)

   # Current conditions
   temps = {t['place']: t['value'] for t in now['temperature']['data']}
   time = now['temperature']['recordTime'][11:16]
   temp = temps.get('Shau Kei Wan', temps.get('Hong Kong Observatory'))

   # Humidity
   humidity = now.get('humidity', {}).get('data', [{}])[0].get('value', '?')

   # UV index (only show if >= 6)
   uv = now.get('uvindex', {}).get('data', [{}])
   uv_val = int(uv[0].get('value', 0)) if uv and uv[0].get('value') else 0

   # Today's forecast
   today = fnd['weatherForecast'][0]
   tomorrow = fnd['weatherForecast'][1]
   lo, hi = today['forecastMintemp']['value'], today['forecastMaxtemp']['value']
   forecast_desc = today.get('forecastWeather', '')

   # Tomorrow
   tom_lo, tom_hi = tomorrow['forecastMintemp']['value'], tomorrow['forecastMaxtemp']['value']
   tom_desc = tomorrow.get('forecastWeather', '')
   tom_day = tomorrow.get('week', 'Tomorrow')

   # Rainfall - Eastern District or Chai Wan
   rain_mm = 0
   if 'rainfall' in now and 'data' in now['rainfall']:
       rain_data = {r['place']: r.get('max', 0) for r in now['rainfall']['data']}
       rain_mm = rain_data.get('Eastern District', rain_data.get('Chai Wan', 0))

   # Warnings
   warnings = []
   warn_icons = {
       'WTCSGNL': '🌀', 'WRAIN': '⛈️', 'WHOT': '🥵', 'WCOLD': '🥶',
       'WFROST': '❄️', 'WMSGNL': '💨', 'WTS': '⚡', 'WFIRE': '🔥',
       'WL': '⛰️', 'WTMW': '🌊',
   }
   for key, val in warn.items():
       if isinstance(val, dict) and 'name' in val:
           icon = warn_icons.get(key, '⚠️')
           code = val.get('code', '')
           if key == 'WTCSGNL':
               warnings.append(f'{icon} T{code}')
           else:
               # Shorten common warning names
               name = val['name'].replace(' Warning Signal', '').replace(' Warning', '')
               warnings.append(f'{icon} {name}')

   # Fun commentary based on conditions
   def get_vibe(temp, humidity, forecast, warnings, rain_mm):
       if any('🌀' in w for w in warnings):
           return random.choice([
               '🌀 Typhoon vibes — enjoy your legitimate day off!',
               '🌀 Nature says stay home. Who are we to argue?',
               '🌀 Perfect weather for watching the harbor from indoors.',
           ])
       if any('🥵' in w for w in warnings) or temp >= 33:
           return random.choice([
               '🥵 Stepping outside = instant regret.',
               '🥵 The sun woke up and chose violence.',
               '🥵 AC is not a luxury, it\\'s survival.',
           ])
       if any('🥶' in w for w in warnings) or temp <= 12:
           return random.choice([
               '🥶 HK cold hits different. Layer up.',
               '🥶 Time to flex that one winter jacket you own.',
               '🥶 Bubble tea? Make it hot.',
           ])
       if rain_mm > 10 or any('⛈️' in w for w in warnings):
           return random.choice([
               '☔ Umbrella is not optional today.',
               '🌧️ Perfect excuse to cancel outdoor plans.',
               '⛈️ The MTR will smell... interesting.',
           ])
       if 'rain' in forecast.lower() or 'shower' in forecast.lower():
           return random.choice([
               '🌦️ Might rain, might not. Classic HK.',
               '☂️ Pack an umbrella, just in case.',
               '🌧️ Showers possible — dress accordingly.',
           ])
       if humidity >= 90:
           return random.choice([
               '💦 Humidity at \"why bother showering\" levels.',
               '💦 The air is soup today.',
               '🌫️ Glasses will fog. Accept it.',
           ])
       if 'sunny' in forecast.lower() or 'fine' in forecast.lower():
           return random.choice([
               '☀️ Actually nice out. Suspicious.',
               '🌤️ Solid day to touch grass.',
               '😎 Good vibes only.',
           ])
       return random.choice([
           '🤷 Weather\\'s doing its thing.',
           '📊 Acceptable conditions for existence.',
           '✨ Could be worse!',
       ])

   vibe = get_vibe(temp, humidity, forecast_desc, warnings, rain_mm)

   # Weather icon based on conditions
   def get_icon(forecast, warnings, rain_mm):
       if any('🌀' in w for w in warnings): return '🌀'
       if any('⛈️' in w for w in warnings) or rain_mm > 5: return '🌧️'
       if 'thunder' in forecast.lower(): return '⛈️'
       if 'rain' in forecast.lower() or 'shower' in forecast.lower(): return '🌦️'
       if 'cloudy' in forecast.lower(): return '☁️'
       if 'sunny' in forecast.lower() or 'fine' in forecast.lower(): return '☀️'
       return '🌤️'

   icon = get_icon(forecast_desc, warnings, rain_mm)

   # === OUTPUT (Telegram-friendly) ===
   
   # Warnings first if any (most important!)
   if warnings:
       print('**⚠️ ' + ' • '.join(warnings) + '**')
       print()

   # Header with location and time
   print(f'**{icon} Shau Kei Wan** ({time})')
   print()

   # Current conditions
   conditions = f'• {temp}°C, {humidity}% humidity'
   if uv_val >= 6:
       conditions += f', UV {uv_val} 🔆'
   print(conditions)

   # Today
   print(f'• Today: {lo}°–{hi}°C — {forecast_desc}')

   # Tomorrow
   print(f'• {tom_day}: {tom_lo}°–{tom_hi}°C — {tom_desc}')

   # Rainfall if significant
   if rain_mm > 0:
       print(f'• 🌧️ {rain_mm}mm rain in past hour')

   # Fun commentary
   print()
   print(vibe)
   "
   ```

2. **Present the weather summary** to user. The script outputs messaging-ready format.

## Formatting Notes

Output is optimized for Telegram/WhatsApp:
- Uses `•` bullets, not dashes or pipes
- Bold (`**text**`) for emphasis, no markdown headers
- Warnings appear FIRST if present (most actionable)
- UV only shown if ≥6 (when it matters)
- Fun commentary adapts to conditions
- Compact: 5-7 lines on normal days

## Error Handling

- **If API unreachable**: Report error, suggest checking HKO website directly
- **If Shau Kei Wan not available**: Use "Hong Kong Observatory" reading instead

## Example Output

**Normal day:**
```
**☀️ Shau Kei Wan** (08:00)

• 24°C, 78% humidity
• Today: 23°–28°C — Cloudy with sunny intervals
• Friday: 24°–29°C — Mainly fine

☀️ Actually nice out. Suspicious.
```

**Spicy day:**
```
**⚠️ 🌀 T8 • ⛈️ Amber Rainstorm**

**🌧️ Shau Kei Wan** (14:00)

• 27°C, 95% humidity
• Today: 26°–30°C — Squally showers and thunderstorms
• Saturday: 25°–28°C — Rain with thunderstorms
• 🌧️ 15mm rain in past hour

🌀 Typhoon vibes — enjoy your legitimate day off!
```

## Warning Types

- 🌀 Typhoon signal (T1, T3, T8, T9, T10)
- ⛈️ Rainstorm (Amber/Red/Black)
- 🥵 Very Hot Weather
- 🥶 Cold Weather
- ❄️ Frost
- 💨 Strong Monsoon
- ⚡ Thunderstorm
- 🔥 Fire Danger
- ⛰️ Landslip
- 🌊 Tsunami
