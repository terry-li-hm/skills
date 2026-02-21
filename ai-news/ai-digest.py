#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pyyaml", "httpx", "openai"]
# ///
"""
AI Thematic Digest — Monthly evidence-grounded synthesis of AI developments.

Reads archived article full text from ~/.cache/ai-news-articles/ (populated by
ai-news-daily.py cron) and AI News Log entries, clusters by theme, and produces
evidence briefs with claims, sources, echo counts, and banking implications.

Usage:
    uv run ~/skills/ai-news/ai-digest.py                    # Current month
    uv run ~/skills/ai-news/ai-digest.py --month 2026-02    # Specific month
    uv run ~/skills/ai-news/ai-digest.py --dry-run           # Show themes only
    uv run ~/skills/ai-news/ai-digest.py --themes 5          # Limit to 5 themes
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from openai import OpenAI

# Paths
ARTICLE_CACHE_DIR = Path.home() / ".cache" / "ai-news-articles"
NEWS_LOG = Path.home() / "notes" / "AI News Log.md"
OUTPUT_DIR = Path.home() / "notes" / "AI & Tech"

HKT = timezone(timedelta(hours=8))

# LLM config
DEFAULT_MODEL = "google/gemini-3-flash-preview"

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_archived_articles(month: str) -> list[dict]:
    """Load cached article JSONs for a given YYYY-MM month."""
    if not ARTICLE_CACHE_DIR.exists():
        return []
    articles = []
    for f in sorted(ARTICLE_CACHE_DIR.iterdir()):
        if not f.name.endswith(".json"):
            continue
        if not f.name.startswith(month):
            continue
        try:
            data = json.loads(f.read_text())
            data["_file"] = f.name
            articles.append(data)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  Skip {f.name}: {e}", file=sys.stderr)
    return articles


def load_news_log_entries(month: str) -> list[dict]:
    """Parse AI News Log for entries in the target month.

    Returns lightweight dicts with title, source, date, link, summary.
    These supplement archived articles — many Tier 2 sources won't have
    full text but their headlines still inform theme clustering.
    """
    if not NEWS_LOG.exists():
        return []

    content = NEWS_LOG.read_text()
    entries = []
    current_date = ""
    current_source = ""

    for line in content.splitlines():
        # Date header: ## 2026-02-20 (Automated Daily Scan)
        date_match = re.match(r"^## (\d{4}-\d{2}-\d{2})", line)
        if date_match:
            current_date = date_match.group(1)
            continue

        # Source header: ### Simon Willison
        source_match = re.match(r"^### (.+)", line)
        if source_match:
            current_source = source_match.group(1).strip()
            continue

        # Article entry: - **[Title](link)** (date) — summary
        # or: - **Title** (date) — summary
        article_match = re.match(
            r"^- \*\*(?:\[([^\]]+)\]\(([^)]+)\)|([^*]+))\*\*"
            r"(?:\s*\(([^)]*)\))?"
            r"(?:\s*—\s*(.+))?",
            line,
        )
        if article_match and current_date.startswith(month):
            title = (article_match.group(1) or article_match.group(3) or "").strip()
            link = article_match.group(2) or ""
            date = article_match.group(4) or current_date
            summary = article_match.group(5) or ""
            if title:
                entries.append({
                    "title": title,
                    "source": current_source,
                    "date": date,
                    "link": link,
                    "summary": summary,
                })

    return entries


# ---------------------------------------------------------------------------
# LLM calls
# ---------------------------------------------------------------------------


def _llm_call(client: OpenAI, model: str, system: str, user: str,
              max_tokens: int = 4000) -> str:
    """Single LLM call via OpenRouter."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def identify_themes(client: OpenAI, model: str, articles: list[dict],
                    log_entries: list[dict], max_themes: int) -> list[dict]:
    """Pass 1: Identify thematic clusters from article metadata."""
    # Build metadata listing
    items = []
    for i, a in enumerate(articles):
        text_preview = ""
        if a.get("text"):
            words = a["text"].split()[:200]
            text_preview = " ".join(words)
        items.append(
            f"[{i}] {a['date']} | {a['source']} | {a['title']}"
            f"\n    Summary: {a.get('summary', '')}"
            f"\n    Preview: {text_preview[:500]}"
        )

    # Add log entries (offset index to avoid collision)
    offset = len(articles)
    for i, e in enumerate(log_entries):
        items.append(
            f"[{offset + i}] {e['date']} | {e['source']} | {e['title']}"
            f"\n    Summary: {e.get('summary', '')}"
        )

    listing = "\n\n".join(items)

    system = f"""\
You identify thematic clusters in AI news for a consultant advising banks on AI strategy.

Rules:
- Identify {max_themes} themes most relevant to AI in banking/financial services
- Each theme should have 3+ articles supporting it
- Themes should be specific (not "AI progress") — e.g., "Agentic AI frameworks maturing for enterprise"
- Include cross-cutting themes (regulation, open-source vs proprietary, infrastructure)
- Return valid JSON only, no markdown fences"""

    user = f"""\
Below are {len(articles)} archived articles (with full text available) and {len(log_entries)} news log headlines from this month.

Identify up to {max_themes} thematic clusters. For each theme, list the article indices that belong to it.
An article can appear in multiple themes.

Return JSON:
[
  {{
    "theme": "Theme title (specific, not generic)",
    "description": "2-3 sentence description of what's happening",
    "article_indices": [0, 3, 7, 15],
    "banking_relevance": "Why this matters for banks/fintech"
  }}
]

Articles:
{listing}"""

    raw = _llm_call(client, model, system, user, max_tokens=4000)

    # Parse JSON from response (strip markdown fences if present)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)


def synthesize_theme(client: OpenAI, model: str, theme: dict,
                     articles: list[dict], log_entries: list[dict]) -> str:
    """Pass 2: Produce evidence brief for a single theme."""
    # Gather full text for articles in this theme
    all_items = articles + log_entries
    theme_articles = []
    for idx in theme.get("article_indices", []):
        if 0 <= idx < len(all_items):
            theme_articles.append(all_items[idx])

    # Build context with full text where available
    context_parts = []
    for a in theme_articles:
        text = a.get("text", "")
        if text:
            # Truncate to ~3000 words to stay within context
            words = text.split()[:3000]
            text_block = " ".join(words)
        else:
            text_block = a.get("summary", "(no text available)")

        context_parts.append(
            f"### {a.get('source', 'Unknown')} — {a.get('title', 'Untitled')}"
            f"\nDate: {a.get('date', 'unknown')} | Link: {a.get('link', 'n/a')}"
            f"\n\n{text_block}"
        )

    context = "\n\n---\n\n".join(context_parts)

    system = """\
You produce evidence briefs for an AI consultant advising banks. Your output must be:
- Grounded in the source articles (no external knowledge)
- Specific — include verbatim quotes where possible
- Honest about evidence quality — mark [paraphrased] when not verbatim
- Focused on banking/financial services implications"""

    user = f"""\
Theme: {theme['theme']}
Description: {theme['description']}
Banking relevance: {theme['banking_relevance']}

Produce an evidence brief with these sections:

## {theme['theme']}

### Summary
2-3 sentences on the theme.

### Claims & Evidence
For each major claim:
- **Claim:** [specific assertion]
- **Source:** [publication name + date]
- **Quote:** "[verbatim quote]" or [paraphrased] summary
- **Echo count:** [how many of the provided sources make similar claims]
- **Evidence quality:** [Primary research | Industry report | Expert opinion | Derivative coverage]

### Open Questions
What's unresolved or contested across sources.

### Banking & Fintech Implications
Specific implications for:
- Client advisory conversations
- Risk and compliance
- Technology strategy
- Competitive positioning

### Key Quotes
2-3 most impactful verbatim quotes with attribution. Mark [paraphrased] where exact wording unavailable.

---

Source articles:

{context}"""

    return _llm_call(client, model, system, user, max_tokens=6000)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def write_digest(month: str, themes: list[dict], theme_briefs: list[str]) -> Path:
    """Write the thematic digest to the vault."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{month} AI Thematic Digest.md"

    now = datetime.now(HKT)
    lines = [
        f"# AI Thematic Digest — {month}",
        "",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M')} HKT",
        f"Themes: {len(themes)}",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
    ]

    for i, theme in enumerate(themes, 1):
        anchor = re.sub(r"[^a-z0-9 ]", "", theme["theme"].lower()).replace(" ", "-")
        lines.append(f"{i}. [{theme['theme']}](#{anchor})")

    lines.extend(["", "---", ""])

    for brief in theme_briefs:
        lines.extend([brief, "", "---", ""])

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="AI Thematic Digest — monthly evidence-grounded synthesis",
    )
    parser.add_argument(
        "--month", default=datetime.now(HKT).strftime("%Y-%m"),
        help="Target month YYYY-MM (default: current)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show themes only, no synthesis")
    parser.add_argument("--themes", type=int, default=8, help="Max themes to identify (default: 8)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter model ID")
    args = parser.parse_args()

    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    # Load data
    print(f"Loading articles for {args.month}...", file=sys.stderr)
    articles = load_archived_articles(args.month)
    log_entries = load_news_log_entries(args.month)

    articles_with_text = sum(1 for a in articles if a.get("text"))
    print(
        f"  Archived articles: {len(articles)} ({articles_with_text} with full text)",
        file=sys.stderr,
    )
    print(f"  News log entries: {len(log_entries)}", file=sys.stderr)

    if not articles and not log_entries:
        print("No data found for this month. Run ai-news-daily.py first.", file=sys.stderr)
        sys.exit(1)

    # Pass 1: Identify themes
    print(f"\nPass 1: Identifying up to {args.themes} themes...", file=sys.stderr)
    themes = identify_themes(client, args.model, articles, log_entries, args.themes)
    print(f"  Found {len(themes)} themes:", file=sys.stderr)
    for i, t in enumerate(themes, 1):
        n_articles = len(t.get("article_indices", []))
        print(f"  {i}. {t['theme']} ({n_articles} articles)", file=sys.stderr)
        print(f"     {t.get('description', '')[:100]}", file=sys.stderr)

    if args.dry_run:
        print("\n--dry-run: Stopping after theme identification.", file=sys.stderr)
        # Print full theme details to stdout for review
        print(json.dumps(themes, indent=2, ensure_ascii=False))
        return

    # Pass 2: Synthesize each theme
    print(f"\nPass 2: Synthesizing {len(themes)} theme briefs...", file=sys.stderr)
    theme_briefs = []
    for i, theme in enumerate(themes, 1):
        print(f"  [{i}/{len(themes)}] {theme['theme']}...", file=sys.stderr)
        brief = synthesize_theme(client, args.model, theme, articles, log_entries)
        theme_briefs.append(brief)
        print(f"  Done ({len(brief)} chars)", file=sys.stderr)

    # Write output
    output_path = write_digest(args.month, themes, theme_briefs)
    print(f"\nDigest written: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
