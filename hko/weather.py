#!/usr/bin/env python3
"""HK Observatory weather summary — Shau Kei Wan focus, messaging-ready output."""

import json
import random
import sys

def main():
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
    uv_val = 0
    uv_data = now.get('uvindex')
    if isinstance(uv_data, dict):
        uv_list = uv_data.get('data', [])
        if uv_list and isinstance(uv_list[0], dict) and uv_list[0].get('value'):
            uv_val = int(uv_list[0]['value'])

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
        'WTCSGNL': '\U0001f300', 'WRAIN': '\u26c8\ufe0f', 'WHOT': '\U0001f975',
        'WCOLD': '\U0001f976', 'WFROST': '\u2744\ufe0f', 'WMSGNL': '\U0001f4a8',
        'WTS': '\u26a1', 'WFIRE': '\U0001f525', 'WL': '\u26f0\ufe0f', 'WTMW': '\U0001f30a',
    }
    for key, val in warn.items():
        if isinstance(val, dict) and 'name' in val:
            icon = warn_icons.get(key, '\u26a0\ufe0f')
            code = val.get('code', '')
            if key == 'WTCSGNL':
                warnings.append(f'{icon} T{code}')
            else:
                name = val['name'].replace(' Warning Signal', '').replace(' Warning', '')
                warnings.append(f'{icon} {name}')

    # Fun commentary
    def get_vibe(temp, humidity, forecast, warnings, rain_mm):
        if any('\U0001f300' in w for w in warnings):
            return random.choice([
                '\U0001f300 Typhoon vibes — enjoy your legitimate day off!',
                '\U0001f300 Nature says stay home. Who are we to argue?',
                '\U0001f300 Perfect weather for watching the harbor from indoors.',
            ])
        if any('\U0001f975' in w for w in warnings) or temp >= 33:
            return random.choice([
                '\U0001f975 Stepping outside = instant regret.',
                '\U0001f975 The sun woke up and chose violence.',
                "\U0001f975 AC is not a luxury, it's survival.",
            ])
        if any('\U0001f976' in w for w in warnings) or temp <= 12:
            return random.choice([
                '\U0001f976 HK cold hits different. Layer up.',
                '\U0001f976 Time to flex that one winter jacket you own.',
                '\U0001f976 Bubble tea? Make it hot.',
            ])
        if rain_mm > 10 or any('\u26c8\ufe0f' in w for w in warnings):
            return random.choice([
                '\u2614 Umbrella is not optional today.',
                '\U0001f327\ufe0f Perfect excuse to cancel outdoor plans.',
                '\u26c8\ufe0f The MTR will smell... interesting.',
            ])
        if 'rain' in forecast.lower() or 'shower' in forecast.lower():
            return random.choice([
                '\U0001f326\ufe0f Might rain, might not. Classic HK.',
                '\u2602\ufe0f Pack an umbrella, just in case.',
                '\U0001f327\ufe0f Showers possible — dress accordingly.',
            ])
        if humidity >= 90:
            return random.choice([
                '\U0001f4a6 Humidity at "why bother showering" levels.',
                '\U0001f4a6 The air is soup today.',
                '\U0001f32b\ufe0f Glasses will fog. Accept it.',
            ])
        if 'sunny' in forecast.lower() or 'fine' in forecast.lower():
            return random.choice([
                '\u2600\ufe0f Actually nice out. Suspicious.',
                '\U0001f324\ufe0f Solid day to touch grass.',
                '\U0001f60e Good vibes only.',
            ])
        return random.choice([
            '\U0001f937 Weather\'s doing its thing.',
            '\U0001f4ca Acceptable conditions for existence.',
            '\u2728 Could be worse!',
        ])

    vibe = get_vibe(temp, humidity, forecast_desc, warnings, rain_mm)

    # Weather icon
    def get_icon(forecast, warnings, rain_mm):
        if any('\U0001f300' in w for w in warnings): return '\U0001f300'
        if any('\u26c8\ufe0f' in w for w in warnings) or rain_mm > 5: return '\U0001f327\ufe0f'
        if 'thunder' in forecast.lower(): return '\u26c8\ufe0f'
        if 'rain' in forecast.lower() or 'shower' in forecast.lower(): return '\U0001f326\ufe0f'
        if 'cloudy' in forecast.lower(): return '\u2601\ufe0f'
        if 'sunny' in forecast.lower() or 'fine' in forecast.lower(): return '\u2600\ufe0f'
        return '\U0001f324\ufe0f'

    icon = get_icon(forecast_desc, warnings, rain_mm)

    # === OUTPUT ===
    if warnings:
        print('**\u26a0\ufe0f ' + ' \u2022 '.join(warnings) + '**')
        print()

    print(f'**{icon} Shau Kei Wan** ({time})')
    print()

    conditions = f'\u2022 {temp}\u00b0C, {humidity}% humidity'
    if uv_val >= 6:
        conditions += f', UV {uv_val} \U0001f506'
    print(conditions)

    print(f'\u2022 Today: {lo}\u00b0\u2013{hi}\u00b0C \u2014 {forecast_desc}')
    print(f'\u2022 {tom_day}: {tom_lo}\u00b0\u2013{tom_hi}\u00b0C \u2014 {tom_desc}')

    if rain_mm > 0:
        print(f'\u2022 \U0001f327\ufe0f {rain_mm}mm rain in past hour')

    print()
    print(vibe)

if __name__ == '__main__':
    main()
