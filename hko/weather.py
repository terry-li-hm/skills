#!/usr/bin/env python3
"""HK Observatory weather — templated, no LLM."""

import json
import sys


def build_weather_line(now, fnd, warn):
    """Build a templated weather line — no LLM needed."""
    temps = {t["place"]: t["value"] for t in now["temperature"]["data"]}
    temp = temps.get("Shau Kei Wan", temps.get("Hong Kong Observatory"))
    humidity = now.get("humidity", {}).get("data", [{}])[0].get("value", "?")

    # UV
    uv_val = 0
    uv_data = now.get("uvindex")
    if isinstance(uv_data, dict):
        uv_list = uv_data.get("data", [])
        if uv_list and isinstance(uv_list[0], dict) and uv_list[0].get("value"):
            uv_val = int(uv_list[0]["value"])

    # Forecast
    today = fnd["weatherForecast"][0]
    lo, hi = today["forecastMintemp"]["value"], today["forecastMaxtemp"]["value"]
    forecast_desc = today.get("forecastWeather", "")

    # Rainfall
    rain_mm = 0
    if "rainfall" in now and "data" in now["rainfall"]:
        rain_data = {r["place"]: r.get("max", 0) for r in now["rainfall"]["data"]}
        rain_mm = rain_data.get("Eastern District", rain_data.get("Chai Wan", 0))

    # Warnings
    warnings = []
    warn_icons = {
        "WTCSGNL": "\U0001f300", "WRAIN": "\u26c8\ufe0f", "WHOT": "\U0001f975",
        "WCOLD": "\U0001f976", "WFROST": "\u2744\ufe0f", "WMSGNL": "\U0001f4a8",
        "WTS": "\u26a1", "WFIRE": "\U0001f525", "WL": "\u26f0\ufe0f", "WTMW": "\U0001f30a",
    }
    for key, val in warn.items():
        if isinstance(val, dict) and "name" in val:
            icon = warn_icons.get(key, "\u26a0\ufe0f")
            code = val.get("code", "")
            if key == "WTCSGNL":
                warnings.append(f"{icon} T{code}")
            else:
                name = val["name"].replace(" Warning Signal", "").replace(" Warning", "")
                warnings.append(f"{icon} {name}")

    # Pick weather emoji
    fc = forecast_desc.lower()
    if any("\U0001f300" in w for w in warnings):
        emoji = "\U0001f300"
    elif any("\u26c8\ufe0f" in w for w in warnings) or rain_mm > 5:
        emoji = "\U0001f327\ufe0f"
    elif "thunder" in fc:
        emoji = "\u26c8\ufe0f"
    elif "rain" in fc or "shower" in fc:
        emoji = "\U0001f326\ufe0f"
    elif "cloudy" in fc:
        emoji = "\u2601\ufe0f"
    elif "sunny" in fc or "fine" in fc:
        emoji = "\u2600\ufe0f"
    else:
        emoji = "\U0001f324\ufe0f"

    # Build line: ☀️ 19–25°C, sunny and dry, muggy
    desc = forecast_desc.rstrip(".")
    desc = desc[0].lower() + desc[1:] if desc else ""

    parts = [f"{emoji} {lo}\u2013{hi}\u00b0C, {desc}"]
    if rain_mm > 0:
        parts.append(f"{rain_mm}mm rain")
    if uv_val >= 6:
        parts.append(f"UV {uv_val}")
    if humidity != "?" and int(humidity) >= 90:
        parts.append("muggy")

    line = ", ".join(parts)

    if warnings:
        line = "\u26a0\ufe0f " + " \u2022 ".join(warnings) + "\n" + line

    return line


def main():
    with open("/tmp/hko_now.json") as f:
        now = json.load(f)
    with open("/tmp/hko_fnd.json") as f:
        fnd = json.load(f)
    with open("/tmp/hko_warn.json") as f:
        warn = json.load(f)

    print(build_weather_line(now, fnd, warn))


if __name__ == "__main__":
    main()
