---
name: web-search
description: Reference for choosing the right web search tool. Not user-invocable — use as internal guidance when performing searches.
user_invocable: false
---

# Web Search Tool Selection Guide

Reference for choosing the optimal search tool. Updated 2026-02-13.

## Available Tools (Active)

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| **WebSearch** | Built-in | Free | General purpose, quick searches |
| **Perplexity CLI** | Bash script | $0.006–0.40/query | Deep research, reasoning |
| **Perplexity MCP** | MCP server | Same as CLI | Same, but no model control |
| **WebFetch** | Built-in | Free | Scrape specific URLs to markdown |

## Cost Tiers — Route by Budget

| Tier | Tool | Cost/query | Use When |
|------|------|------------|----------|
| **Free** | `WebSearch` | $0 | Default for everything |
| **Cheap** | `perplexity.sh search` | ~$0.006 | Need cited synthesis, WebSearch insufficient |
| **Mid** | `perplexity.sh ask` / `reason` | ~$0.01 | Structured surveys, complex reasoning |
| **Expensive** | `perplexity.sh research` | ~$0.40 | Deep novel research only. **Always ask before using.** |

**Default to free tier.** Only escalate when the cheaper tool genuinely can't answer.

## Use Case Routing

| Need | Tool | Why |
|------|------|-----|
| Quick answer / general search | `WebSearch` | Free, fast, no overhead |
| Structured survey ("list the platforms for X") | `perplexity.sh ask` | Concise, tabular, low fabrication |
| Deep analysis of novel questions | `perplexity.sh research` | Breadth + citations. **$0.40/query — confirm first** |
| Complex reasoning / trade-off analysis | `perplexity.sh reason` | Reasoning chain, best for hard questions |
| Verify claims / get primary sources | `WebSearch` | Returns links, no hallucinated synthesis |
| AI news | `WebSearch` | Free, sufficient for news |
| Scrape a specific URL | `WebFetch` | HTML → markdown with prompt |
| Code & documentation | Context7 plugin | Best for library docs |
| Job/company research | `WebSearch` → `perplexity.sh ask` | Free first, paid for depth |

## Perplexity CLI (`~/scripts/perplexity.sh`)

Lightweight bash wrapper around the Perplexity API. Replaces MCP for most uses.

```bash
# Modes and their models:
perplexity.sh search "query"    # sonar          ~$0.006
perplexity.sh ask "query"       # sonar-pro      ~$0.01
perplexity.sh reason "query"    # sonar-reasoning-pro ~$0.01
perplexity.sh research "query"  # sonar-deep-research ~$0.40 ← EXPENSIVE
```

**Advantages over MCP:** explicit model control, no npx startup, no running process, transparent cost.

**MCP is still available** for convenience (native tool calls vs Bash). Same models, same cost — but you can't pick sonar vs sonar-pro per request. MCP auto-routes: `perplexity_search`→sonar, `perplexity_ask`→sonar-pro, `perplexity_research`→sonar-deep-research, `perplexity_reason`→sonar-reasoning-pro.

## Perplexity Quality Notes

- **All Perplexity tools inherit search index bias.** If a vendor publishes 4+ SEO comparison articles, they'll dominate results. Cross-check with WebSearch.
- **Don't default to the most expensive tool.** `ask` > `research` for "what exists?" questions. Reserve `research` for "what does this mean?" questions.
- **Never cite Perplexity metrics without checking the underlying source.** Fabricated case studies with round numbers (75% decrease, 40% increase) are common.
- **`strip_thinking: true`** on MCP reasoning calls saves significant tokens.

## WebSearch (Built-in)

- Default for quick answers — fast, good summaries
- No cost, always available
- Returns links for verification

## WebFetch (Built-in)

- Fetches URL, converts HTML to markdown, processes with prompt
- 15-minute cache, handles redirects
- Falls back to Jina Reader or browser automation for complex pages

## WeChat Articles (mp.weixin.qq.com)

See the dedicated `wechat-article` skill.

## Removed Tools

- **Tavily** — Removed 2026-02-07. Replaced by WebFetch + Perplexity.
- **Serper** — Removed 2026-02-07. Redundant with WebSearch + Perplexity.
- **Exa** — Replaced by Context7 plugin + Perplexity.
- **Brave** — Rarely used unique features.

API keys preserved in `~/.secrets`. Re-enable if needed.
