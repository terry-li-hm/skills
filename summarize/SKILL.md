---
name: summarize
description: Summarize or extract text from URLs, podcasts, and local files. "summarize this"
user_invocable: true
github_url: https://github.com/steipete/summarize
---

# Summarize

Summarize URLs, local files, and YouTube links. Prefer direct summarization over the CLI.

## Trigger

Use when:
- User says "summarize this URL/article"
- User asks "what's this link/video about?"
- User says "transcribe this YouTube/video"
- User wants to extract content from a webpage or PDF
- User pastes a URL with no other context (implicit "what's this?")

## Approach

**Default: Fetch content → read directly → summarize in-context.** This produces better, more contextual summaries than delegating to the `summarize` CLI (which adds a middleman LLM). Especially for content that will be saved to vault — tagging, relevance notes, and quotables are best done in-context.

### Content Fetch Chain

Try in order (WeChat articles skip to step 2 — Jina/WebFetch both hit CAPTCHA):

```
1. Jina Reader: curl -s -H "Accept: text/markdown" "https://r.jina.ai/URL"
   (reliable, full content, no truncation)
   ↓ fails
2. agent-browser: open URL → eval JS to extract text
   (handles WeChat, SPAs, CAPTCHA-protected pages)
   ↓ fails
3. WebFetch (fast, cached 15min, but may truncate long content)
   ↓ fails
4. summarize CLI --extract-only (Chrome UA fallback)
   ↓ fails
5. Ask user for copy/paste
```

### YouTube Transcripts

```bash
# Extract transcript only (truncates ~200 lines — use for short videos)
summarize "https://youtu.be/VIDEO_ID" --youtube auto --extract-only

# For full transcripts, use youtube-transcript-api directly via uv:
uv run --script --python 3.13 -q - <<'PYEOF'
# /// script
# dependencies = ["youtube-transcript-api"]
# ///
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch('VIDEO_ID')
entries = list(transcript)
full_text = ' '.join(e.text for e in entries)
last = entries[-1]
print(f'Words: {len(full_text.split())} | Duration: {(last.start + last.duration)/60:.1f} min')
print(full_text)
PYEOF
```

**API gotcha (Feb 2026):** `youtube-transcript-api` v1.x changed from class method `YouTubeTranscriptApi.get_transcript(id)` to instance method `YouTubeTranscriptApi().fetch(id)`. Entries use `.text`/`.start`/`.duration` attributes, not dict keys.

**Verification:** For long transcripts fetched via `--extract-only`, cross-check word count and last timestamp against video duration. The CLI truncates silently.

For batch YouTube channel digests, use `/digest` instead.

### WeChat Articles

Jina Reader and WebFetch both hit WeChat's CAPTCHA wall. Use `agent-browser eval` directly:

```bash
agent-browser open "https://mp.weixin.qq.com/s/ARTICLE_ID"
# Wait for page load, then extract full text:
agent-browser eval "document.getElementById('js_content').innerText"
```

This returns the complete article text in one call — no scrolling or screenshots needed.

Short URLs (`/s/ABC123`) are more stable than long URLs (`?__biz=...`).
Fallback: `summarize` CLI with `--extract-only`, or search for mirror on zhihu.com/163.com/csdn.net.

### Login-required Sites

Always need browser automation: LinkedIn, X/Twitter, WhatsApp Web, banking sites.

### Xiaohongshu (XHS)

Images need `Referer: https://www.xiaohongshu.com/` header or you get 403.

## CLI Fallback

The `summarize` CLI (`brew install steipete/tap/summarize`, v0.10.0) is available but has known issues:
- Google API key (`GEMINI_API_KEY`) is set but invalid for Generative AI API
- Anthropic model can return empty summaries on long content
- `--extract-only` truncates long transcripts (~200 lines)

If the CLI is needed (e.g., WeChat), use `--model openrouter/...` to avoid the Google key issue.

## Output

- For huge transcripts, return a tight summary first, then ask which section to expand
- When saving to vault, include: source URL, date, type, tags, relevance notes
- Quotable lines are valuable — pull 2-3 standout quotes
