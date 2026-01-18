# /hko - Hong Kong Observatory Temperature

Check current temperature from HK Observatory API, focusing on Shau Kei Wan (Island East).

## Trigger

- User says "hko", "weather", "temperature", or "天氣"
- Morning check-ins

## Workflow

Run this curl command and parse the JSON:
```bash
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
```

Extract from the response:
- `temperature.data` array - find entry where `place` is "Shau Kei Wan"
- `temperature.recordTime` - the timestamp

## Output Format

Quick one-liner only:
```
🌡️ Shau Kei Wan: XX°C (as of HH:MM)
```

## Fallback

If Shau Kei Wan not available, use "Hong Kong Observatory" reading instead.
