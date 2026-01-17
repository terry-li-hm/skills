# /hko - Hong Kong Observatory Temperature

Check current temperature from HK Observatory, focusing on Eastern District.

## Trigger

- User says "hko", "weather", "temperature", or "天氣"
- Morning check-ins

## Workflow

1. Use browser automation to navigate to HKO regional temperatures page: `https://www.hko.gov.hk/en/wxinfo/ts/index.htm`
2. Find the temperature for "Eastern District" (東區) or "Tai Koo" (太古)
3. If Eastern District not available, fall back to "Hong Kong Observatory" general reading
4. Return a single-line response in format: `🌡️ Eastern District: XX°C (as of HH:MM)`

## Output Format

Quick one-liner only. Example:
```
🌡️ Eastern District: 24°C (as of 08:45)
```

## Notes

- HKO updates temperatures every few minutes
- Eastern District station may sometimes be listed as "Tai Koo" or nearby area
- If browser automation fails, fall back to the main HKO page temperature
