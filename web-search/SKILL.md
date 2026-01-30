---
name: web-search
description: Reference for choosing the right web search tool. Not user-invocable — use as internal guidance when performing searches.
user_invocable: false
---

# Web Search Tool Selection Guide

Reference for choosing the optimal search tool based on use case. Updated 2026-01-30.

## Calling Convention

**Claude Code (native MCP):**
```
mcp__perplexity__perplexity_search
```

**OpenClaw (via mcporter):**
```bash
mcporter call perplexity.perplexity_search query="..."
```

Config: `~/clawd/config/mcporter.json` (imported from Claude Code)

## Available Tools

| Tool | Type | Best For |
|------|------|----------|
| **web_search** | Built-in | General purpose, quick searches (Brave API) |
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

### web_search (Built-in)
- Best all-around for quick answers
- Returns synthesized summaries, not just links
- Good formatting with key points extracted

### Perplexity (MCP)
```bash
# OpenClaw
mcporter call perplexity.perplexity_search query="..."
mcporter call perplexity.perplexity_ask userContent="..."

# Claude Code
mcp__perplexity__perplexity_search
mcp__perplexity__perplexity_ask
```
- Excellent for AI news — detailed excerpts with analysis

### Serper (MCP)
```bash
# OpenClaw
mcporter call serper.search query="..." num=10
mcporter call serper.search query="..." gl=hk hl=zh  # Regional

# Claude Code
mcp__serper__google_search
mcp__serper__scrape
```
- Google search via API
- Supports regional targeting: `gl: "hk"`, `gl: "us"`
- Language: `hl: "en"`, `hl: "zh"`
- Clean structured JSON output

### Exa (MCP)
```bash
# OpenClaw
mcporter call exa.web_search_exa query="..." numResults=5 type=deep
mcporter call exa.get_code_context_exa query="React hooks"
mcporter call exa.company_research_exa companyName="Anthropic"

# Claude Code
mcp__exa__web_search_exa
mcp__exa__get_code_context_exa
```
- Semantic search, good for finding similar content
- `get_code_context_exa` is excellent for programming queries
- Returns full text snippets

### Brave (MCP)
```bash
# OpenClaw
mcporter call brave-search.brave_web_search query="..."
mcporter call brave-search.brave_news_search query="..."
mcporter call brave-search.brave_video_search query="..."

# Claude Code
mcp__brave-search__brave_web_search
mcp__brave-search__brave_news_search
mcp__brave-search__brave_video_search
```
- Alternative to Google index
- Video search is useful
- News search can return unrelated results — use with caution

### Tavily (MCP)
```bash
# OpenClaw
mcporter call tavily.tavily-search query="..."
mcporter call tavily.tavily-extract urls='["https://..."]'

# Claude Code
mcp__tavily__tavily-search
mcp__tavily__tavily-extract
mcp__tavily__tavily-crawl
```
- `tavily-extract` good for scraping specific URLs
- `tavily-crawl` for site mapping
- News search is weak (returns press releases)

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

**See the dedicated `wechat-article` skill for full workflow.**

Quick reference:
- **Primary:** `wechat.imagenie.us` API (only short URLs: `/s/ABC123`)
- **Fallback:** Mirror sites (163.com, zhihu.com, csdn.net)
- **Direct access fails:** WebFetch, Serper, Jina, Claude in Chrome all get CAPTCHA blocked

## Removed Tools

- **Google Search (direct API)** — Removed 2026-01-21. "Custom Search JSON API not enabled" error. Serper provides same Google results.

## Notes

- For Terry's use cases (AI news, job search), core tools are: **WebSearch + Perplexity + Serper**
- Exa worth keeping for code context
- Brave and Tavily are somewhat redundant but kept for specialized features (video search, crawling)
