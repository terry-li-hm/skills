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

Try in order:

```
1. Jina Reader: curl -s -H "Accept: text/markdown" "https://r.jina.ai/URL"
   (reliable, full content, no truncation)
   ↓ fails
2. WebFetch (fast, cached 15min, but may truncate long content)
   ↓ fails
3. summarize CLI --extract-only (Chrome UA, handles WeChat)
   ↓ fails
4. Browser automation (for login-required pages)
   ↓ fails
5. Ask user for copy/paste
```

### YouTube Transcripts

```bash
# Extract transcript only
summarize "https://youtu.be/VIDEO_ID" --youtube auto --extract-only

# Or use youtube-transcript-api directly (cleaner output)
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; ..."
```

For batch YouTube channel digests, use `/digest` instead.

### WeChat Articles

`summarize` CLI is the primary tool here — bypasses WeChat CAPTCHA via Chrome UA string.

```bash
summarize "https://mp.weixin.qq.com/s/ARTICLE_ID" --extract-only
```

Short URLs (`/s/ABC123`) are more stable than long URLs (`?__biz=...`).
Fallback: Firecrawl or search for mirror on zhihu.com/163.com/csdn.net.

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
