#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml", "httpx", "openai", "yt-dlp"]
# ///
"""
Content Digest — Monthly insight extraction from YouTube channels.

Fetches recent episodes via yt-dlp, extracts transcripts, runs LLM insight
extraction via OpenRouter, and writes digest notes to the Obsidian vault.

Usage:
    uv run ~/skills/digest/digest.py [source_name] [--days N] [--dry-run]

Examples:
    uv run ~/skills/digest/digest.py                    # All sources, last 30 days
    uv run ~/skills/digest/digest.py huberman           # Just Huberman
    uv run ~/skills/digest/digest.py --days 60          # Last 60 days
    uv run ~/skills/digest/digest.py --dry-run          # List episodes only
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from openai import OpenAI

SKILL_DIR = Path(__file__).parent
SOURCES_FILE = SKILL_DIR / "sources.yaml"
TRANSCRIPT_SCRIPT = Path.home() / "skills" / ".archive" / "youtube-transcript" / "extract_transcript.py"
VAULT_DIR = Path.home() / "notes"

INSIGHT_PROMPT = """\
You are an expert at extracting actionable insights from podcast and video transcripts.
Analyze this transcript and extract ALL insightful, non-trivial points. Be comprehensive.

Structure your output as:

## Key Insights

For each insight:
- **Claim:** What is being asserted
- **Evidence:** [RCT | Meta-analysis | Observational | Animal | Mechanistic | Expert opinion | Anecdotal]
- **Mechanism:** Brief explanation of why/how (if discussed)
- **Actionable takeaway:** What to do with this (if applicable)

## Protocols & Recommendations

Specific actionable protocols mentioned. Include full specifics:
- Substance/practice name
- Dose / intensity / duration
- Timing (time of day, relative to meals, etc.)
- Frequency
- Caveats or contraindications mentioned

## Contrarian or Surprising Points

Anything that contradicts common belief, popular health advice, or might surprise a well-read audience.

## Notable Quotes

2-3 most impactful direct quotes (verbatim from transcript).

## Episode Summary

3-5 sentence overview for quick scanning.

Be thorough. Extract every non-trivial insight. Better to include too much than too little.\
"""


def load_sources(filter_name: str | None = None) -> list[dict]:
    with open(SOURCES_FILE) as f:
        sources = yaml.safe_load(f)
    if filter_name:
        q = filter_name.lower()
        sources = [
            s for s in sources
            if q in s["name"].lower() or q in s.get("vault_path", "").lower()
        ]
    return sources


def list_youtube_videos(handle: str, max_items: int = 15) -> list[dict]:
    """List recent videos from a YouTube channel using yt-dlp."""
    url = f"https://www.youtube.com/{handle}/videos"
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-download",
        "--playlist-items", f"1-{max_items}",
        "--print", '{"id":"%(id)s","title":"%(title)s","upload_date":"%(upload_date)s","duration":"%(duration)s"}',
        "--no-warnings",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp listing failed: {result.stderr}")

    videos = []
    for line in result.stdout.strip().splitlines():
        try:
            data = json.loads(line)
            upload_date = data.get("upload_date")
            if upload_date and upload_date != "NA":
                data["date"] = datetime.strptime(upload_date, "%Y%m%d").replace(tzinfo=timezone.utc)
            else:
                data["date"] = None
            videos.append(data)
        except (json.JSONDecodeError, ValueError):
            continue
    return videos


def extract_transcript(video_id: str) -> str:
    """Extract transcript using youtube-transcript-api (clean) with yt-dlp fallback."""
    # Try API method first (no duplication issues)
    cmd = [
        "uv", "run", str(TRANSCRIPT_SCRIPT),
        video_id, "--clean", "--method", "api",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()

    # Fallback to yt-dlp
    print("  youtube-transcript-api failed, trying yt-dlp...", file=sys.stderr)
    cmd = [
        "uv", "run", str(TRANSCRIPT_SCRIPT),
        video_id, "--clean", "--method", "ytdlp",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode == 0 and result.stdout.strip():
        # Deduplicate yt-dlp output (auto-captions repeat lines 3x)
        return _deduplicate_transcript(result.stdout.strip())

    raise RuntimeError(f"Both transcript methods failed. stderr: {result.stderr}")


def _deduplicate_transcript(text: str) -> str:
    """Remove consecutive duplicate phrases from yt-dlp auto-caption output."""
    words = text.split()
    if len(words) < 6:
        return text

    # Sliding window deduplication: if a sequence of N words repeats
    # immediately, keep only one copy
    result = []
    i = 0
    while i < len(words):
        # Try chunk sizes from large to small
        found_dup = False
        for chunk_size in range(min(20, (len(words) - i) // 2), 2, -1):
            chunk = words[i : i + chunk_size]
            next_chunk = words[i + chunk_size : i + 2 * chunk_size]
            if chunk == next_chunk:
                result.extend(chunk)
                # Skip all consecutive copies
                j = i + chunk_size
                while words[j : j + chunk_size] == chunk:
                    j += chunk_size
                i = j
                found_dup = True
                break
        if not found_dup:
            result.append(words[i])
            i += 1

    return " ".join(result)


def extract_insights(transcript: str, title: str, model: str) -> str:
    """Run LLM insight extraction on a transcript via OpenRouter."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": INSIGHT_PROMPT},
            {"role": "user", "content": f"Episode: {title}\n\nTranscript:\n{transcript}"},
        ],
        max_tokens=8000,
    )
    return response.choices[0].message.content


def write_digest(source: dict, episodes_insights: list[dict], month_str: str) -> Path:
    """Write digest note to vault."""
    vault_path = VAULT_DIR / source["vault_path"]
    vault_path.mkdir(parents=True, exist_ok=True)

    digest_file = vault_path / f"{month_str} Digest.md"

    lines = [
        f"# {source['name']} — {month_str} Digest",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Episodes: {len(episodes_insights)}",
        "",
    ]

    for ep in episodes_insights:
        duration_s = ep.get("duration")
        if duration_s and duration_s != "NA":
            try:
                mins = int(float(duration_s)) // 60
                duration_str = f" ({mins} min)"
            except (ValueError, TypeError):
                duration_str = ""
        else:
            duration_str = ""

        date_str = ep["date"].strftime("%Y-%m-%d") if ep.get("date") else "unknown"

        lines.extend([
            "---",
            "",
            f"## {ep['title']}",
            "",
            f"**Published:** {date_str}{duration_str}",
            f"**Video:** https://youtube.com/watch?v={ep['id']}",
            "",
            ep["insights"],
            "",
        ])

    digest_file.write_text("\n".join(lines), encoding="utf-8")
    return digest_file


def main():
    parser = argparse.ArgumentParser(description="Monthly content digest")
    parser.add_argument("source", nargs="?", help="Source name filter (partial match)")
    parser.add_argument("--days", type=int, default=30, help="Look back N days (default: 30)")
    parser.add_argument("--dry-run", action="store_true", help="List episodes without processing")
    parser.add_argument("--model", default="google/gemini-2.0-flash-001", help="OpenRouter model ID")
    parser.add_argument("--max-videos", type=int, default=15, help="Max videos to fetch per channel")
    args = parser.parse_args()

    if not args.dry_run and not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    sources = load_sources(args.source)
    if not sources:
        print(f"No sources found matching '{args.source}'", file=sys.stderr)
        sys.exit(1)

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    month_str = datetime.now().strftime("%Y-%m")

    for source in sources:
        print(f"\n{'=' * 60}", file=sys.stderr)
        print(f"Source: {source['name']}", file=sys.stderr)
        print(f"{'=' * 60}", file=sys.stderr)

        if source["type"] == "youtube":
            try:
                videos = list_youtube_videos(source["handle"], max_items=args.max_videos)
            except Exception as e:
                print(f"Error listing videos: {e}", file=sys.stderr)
                continue

            # Filter to recent episodes
            episodes = [v for v in videos if v.get("date") and v["date"] >= since]
        else:
            print(f"Unsupported source type: {source['type']}", file=sys.stderr)
            continue

        if not episodes:
            print(f"No episodes in last {args.days} days", file=sys.stderr)
            continue

        print(f"Found {len(episodes)} episodes:", file=sys.stderr)
        for ep in episodes:
            duration_s = ep.get("duration", "0")
            try:
                mins = int(float(duration_s)) // 60
            except (ValueError, TypeError):
                mins = 0
            date_str = ep["date"].strftime("%Y-%m-%d") if ep.get("date") else "?"
            print(f"  [{date_str}] {ep['title']} ({mins}m)", file=sys.stderr)

        if args.dry_run:
            continue

        episodes_insights = []
        for i, ep in enumerate(episodes, 1):
            print(f"\n[{i}/{len(episodes)}] Processing: {ep['title']}", file=sys.stderr)

            try:
                print("  Extracting transcript...", file=sys.stderr)
                transcript = extract_transcript(ep["id"])
                word_count = len(transcript.split())
                print(f"  Transcript: {word_count:,} words", file=sys.stderr)

                print(f"  Extracting insights ({args.model})...", file=sys.stderr)
                insights = extract_insights(transcript, ep["title"], model=args.model)

                episodes_insights.append({
                    **ep,
                    "insights": insights,
                })
                print("  Done.", file=sys.stderr)
            except Exception as e:
                print(f"  ERROR: {e}", file=sys.stderr)
                continue

        if episodes_insights:
            digest_file = write_digest(source, episodes_insights, month_str)
            print(f"\nDigest written: {digest_file}", file=sys.stderr)
        else:
            print("\nNo episodes processed successfully.", file=sys.stderr)


if __name__ == "__main__":
    main()
