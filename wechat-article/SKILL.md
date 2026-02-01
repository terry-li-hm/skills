---
name: wechat-article
description: Fetch and extract content from WeChat public account articles. Use when user shares a WeChat URL or asks to read a WeChat article.
user_invocable: false
---

# WeChat Article Extractor

Extract content from WeChat public account articles (mp.weixin.qq.com).

## When to Use

- User shares a WeChat article URL
- User asks to read/summarize a WeChat article
- Need to extract content from mp.weixin.qq.com

## URL Formats

WeChat articles have two URL formats:

| Format | Example | Supported |
|--------|---------|-----------|
| **Short** | `mp.weixin.qq.com/s/ABC123xyz` | ✅ Direct extraction |
| **Long** | `mp.weixin.qq.com/s?__biz=...&mid=...&sn=...` | ❌ Needs conversion |

## Extraction Workflow

### Step 1: Identify URL Format

```python
import re

def is_short_url(url: str) -> bool:
    """Check if URL is short format (directly usable)."""
    # Short format: /s/ followed by alphanumeric ID (no query params)
    return bool(re.match(r'https?://mp\.weixin\.qq\.com/s/[A-Za-z0-9_-]+$', url))
```

### Step 2: Extract Content

**For short URLs** — Use wechat.imagenie.us API:

```bash
curl -X POST "https://wechat.imagenie.us/extract" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/ABC123","format":"markdown"}'
```

Response:
```json
{
  "success": true,
  "content": "# Article Title\n\nArticle content in markdown..."
}
```

**For long URLs** — Convert first:

1. Extract article title from the URL (if available) or fetch page title
2. Search for short URL: `WebSearch: "article title" site:mp.weixin.qq.com/s/`
3. Use the short URL with wechat.imagenie.us

### Step 3: Fallback Options

If wechat.imagenie.us fails:

1. **Mirror sites** — Search for reposts:
   ```
   WebSearch: "article title" site:163.com OR site:zhihu.com OR site:csdn.net
   ```

2. **Serper scrape** — Try mirror URL directly:
   ```bash
   # OpenClaw
   mcporter call serper.scrape url="[mirror URL]"
   
   # Claude Code
   mcp__serper__scrape
   ```

## Complete Workflow

```
User provides WeChat URL
         │
         ▼
   Is short URL?
    (/s/ABC123)
         │
    ┌────┴────┐
   Yes        No
    │          │
    ▼          ▼
  Use API   Search for
  directly  short URL
    │          │
    ▼          ▼
  Success?  Found short URL?
    │          │
   ┌┴┐        ┌┴┐
  Yes No    Yes  No
   │   │     │    │
   ▼   │     ▼    ▼
Return │   Use   Search
content│   API   mirrors
       │     │    │
       └──┬──┘    │
          ▼       ▼
       Search   Scrape
       mirrors  mirror
```

## Example Usage

**Input:** `https://mp.weixin.qq.com/s/nnysYJCNQA-SPUefOPBwZw`

**Action:**
```bash
curl -s -X POST "https://wechat.imagenie.us/extract" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/nnysYJCNQA-SPUefOPBwZw","format":"markdown"}'
```

**Output:** Full article in Markdown format.

## API Reference

### wechat.imagenie.us

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/extract` | POST | Extract article (recommended) |
| `/{url}` | GET | Direct access (HTML default) |
| `/health` | GET | Service health check |
| `/status` | GET | Service status |

**POST /extract body:**
```json
{
  "url": "https://mp.weixin.qq.com/s/ABC123",
  "format": "markdown"  // or "json", "html"
}
```

**Headers for GET:**
- `Accept: text/markdown` — Returns Markdown instead of HTML

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_URL` | Long URL format | Search for short URL |
| `POOR_CONTENT_QUALITY` | Extraction failed | Try mirror sites |
| 404 | URL encoding issue | Use POST /extract instead |
| 429 | Rate limited | Wait and retry |

## Limitations

- Only short URLs work with the API
- Some articles may be deleted or restricted
- Rate limits apply to the extraction service
- Mirror sites may have outdated versions

## Related

- See `web-search` skill for mirror site search strategies
- See `evaluate-article` skill for article analysis workflow
