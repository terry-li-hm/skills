# /hko - Hong Kong Observatory Temperature

Check current temperature from HK Observatory API, focusing on Shau Kei Wan (Island East).

## Trigger

- User says "hko", "weather", "temperature", or "天氣"
- Morning check-ins

## Workflow

Run this command:
```bash
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en" -o /tmp/hko_now.json && \
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en" -o /tmp/hko_fnd.json && \
python3 -c "
import json
with open('/tmp/hko_now.json') as f: now = json.load(f)
with open('/tmp/hko_fnd.json') as f: fnd = json.load(f)
temps = {t['place']: t['value'] for t in now['temperature']['data']}
time = now['temperature']['recordTime'][11:16]
temp = temps.get('Shau Kei Wan', temps.get('Hong Kong Observatory'))
today = fnd['weatherForecast'][0]
lo, hi = today['forecastMintemp']['value'], today['forecastMaxtemp']['value']
print(f'🌡️ Shau Kei Wan: {temp}°C (Lo {lo}° / Hi {hi}°) as of {time}')
"
```

## Output Format

Quick one-liner:
```
🌡️ Shau Kei Wan: 19°C (Lo 19° / Hi 23°) as of 08:00
```

## Fallback

If Shau Kei Wan not available, use "Hong Kong Observatory" reading instead.
