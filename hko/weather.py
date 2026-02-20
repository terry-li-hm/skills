#!/usr/bin/env python3
"""HK Observatory weather + morning news — warm, witty, wife-forwardable."""

import json
import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request


def fetch_news():
    """Fetch top 3 RTHK local news headlines."""
    url = "http://rthk9.rthk.hk/rthk/news/rss/e_expressnews_elocal.xml"
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
        headlines = []
        for item in root.findall(".//item")[:3]:
            title = item.findtext("title", "").strip()
            desc = item.findtext("description", "").strip()
            sentences = desc.replace("\n", " ").split(". ")
            short_desc = ". ".join(sentences[:2]).strip()
            if short_desc and not short_desc.endswith("."):
                short_desc += "."
            if title:
                headlines.append({"title": title, "desc": short_desc})
        return headlines
    except Exception:
        return []


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    with open("/tmp/hko_now.json") as f:
        now = json.load(f)
    with open("/tmp/hko_fnd.json") as f:
        fnd = json.load(f)
    with open("/tmp/hko_warn.json") as f:
        warn = json.load(f)

    # Current conditions
    temps = {t["place"]: t["value"] for t in now["temperature"]["data"]}
    time = now["temperature"]["recordTime"][11:16]
    temp = temps.get("Shau Kei Wan", temps.get("Hong Kong Observatory"))

    # Humidity
    humidity = now.get("humidity", {}).get("data", [{}])[0].get("value", "?")

    # UV index (only show if >= 6)
    uv_val = 0
    uv_data = now.get("uvindex")
    if isinstance(uv_data, dict):
        uv_list = uv_data.get("data", [])
        if uv_list and isinstance(uv_list[0], dict) and uv_list[0].get("value"):
            uv_val = int(uv_list[0]["value"])

    # Today's forecast
    today = fnd["weatherForecast"][0]
    lo, hi = today["forecastMintemp"]["value"], today["forecastMaxtemp"]["value"]
    forecast_desc = today.get("forecastWeather", "")

    # Rainfall - Eastern District or Chai Wan
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

    # Weather icon
    def get_icon(forecast, warns, rain):
        if any("\U0001f300" in w for w in warns): return "\U0001f300"
        if any("\u26c8\ufe0f" in w for w in warns) or rain > 5: return "\U0001f327\ufe0f"
        if "thunder" in forecast.lower(): return "\u26c8\ufe0f"
        if "rain" in forecast.lower() or "shower" in forecast.lower(): return "\U0001f326\ufe0f"
        if "cloudy" in forecast.lower(): return "\u2601\ufe0f"
        if "sunny" in forecast.lower() or "fine" in forecast.lower(): return "\u2600\ufe0f"
        return "\U0001f324\ufe0f"

    icon = get_icon(forecast_desc, warnings, rain_mm)

    # Build weather summary string
    weather_summary = f"{temp}°C now, {humidity}% humidity, forecast {lo}°–{hi}°C — {forecast_desc}"
    if rain_mm > 0:
        weather_summary += f", {rain_mm}mm rain in past hour"
    if warnings:
        weather_summary += ", warnings: " + ", ".join(warnings)

    if mode == "prompt":
        # Output just the LLM prompt (for claude -p)
        headlines = fetch_news()
        news_text = "\n".join(
            f"- {h['title']}: {h['desc']}" for h in headlines
        ) or "No news available today."

        print(f"""Write ONLY the message text — no preamble, no quotes, no "Here's...".

You're writing a short morning note for someone's wife in Hong Kong. Weave today's weather together with one news headline — warm, light, a little funny.

WEATHER: {weather_summary}

NEWS:
{news_text}

Rules:
- Pick the lightest/most relatable headline. SKIP violence or tragedy.
- Briefly name what the news is about so the reader gets it without having seen the headline.
- 2-3 short sentences. Warm, playful. 1-2 emojis max.
- Don't start with "Good morning" (already in header).
- English, Cantonese slang OK if natural.
- Output ONLY the message. No labels, no preamble, no quotes.""")
        return

    # mode == "full" — output the formatted weather block
    if warnings:
        print("**\u26a0\ufe0f " + " \u2022 ".join(warnings) + "**")
        print()

    print(f"{icon} **Good morning!**")
    # Lowercase first char only, preserve rest (e.g. "Sunny periods. Dry..." stays readable)
    desc = forecast_desc[0].lower() + forecast_desc[1:] if forecast_desc else ""
    line = f"{temp}\u00b0C now, {desc}"
    if lo != hi:
        line += f" ({lo}\u00b0\u2013{hi}\u00b0C)"
    if uv_val >= 6:
        line += f" \u2022 UV {uv_val} \U0001f506"
    if rain_mm > 0:
        line += f" \u2022 \U0001f327\ufe0f {rain_mm}mm rain"
    print(line)


if __name__ == "__main__":
    main()
