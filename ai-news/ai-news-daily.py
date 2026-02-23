#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "feedparser",
#     "requests",
#     "trafilatura",
#     "pyyaml",
#     "beautifulsoup4",
# ]
# ///
"""Daily AI news fetcher — runs via cron, zero LLM tokens.

Fetches Tier 1 sources (RSS preferred, web scraping fallback),
dedupes by date + title prefix, appends delta to AI News Log,
sends summary to Telegram.

Also archives full article text for Tier 1 sources (via trafilatura)
to ~/.cache/ai-news-articles/ for downstream thematic digest synthesis.

Dedup strategy:
  1. Date-based: Only keep articles published after the last scan date
  2. Title-prefix: For undated web scrapes, check if title prefix already in log
  3. Junk filter: Drop short/generic titles (nav items, categories)

Cron: 30 18 * * * (6:30 PM HKT daily)
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests
import trafilatura
import yaml
from bs4 import BeautifulSoup

# Paths
SOURCES_YAML = Path.home() / "skills" / "ai-news" / "sources.yaml"
NEWS_LOG = Path.home() / "notes" / "AI News Log.md"
STATE_FILE = Path.home() / ".cache" / "ai-news-state.json"
ARTICLE_CACHE_DIR = Path.home() / ".cache" / "ai-news-articles"

HKT = timezone(timedelta(hours=8))
NOW = datetime.now(HKT)
TODAY = NOW.strftime("%Y-%m-%d")

CADENCE_DAYS = {
    "daily": 0,
    "twice_weekly": 2,
    "weekly": 5,
    "biweekly": 10,
    "monthly": 25,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AI-News-Bot/1.0"
}
TIMEOUT = 15


# --- State management ---

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_last_scan_date(state: dict) -> str:
    """Get the most recent scan date across all sources, or 1 day ago."""
    dates = []
    for v in state.values():
        try:
            dates.append(datetime.fromisoformat(v))
        except (ValueError, TypeError):
            pass
    if dates:
        latest = max(dates)
        return latest.strftime("%Y-%m-%d")
    return (NOW - timedelta(days=1)).strftime("%Y-%m-%d")


# --- Dedup ---

def load_title_prefixes() -> set[str]:
    """Extract normalised title prefixes from the log for dedup."""
    if not NEWS_LOG.exists():
        return set()
    content = NEWS_LOG.read_text()
    prefixes = set()
    # Match **"Title"**, **Title**, **[Title](url)** patterns
    for match in re.finditer(
        r'\*\*["\u201c]?(?:\[)?(.+?)(?:\]\([^)]*\))?["\u201d]?\*\*', content
    ):
        title = match.group(1).strip()
        prefix = _title_prefix(title)
        if prefix:
            prefixes.add(prefix)
    # Also match "Quoted titles" in narrative-style manual entries
    for match in re.finditer(r'["\u201c]([^"\u201d]{15,})["\u201d]', content):
        prefix = _title_prefix(match.group(1).strip())
        if prefix:
            prefixes.add(prefix)
    return prefixes


def _title_prefix(title: str) -> str:
    """First 6 significant words, normalised. Robust to subtitle variations."""
    words = re.sub(r'[^\w\s]', '', title.lower()).split()
    sig = [w for w in words if len(w) > 2][:6]
    return " ".join(sig)


def is_junk(title: str) -> bool:
    """Filter out short, generic, or navigation titles."""
    norm = re.sub(r'[^\w\s]', '', title.lower()).strip()
    if len(norm) < 15:
        return True
    junk = {
        "current accounts", "crypto investigations", "crypto compliance",
        "crypto security fraud", "cumulative repo count over time",
        "cumulative star count over time", "subscribe", "sign up",
        "read more", "learn more", "load more", "all posts",
        "latest posts", "featured", "trending", "popular",
    }
    return norm in junk or norm.startswith("量子位编辑")


def should_fetch(name: str, cadence: str, state: dict) -> bool:
    min_days = CADENCE_DAYS.get(cadence, 0)
    if min_days == 0:
        return True
    last = state.get(name)
    if not last:
        return True
    try:
        return (NOW - datetime.fromisoformat(last)).days >= min_days
    except (ValueError, TypeError):
        return True


# --- Fetchers ---

def fetch_rss(url: str, since_date: str, max_items: int = 5) -> list[dict]:
    """Fetch articles from RSS, filtering to only those after since_date."""
    try:
        feed = feedparser.parse(url, request_headers=HEADERS)
        articles = []
        for entry in feed.entries[:max_items * 2]:  # fetch extra, filter by date
            title = entry.get("title", "").strip()
            if not title:
                continue
            date_str = _parse_feed_date(entry)
            # Date-based filter: skip articles from before last scan
            if date_str and date_str <= since_date:
                continue
            summary = _extract_summary(entry)
            link = entry.get("link", "")
            articles.append({"title": title, "date": date_str, "summary": summary, "link": link})
            if len(articles) >= max_items:
                break
        return articles
    except Exception as e:
        print(f"  RSS error {url}: {e}", file=sys.stderr)
        return []


def _parse_feed_date(entry) -> str:
    for field in ("published_parsed", "updated_parsed", "created_parsed"):
        parsed = getattr(entry, field, None)
        if parsed:
            return f"{parsed.tm_year}-{parsed.tm_mon:02d}-{parsed.tm_mday:02d}"
    return ""


def _extract_summary(entry) -> str:
    if not hasattr(entry, "summary"):
        return ""
    soup = BeautifulSoup(entry.summary, "html.parser")
    text = soup.get_text().replace("\n", " ").strip()
    first = re.split(r'[.!?。！？]', text)[0].strip()
    return first[:120]


def fetch_web(url: str, max_items: int = 5) -> list[dict]:
    """Scrape titles from a web page (no dates available)."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        articles = []
        for tag in soup.select(
            "article h2 a, article h3 a, h2 a, h3 a, .post-title a"
        )[:max_items]:
            title = tag.get_text().strip()
            if title and len(title) > 10:
                link = tag.get("href", "")
                if link and not link.startswith("http"):
                    # Resolve relative URLs
                    from urllib.parse import urljoin
                    link = urljoin(url, link)
                articles.append({"title": title, "date": "", "summary": "", "link": link})

        if not articles:
            for tag in soup.select("h2, h3")[:max_items]:
                title = tag.get_text().strip()
                if title and len(title) > 20:
                    articles.append({"title": title, "date": "", "summary": "", "link": ""})

        return articles
    except Exception as e:
        print(f"  Web error {url}: {e}", file=sys.stderr)
        return []


# --- Formatting ---

def format_markdown(results: dict[str, list[dict]]) -> str:
    lines = [f"## {TODAY} (Automated Daily Scan)\n"]
    for source, articles in results.items():
        if not articles:
            continue
        lines.append(f"### {source}\n")
        for a in articles:
            date_part = f" ({a['date']})" if a["date"] else ""
            summary_part = f" — {a['summary']}" if a["summary"] else ""
            title_part = f"[{a['title']}]({a['link']})" if a.get("link") else a["title"]
            lines.append(f"- **{title_part}**{date_part}{summary_part}")
        lines.append("")
    return "\n".join(lines)



# --- Article archival ---

ARCHIVE_TIMEOUT = 10


def _slug(text: str) -> str:
    """Normalise text to a filesystem-safe slug."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower().strip())[:60].strip('-')


def _title_hash(title: str) -> str:
    return hashlib.sha256(title.encode()).hexdigest()[:8]


def archive_article(article: dict, source_name: str, tier: int) -> None:
    """Extract and cache full article text for Tier 1 sources."""
    if tier != 1:
        return
    link = article.get("link", "")
    if not link:
        return

    date_str = article.get("date") or TODAY
    slug = _slug(source_name)
    h = _title_hash(article["title"])
    filename = f"{date_str}_{slug}_{h}.json"
    filepath = ARTICLE_CACHE_DIR / filename

    if filepath.exists():
        return  # already archived

    # Extract full text via trafilatura
    text = None
    try:
        downloaded = trafilatura.fetch_url(link)
        if downloaded:
            text = trafilatura.extract(downloaded)
    except Exception as e:
        print(f"  Archive error {link}: {e}", file=sys.stderr)

    record = {
        "title": article["title"],
        "date": date_str,
        "source": source_name,
        "tier": tier,
        "link": link,
        "summary": article.get("summary", ""),
        "text": text,
        "fetched_at": NOW.isoformat(),
    }

    ARTICLE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    filepath.write_text(json.dumps(record, ensure_ascii=False, indent=2))
    status = f"{len(text)} chars" if text else "null (extraction failed)"
    print(f"  Archived: {filename} [{status}]", file=sys.stderr)


MAX_LOG_LINES = 500
ARCHIVE_DIR = Path.home() / "notes"


def rotate_log_if_needed():
    """Archive old entries when log exceeds MAX_LOG_LINES."""
    if not NEWS_LOG.exists():
        return
    content = NEWS_LOG.read_text()
    lines = content.splitlines()
    if len(lines) <= MAX_LOG_LINES:
        return

    # Find date headers — keep last 14 days, archive the rest
    cutoff = (NOW - timedelta(days=14)).strftime("%Y-%m-%d")
    keep_from = None
    for i, line in enumerate(lines):
        m = re.match(r'^## (\d{4}-\d{2}-\d{2})', line)
        if m and m.group(1) < cutoff:
            keep_from = i
            break

    if keep_from is None:
        return  # everything is recent

    # Split: header + recent entries vs old entries
    marker_line = next(
        (i for i, l in enumerate(lines) if "<!-- News entries below" in l), 0
    )
    header = lines[:marker_line + 1]
    recent = lines[marker_line + 1:keep_from]
    old = lines[keep_from:]

    # Archive old entries
    month = NOW.strftime("%Y-%m")
    archive_path = ARCHIVE_DIR / f"AI News Log - Archive {month}.md"
    mode = "a" if archive_path.exists() else "w"
    with open(archive_path, mode) as f:
        if mode == "w":
            f.write(f"# AI News Log Archive — {month}\n\n")
        f.write("\n".join(old) + "\n")

    # Rewrite main log with header + recent only
    NEWS_LOG.write_text("\n".join(header + recent) + "\n")
    print(
        f"Rotated: archived {len(old)} lines to {archive_path.name}, "
        f"kept {len(recent)} lines.",
        file=sys.stderr,
    )


# --- Main ---

def main():
    no_archive = "--no-archive" in sys.argv

    rotate_log_if_needed()

    with open(SOURCES_YAML) as f:
        config = yaml.safe_load(f)

    state = load_state()
    since_date = get_last_scan_date(state)
    title_prefixes = load_title_prefixes()

    print(f"Last scan: {since_date}. Filtering articles after this date.", file=sys.stderr)

    # Collect all sources with tier info (tier controls display priority, not fetch)
    all_sources = []
    for section in ("web_sources", "consulting_and_regulators", "bank_tech_blogs", "chinese_sources"):
        for source in config.get(section, []):
            all_sources.append(source)

    results: dict[str, list[dict]] = {}
    skipped = []
    archived_count = 0

    for source in all_sources:
        name = source["name"]
        tier = source.get("tier", 2)
        cadence = source.get("cadence", "daily")

        if not should_fetch(name, cadence, state):
            skipped.append(name)
            continue

        print(f"Fetching: {name}...", file=sys.stderr)

        # Fetch — RSS uses date filter, web uses title-prefix dedup
        if "rss" in source:
            articles = fetch_rss(source["rss"], since_date)
        else:
            articles = fetch_web(source.get("url", ""))

        # Filter junk + title-prefix dedup
        new_articles = []
        for a in articles:
            if is_junk(a["title"]):
                continue
            prefix = _title_prefix(a["title"])
            if prefix in title_prefixes:
                continue
            new_articles.append(a)
            title_prefixes.add(prefix)

        # Archive full text for Tier 1 articles
        if not no_archive:
            for a in new_articles:
                if a.get("link") and tier == 1:
                    archive_article(a, name, tier)
                    archived_count += 1

        if new_articles:
            results[name] = new_articles

        state[name] = NOW.isoformat()

    save_state(state)

    if skipped:
        print(f"Skipped (cadence): {', '.join(skipped)}", file=sys.stderr)

    if not results:
        print("No new articles found.", file=sys.stderr)
        return

    total = sum(len(v) for v in results.values())

    # Append to log
    md = format_markdown(results)
    if NEWS_LOG.exists():
        content = NEWS_LOG.read_text()
        marker = "<!-- News entries below, added by /ai-news -->"
        if marker in content:
            content = content.replace(marker, f"{marker}\n\n{md}")
        else:
            content += f"\n\n{md}"
        NEWS_LOG.write_text(content)

    archive_msg = f", archived {archived_count} articles" if archived_count else ""
    print(f"Logged {total} new articles{archive_msg}.", file=sys.stderr)



if __name__ == "__main__":
    main()
