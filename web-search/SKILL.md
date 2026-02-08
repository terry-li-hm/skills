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
| **WebFetch** | Built-in | Scrape specific URLs to markdown |

## Use Case Routing

| Need | Tool | Why |
|------|------|-----|
| Quick answer / general search | `WebSearch` | Fast, no MCP overhead |
| Structured survey ("list the platforms for X") | `perplexity_ask` | Concise, tabular, low fabrication risk |
| Deep analysis of novel questions | `perplexity_research` | Breadth + citations, but needs filtering |
| Complex reasoning / trade-off analysis | `perplexity_reason` | Reasoning chain, best for hard questions |
| Verify claims / get primary sources | `WebSearch` | Returns links, no hallucinated synthesis |
| AI news | `WebSearch` or `perplexity_search` | Both work, WebSearch is faster |
| Scrape a specific URL | `WebFetch` | HTML → markdown with prompt |
| Code & documentation | Context7 plugin or `perplexity_search` | Context7 preferred for library docs |
| Job search | `WebSearch` → `perplexity_search` | WebSearch first, Perplexity for depth |
| Company research | `perplexity_ask` or `perplexity_research` | Ask for overview, Research for deep dive |

## Tool Details

### WebSearch (Built-in)
- Default for quick answers — fast, good summaries
- No MCP overhead, always available

### Perplexity (MCP)
- `perplexity_search` — web search with excerpts
- `perplexity_ask` — conversational Q&A. **Best for structured surveys** (list platforms, compare options). ~80% signal, concise, low fabrication risk.
- `perplexity_research` — comprehensive deep research with citations. **Best for novel/deep questions** where breadth matters. ~40% signal — over-produces for simple surveys, ingests SEO content uncritically, round metrics from fabricated case studies pass through. Always filter output manually.
- `perplexity_reason` — complex analysis with reasoning chain

### Perplexity Quality Notes
- **All Perplexity tools inherit search index bias.** If a vendor publishes 4+ SEO comparison articles, they'll dominate results and skew recommendations. Cross-check with WebSearch.
- **Don't default to the most expensive tool.** `perplexity_ask` > `perplexity_research` for "what exists?" questions. Reserve Research for "what does this mean?" questions.
- **Never cite Perplexity metrics without checking the underlying source.** Fabricated case studies with round numbers (75% decrease, 40% increase) are common in its output.

### WebFetch (Built-in)
- Fetches URL, converts HTML to markdown, processes with prompt
- 15-minute cache, handles redirects
- Falls back to Jina Reader or browser automation for complex pages

## WeChat Articles (mp.weixin.qq.com)

See the dedicated `wechat-article` skill.

## Removed Tools

- **Tavily** — Content extraction, crawling, site mapping. Removed 2026-02-07. Replaced by WebFetch + Perplexity.
- **Serper** — Google search via API. Removed 2026-02-07. Redundant with WebSearch + Perplexity.
- **Exa** — Semantic search, code context. Replaced by Context7 plugin + Perplexity.
- **Brave** — Alternative search index, video/image/news. Rarely used unique features.

API keys preserved in backup. Re-enable commands in MEMORY.md if needed.
