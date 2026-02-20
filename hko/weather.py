#!/usr/bin/env python3
"""HK Observatory weather + RTHK Chinese news — one paragraph."""

import json
import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request


def fetch_news():
    """Fetch top 5 RTHK Chinese local news headlines with links."""
    url = "http://rthk9.rthk.hk/rthk/news/rss/c_expressnews_clocal.xml"
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
        headlines = []
        for item in root.findall(".//item")[:5]:
            title = item.findtext("title", "").strip()
            desc = item.findtext("description", "").strip()
            link = item.findtext("link", "").strip()
            # First 2 sentences for context
            sentences = desc.replace("\n", " ")
            # Chinese uses 。 as sentence separator
            parts = sentences.split("。")
            short_desc = "。".join(parts[:2]).strip()
            if short_desc and not short_desc.endswith("。"):
                short_desc += "。"
            if title:
                headlines.append({"title": title, "desc": short_desc, "link": link})
        return headlines
    except Exception:
        return []


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

    # Build line: ☀️ 19–25°C, sunny and dry
    desc = forecast_desc.rstrip(".")
    desc = desc[0].lower() + desc[1:] if desc else ""
    line = f"{emoji} {lo}\u2013{hi}\u00b0C, {desc}."

    if rain_mm > 0:
        line += f", {rain_mm}mm rain"
    if uv_val >= 6:
        line += f", UV {uv_val}"
    if humidity != "?" and int(humidity) >= 90:
        line += ", muggy"

    if warnings:
        line = "\u26a0\ufe0f " + " \u2022 ".join(warnings) + "\n" + line

    return line


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "weather"

    with open("/tmp/hko_now.json") as f:
        now = json.load(f)
    with open("/tmp/hko_fnd.json") as f:
        fnd = json.load(f)
    with open("/tmp/hko_warn.json") as f:
        warn = json.load(f)

    if mode == "weather":
        print(build_weather_line(now, fnd, warn))

    elif mode == "prompt":
        weather_line = build_weather_line(now, fnd, warn)
        headlines = fetch_news()
        news_text = "\n".join(
            f"- [{i}] {h['title']}: {h['desc']}" for i, h in enumerate(headlines)
        ) or "No news available today."

        print(f"""Output ONLY your sentence + index. Nothing else. Do NOT repeat the weather line.

The weather today: "{weather_line}"

Write ONE short, funny sentence connecting the weather to the lightest headline below. Think punchline, not paragraph.

NEWS:
{news_text}

Rules:
- MAX 15 words. Punchy. Make someone smile.
- Skip violence/tragedy. English only. No emoji.
- Name the news topic so the reader gets it.
- If all headlines are heavy, just a short weather quip instead.
- LAST LINE: the index number of headline used (e.g. "3").""")

    elif mode == "links":
        headlines = fetch_news()
        print(json.dumps([h["link"] for h in headlines]))


if __name__ == "__main__":
    main()
