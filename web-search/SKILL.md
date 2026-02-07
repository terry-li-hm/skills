---
name: web-search
description: Reference for choosing the right web search tool. Not user-invocable — use as internal guidance when performing searches.
user_invocable: false
---

# Web Search Tool Selection Guide

Reference for choosing the optimal search tool. Updated 2026-02-07.

## Available Tools (Active)

| Tool | Type | Best For |
|------|------|----------|
| **WebSearch** | Built-in | General purpose, quick searches |
| **Perplexity** | MCP | Deep research, reasoning, AI news |
| **Tavily** | MCP | Content extraction, crawling, site mapping |

## Use Case Routing

| Need | Tool |
|------|------|
| Quick answer / general search | `WebSearch` (built-in) |
| AI news | `WebSearch` or `perplexity_search` |
| Deep research with citations | `perplexity_research` |
| Complex analysis / reasoning | `perplexity_reason` |
| Scrape a specific URL | `tavily_extract` |
| Crawl a website | `tavily_crawl` / `tavily_map` |
| Code & documentation | Context7 plugin or `perplexity_search` |
| Job search | `WebSearch` → `perplexity_search` |
| Company research | `perplexity_research` |

## Tool Details

### WebSearch (Built-in)
- Default for quick answers — fast, good summaries
- No MCP overhead, always available

### Perplexity (MCP)
- `perplexity_search` — web search with excerpts
- `perplexity_ask` — conversational Q&A
- `perplexity_research` — comprehensive deep research with citations
- `perplexity_reason` — complex analysis with reasoning chain

### Tavily (MCP)
- `tavily_search` — general web search
- `tavily_extract` — scrape specific URLs to markdown
- `tavily_crawl` — crawl site with depth/breadth control
- `tavily_map` — map site structure (URL discovery)
- `tavily_research` — multi-source research

## WeChat Articles (mp.weixin.qq.com)

See the dedicated `wechat-article` skill.

## Removed Tools (2026-02-07)

- **Serper** — Google search via API. Redundant with WebSearch + Perplexity.
- **Exa** — Semantic search, code context. Replaced by Context7 plugin + Perplexity.
- **Brave** — Alternative search index, video/image/news. Rarely used unique features.

API keys preserved in backup. Reinstall from `~/.claude.json.backup.*` if needed.
