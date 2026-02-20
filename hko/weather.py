#!/usr/bin/env python3
"""HK Observatory weather + morning news — one warm, witty message."""

import json
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
    with open("/tmp/hko_now.json") as f:
        now = json.load(f)
    with open("/tmp/hko_fnd.json") as f:
        fnd = json.load(f)
    with open("/tmp/hko_warn.json") as f:
        warn = json.load(f)

    # Current conditions
    temps = {t["place"]: t["value"] for t in now["temperature"]["data"]}
    temp = temps.get("Shau Kei Wan", temps.get("Hong Kong Observatory"))
    humidity = now.get("humidity", {}).get("data", [{}])[0].get("value", "?")

    # UV index
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

    # Weather summary for LLM
    weather = f"{temp}°C now, {humidity}% humidity, forecast {lo}°–{hi}°C — {forecast_desc}"
    if rain_mm > 0:
        weather += f", {rain_mm}mm rain in past hour"
    if uv_val >= 6:
        weather += f", UV index {uv_val}"
    if warnings:
        weather += ", warnings: " + ", ".join(warnings)

    # News headlines
    headlines = fetch_news()
    news_text = "\n".join(
        f"- {h['title']}: {h['desc']}" for h in headlines
    ) or "No news available today."

    # Output the prompt for claude -p
    print(f"""Write ONLY the message — no preamble, no quotes, no "Here's...", no labels.

Short morning weather note for someone to forward to their wife. Weave today's weather with one news headline — warm, light, a bit funny. ONE short paragraph, no line breaks.

WEATHER: {weather}

HK NEWS:
{news_text}

Format: Start with a weather emoji, then 2-3 sentences that flow naturally — mention the weather facts (temp, conditions) and connect to the lightest/most relatable headline. Name the news briefly so the reader gets it without context. Skip violence or tragedy. 1-2 emojis total. No "Good morning". Plain text only — no markdown, no bold, no asterisks.""")


if __name__ == "__main__":
    main()
