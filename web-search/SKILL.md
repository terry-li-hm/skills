---
name: web-search
description: Reference for choosing the right web search tool. Not user-invocable — use as internal guidance when performing searches.
user_invocable: false
---

# Web Search Tool Selection Guide

Reference for choosing the optimal MCP search tool based on use case. Updated 2026-01-21 after comparative testing.

## Available Tools

| Tool | Type | Best For |
|------|------|----------|
| **WebSearch** | Built-in | General purpose, synthesized summaries |
| **Perplexity** | MCP | Deep research, detailed analysis |
| **Serper** | MCP | Google results, regional targeting |
| **Exa** | MCP | Code context, semantic search |
| **Brave** | MCP | Alternative web search, video search |
| **Tavily** | MCP | Content extraction, crawling |

## Use Case Recommendations

### AI News
1. **Quick overview**: `WebSearch` — returns synthesized summary with key trends
2. **Deep dive**: `mcp__perplexity__perplexity_search` — rich excerpts, analysis
3. **Avoid**: Tavily (returns press releases), Brave News (mixed unrelated results)

### Job Search
1. **Overview**: `WebSearch` — finds job boards, synthesizes listings
2. **Regional search**: `mcp__serper__google_search` with `gl` parameter (e.g., `gl: "hk"`)
3. **LinkedIn extraction**: `mcp__exa__web_search_exa` or `mcp__tavily__tavily-search`

### Code & Documentation
1. **Primary**: `mcp__exa__get_code_context_exa` — optimized for APIs, libraries, SDKs
2. **Backup**: `mcp__perplexity__perplexity_search`

### Deep Research
1. **Primary**: `mcp__perplexity__perplexity_research` — comprehensive with citations
2. **Reasoning**: `mcp__perplexity__perplexity_reason` — for complex analysis

### General Web Search
1. **Default**: `WebSearch` (built-in) — fast, good summaries
2. **Google-specific**: `mcp__serper__google_search`
3. **Alternative index**: `mcp__brave-search__brave_web_search`

## Tool Details

### WebSearch (Built-in)
- Best all-around for quick answers
- Returns synthesized summaries, not just links
- Good formatting with key points extracted

### Perplexity (MCP)
```
mcp__perplexity__perplexity_search  — Standard search
mcp__perplexity__perplexity_research — Deep research mode
mcp__perplexity__perplexity_reason  — Reasoning mode
mcp__perplexity__perplexity_ask     — Conversational
```
- Excellent for AI news — detailed excerpts with analysis
- `strip_thinking: true` to save context tokens

### Serper (MCP)
```
mcp__serper__google_search
mcp__serper__scrape
```
- Google search via API
- Supports regional targeting: `gl: "hk"`, `gl: "us"`
- Language: `hl: "en"`, `hl: "zh"`
- Clean structured JSON output

### Exa (MCP)
```
mcp__exa__web_search_exa
mcp__exa__get_code_context_exa
```
- Semantic search, good for finding similar content
- `get_code_context_exa` is excellent for programming queries
- Returns full text snippets

### Brave (MCP)
```
mcp__brave-search__brave_web_search
mcp__brave-search__brave_news_search
mcp__brave-search__brave_video_search
mcp__brave-search__brave_image_search
mcp__brave-search__brave_local_search
```
- Alternative to Google index
- Video search is useful
- News search can return unrelated results — use with caution

### Tavily (MCP)
```
mcp__tavily__tavily-search
mcp__tavily__tavily-extract
mcp__tavily__tavily-crawl
mcp__tavily__tavily-map
```
- `tavily-extract` good for scraping specific URLs
- `tavily-crawl` for site mapping
- News search is weak (returns press releases)
- `topic: "news"` parameter available but unreliable

## Quality Rankings (2026-01-21)

### For AI News
1. WebSearch ⭐⭐⭐⭐⭐
2. Perplexity ⭐⭐⭐⭐⭐
3. Serper ⭐⭐⭐⭐
4. Exa ⭐⭐⭐⭐
5. Brave News ⭐⭐⭐
6. Tavily ⭐⭐

### For Job Search
1. WebSearch ⭐⭐⭐⭐⭐
2. Serper ⭐⭐⭐⭐
3. Exa ⭐⭐⭐⭐
4. Tavily ⭐⭐⭐⭐
5. Perplexity ⭐⭐⭐
6. Brave ⭐⭐⭐

## WeChat Articles (mp.weixin.qq.com)

WeChat public articles are heavily protected. Most direct access methods fail.

### ✅ Primary Method: wechat.imagenie.us

A Cloudflare Workers API that handles WeChat's anti-bot protection.

**⚠️ IMPORTANT: Only short URLs work!**
- ✅ Works: `https://mp.weixin.qq.com/s/nnysYJCNQA-SPUefOPBwZw`
- ❌ Fails: `https://mp.weixin.qq.com/s?__biz=...&mid=...&idx=...&sn=...`

```bash
# POST /extract endpoint (recommended for Claude)
curl -X POST "https://wechat.imagenie.us/extract" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mp.weixin.qq.com/s/ABC123","format":"markdown"}'

# GET endpoint (for curl with headers)
curl -H "Accept: text/markdown" "https://wechat.imagenie.us/https://mp.weixin.qq.com/s/ABC123"
```

**Endpoints:**
- `POST /extract` — Best for programmatic use, returns JSON with markdown/html
- `GET /{wechat-url}` — Returns HTML (or Markdown with `Accept: text/markdown` header)
- `GET /health` — Service status check

**Features:** Multi-layer caching, WeChat footer removal, LLM-friendly markdown formatting

**Finding short URLs:** Use WebSearch with `site:mp.weixin.qq.com/s/` to find articles with short URL format.

### ✅ Fallback: Mirror Sites

If the API fails, search for article reposts:
1. Search for article title/keywords on mirror sites
2. Common mirrors: **163.com**, **zhihu.com**, **csdn.net**
3. Use `WebSearch` with Chinese title + site names

```
WebSearch: "长时间运行Agent Cursor Anthropic" site:163.com OR site:zhihu.com
```

Popular WeChat tech articles often get republished within days.

### ❌ Methods That Don't Work

| Method | Result |
|--------|--------|
| WebFetch direct | CAPTCHA block |
| Serper scrape | CAPTCHA block |
| Jina Reader (r.jina.ai) | CAPTCHA block |
| Claude in Chrome | Domain blocked by safety policy |
| Playwright + stealth | CAPTCHA block |
| AgentQL | CAPTCHA block |

## Removed Tools

- **Google Search (direct API)** — Removed 2026-01-21. "Custom Search JSON API not enabled" error. Serper provides same Google results.

## Notes

- For Terry's use cases (AI news, job search), core tools are: **WebSearch + Perplexity + Serper**
- Exa worth keeping for code context
- Brave and Tavily are somewhat redundant but kept for specialized features (video search, crawling)
