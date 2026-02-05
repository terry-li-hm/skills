---
name: content-fetch
description: Reference for URL fetching patterns and fallbacks. Consult when extracting content from web URLs.
user_invocable: false
---

# Content Fetch

Patterns for fetching and extracting content from URLs.

## Tool Selection

| URL Type | Primary Tool | Fallback |
|----------|--------------|----------|
| General web | `WebFetch` | `tavily_extract` |
| WeChat articles | `wechat-article` script | Manual copy |
| YouTube | `youtube-transcript` | yt-dlp |
| PDFs | `pdf-extract` (LlamaParse) | Local OCR |
| Login-required | Browser automation | None |

## WebFetch Patterns

```
WebFetch(url, prompt="Extract the main content")
```

**Handles:**
- HTML → Markdown conversion
- Redirect following (returns redirect URL if different host)
- 15-minute cache

**Gotchas:**
- Fails on authenticated pages (Google Docs, Confluence, Jira)
- Use `ToolSearch` first to find specialized MCP tools

## Redirect Handling

When WebFetch returns a redirect message:
1. Extract the redirect URL from response
2. Make a new WebFetch request with that URL
3. Don't assume original URL worked

## WeChat URL Patterns

| Pattern | Type | Handling |
|---------|------|----------|
| `mp.weixin.qq.com/s/...` | Short URL | Fetch directly |
| `mp.weixin.qq.com/s?__biz=...` | Long URL | Fetch directly |
| `weixin.qq.com/r/...` | QR redirect | Follow redirect first |

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `INVALID_URL` | Malformed URL | Check URL format |
| `POOR_CONTENT_QUALITY` | Extraction failed | Try tavily_extract |
| 404 | Page not found | URL may have expired |
| 429 | Rate limited | Wait and retry |
| Login wall | Requires auth | Use browser automation |

## Fallback Hierarchy

```
1. WebFetch (fast, cached)
   ↓ fails
2. Jina Reader (free, simple)
   ↓ fails
3. tavily_extract (better at complex pages)
   ↓ fails
4. Browser automation (for login-required)
   ↓ fails
5. Ask user for copy/paste
```

### Jina Reader

Free, no API key. Prepend `https://r.jina.ai/` to any URL:

```bash
curl -s -H "Accept: text/markdown" "https://r.jina.ai/https://example.com/article"
```

**Handles:** Most general web pages, blogs, docs
**Fails on:** WeChat, login-required sites, some anti-scrape sites

## Login-Required Sites

These always need browser automation:
- LinkedIn (job pages, profiles)
- X/Twitter
- WhatsApp Web
- Most banking/corporate sites

## Chinese Platform Gotchas

### WeChat (mp.weixin.qq.com)

**Primary:** `wechat-article` skill (uses wechat.imagenie.us API)

**Backup options if API dies:**
1. **Firecrawl** — AI-driven, paid (500 free/month). Sign up at firecrawl.dev
   ```bash
   pip install firecrawl-py
   # Use getattr() not .get() for v2 API
   ```
2. **Playwright with WeChat UA** — Browser automation with mobile User-Agent
3. **Mirror search** — Articles often reposted to zhihu.com, 163.com, csdn.net

**URL tip:** Short URLs (`/s/ABC123`) more stable than long URLs (`?__biz=...`) which trigger CAPTCHAs.

### Xiaohongshu (小红书)

Images require Referer header or you get 403:

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)...',
    'Referer': 'https://www.xiaohongshu.com/'
}
requests.get(image_url, headers=headers)
```

### Douyin / Bilibili

Require browser automation for most content. Heavy anti-scrape.

## Content Extraction Prompts

**For articles:**
```
"Extract the main article content, including title, author, date, and body text"
```

**For job postings:**
```
"Extract job title, company, location, requirements, responsibilities, and salary if disclosed"
```

**For documentation:**
```
"Extract the technical documentation, including code examples"
```

## Related Skills

- `evaluate-article` — Article evaluation workflow
- `wechat-article` — WeChat-specific extraction
- `youtube-transcript` — YouTube transcript extraction
- `pdf-extract` — PDF text extraction
- `chrome-automation` — Browser fallback patterns
