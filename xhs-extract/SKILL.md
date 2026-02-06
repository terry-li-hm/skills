---
name: xhs-extract
description: Extract text and images from Xiaohongshu (小红书/XHS) post URLs. Use when user shares an XHS link or says "xhs", "xiaohongshu", "小红书".
---

# XHS Post Extractor

Extract text content (title, body, tags, stats) and images from Xiaohongshu posts.

## Trigger

Use when:
- User shares an XHS / Xiaohongshu / 小红书 URL
- User says "extract xhs", "parse xhs", "xhs post"
- URL matches `xiaohongshu.com` or `xhslink.com`

## URL Formats

| Format | Example | Notes |
|--------|---------|-------|
| **Explore** | `xiaohongshu.com/explore/{24-char-hex}` | Standard web URL |
| **Discovery** | `xiaohongshu.com/discovery/item/{id}` | Older format |
| **User profile** | `xiaohongshu.com/user/profile/{author}/{id}` | Author-scoped |
| **Short link** | `xhslink.com/{code}` or `xhslink.com/a/{code}` | Share links from app |

Short links get resolved automatically.

## Workflow

### Step 1: Try the Python script (fast path)

```bash
uv run ~/scripts/xhs_extract.py "<url>" --output-dir ~/Downloads
```

Options:
- `--output-dir <dir>` — Where to save images (default: cwd, creates `xhs_{id}/` subfolder)
- `--no-images` — Skip image downloads, text only
- `--json` — Output raw JSON instead of markdown

Markdown goes to stdout, progress/errors to stderr. Pipe-friendly.

### Step 2: If script fails → Playwright MCP

XHS has aggressive anti-scraping. The script works for many public posts but may get blocked. When it fails, use Playwright MCP (already configured with Chrome extension mode):

```
1. browser_navigate → the XHS URL
2. browser_wait_for → selector: "[class*='note-content']" or "img[class*='note']"  (timeout 10s)
3. browser_evaluate → extract data from DOM:
```

**Extraction JS for browser_evaluate:**

```javascript
(() => {
  const result = {};

  // Try __INITIAL_STATE__ first
  if (window.__INITIAL_STATE__) {
    const state = window.__INITIAL_STATE__;
    const noteMap = state?.note?.noteDetailMap;
    if (noteMap) {
      const first = Object.values(noteMap)[0]?.note;
      if (first) {
        result.title = first.title || '';
        result.description = first.desc || '';
        result.author = first.user?.nickname || '';
        result.tags = (first.tagList || []).map(t => '#' + t.name);
        result.images = (first.imageList || []).map(i =>
          (i.urlDefault || i.url || '').replace(/^\/\//, 'https://')
        );
        result.likes = first.interactInfo?.likedCount || '';
        result.collects = first.interactInfo?.collectedCount || '';
        result.comments = first.interactInfo?.commentCount || '';
        return JSON.stringify(result);
      }
    }
  }

  // Fallback: DOM scraping
  const title = document.querySelector('#detail-title')?.innerText
    || document.querySelector('[class*="title"]')?.innerText || '';
  const desc = document.querySelector('#detail-desc')?.innerText
    || document.querySelector('[class*="note-content"]')?.innerText || '';
  const imgs = [...document.querySelectorAll('[class*="note"] img, [class*="slide"] img')]
    .map(i => i.src || i.dataset?.src).filter(Boolean);
  const tags = [...document.querySelectorAll('a[class*="tag"]')]
    .map(a => a.innerText.trim()).filter(t => t.startsWith('#'));

  result.title = title;
  result.description = desc;
  result.images = imgs;
  result.tags = tags;
  return JSON.stringify(result);
})()
```

Then download images with curl (Referer header required):

```bash
curl -o "image_1.jpg" -H "Referer: https://www.xiaohongshu.com/" "<image_url>"
```

### Step 3: If Playwright also fails → agent-browser

Last resort. Use `/agent-browser` to visually navigate and screenshot the post. Then read the screenshot for content.

## Image Download Notes

XHS CDN requires `Referer: https://www.xiaohongshu.com/` header or returns 403. The script handles this automatically. For manual curl:

```bash
curl -H "Referer: https://www.xiaohongshu.com/" \
     -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)..." \
     -o output.jpg "<image_url>"
```

## Output

**Markdown** (default): Title, author, stats, body text, tags, image links.

**JSON** (`--json`): Structured dict with all fields — good for further processing.

**Images**: Saved to `<output-dir>/xhs_<note_id>/` as `<note_id>_1.jpg`, `<note_id>_2.jpg`, etc.

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `403 Forbidden` | Anti-scraping triggered | Use Playwright fallback |
| `418 I'm a teapot` | Bot detection | Use Playwright fallback |
| Empty content | JS-rendered page, no SSR | Use Playwright fallback |
| Short URL fails | Expired share link | Ask user for full URL |
| Image 403 | Missing Referer header | Script handles this; for manual, add `-H "Referer: ..."` |

## Related

- `content-fetch` — General URL extraction (has XHS Referer note)
- `wechat-article` — Similar pattern for WeChat articles
- `archive-article` — Save to Obsidian with local images
