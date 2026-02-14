---
name: summarize
description: Summarize or extract text from URLs, podcasts, and local files. "summarize this"
user_invocable: true
github_url: https://github.com/steipete/summarize
---

# Summarize

Fast CLI to summarize URLs, local files, and YouTube links.

## Trigger

Use when:
- User says "summarize this URL/article"
- User asks "what's this link/video about?"
- User says "transcribe this YouTube/video"
- User wants to extract content from a webpage or PDF

## Prerequisites

- `summarize` CLI installed: `brew install steipete/tap/summarize`
- API key for chosen model provider (OpenRouter, Anthropic, Google, etc.)

## Commands

### Summarize URL

```bash
summarize "https://example.com/article" --model google/gemini-3-flash-preview
```

### Summarize Local File

```bash
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
```

### YouTube Transcript

```bash
# Summary
summarize "https://youtu.be/VIDEO_ID" --youtube auto

# Extract transcript only (no summary)
summarize "https://youtu.be/VIDEO_ID" --youtube auto --extract-only
```

### Model Selection

```bash
# Fast + cheap
summarize "URL" --model google/gemini-3-flash-preview

# Higher quality
summarize "URL" --model anthropic/claude-sonnet-4
```

## Content Fetch Fallback Chain

When fetching URL content, try in order:

```
1. WebFetch (fast, cached, 15min)
   ↓ fails
2. summarize CLI (Chrome UA, handles WeChat)
   ↓ fails
3. Jina Reader: curl -s -H "Accept: text/markdown" "https://r.jina.ai/URL"
   ↓ fails
4. Browser automation (for login-required pages)
   ↓ fails
5. Ask user for copy/paste
```

### WeChat articles

`summarize` is the primary tool — bypasses WeChat CAPTCHA via Chrome UA string.

```bash
summarize "https://mp.weixin.qq.com/s/ARTICLE_ID" --extract-only
```

Short URLs (`/s/ABC123`) are more stable than long URLs (`?__biz=...`).
If `summarize` also fails, fallback to Firecrawl (needs `FIRECRAWL_API_KEY`, 500 free/month) or search for mirror on zhihu.com/163.com/csdn.net.

### Login-required sites

Always need browser automation: LinkedIn, X/Twitter, WhatsApp Web, banking sites.

### Xiaohongshu (XHS)

Images need `Referer: https://www.xiaohongshu.com/` header or you get 403.

## Tips

- For huge transcripts, return a tight summary first, then ask which section to expand
- Use `--extract-only` when user explicitly wants the raw transcript
- Supports PDFs, articles, YouTube, and most web content
- For batch YouTube channel digests, use `/digest` instead
