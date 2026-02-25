---
name: web-search
description: Reference for choosing the right web search tool. Not user-invocable — use as internal guidance when performing searches.
user_invocable: false
---

# Web Search Tool Selection Guide

Reference for choosing the optimal search tool. Updated 2026-02-23.

## Available Tools (Active)

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| **WebSearch** | Built-in | Free | General purpose, quick searches |
| **pplx** | Rust CLI | $0.006–0.40/query | Deep research, reasoning |
| **grok** | Python CLI | ~$0.02/query | X/Twitter search, real-time web |
| **WebFetch** | Built-in | Free | Scrape specific URLs to markdown |

## Cost Tiers — Route by Budget

| Tier | Tool | Cost/query | Use When |
|------|------|------------|----------|
| **Free** | `WebSearch` | $0 | Default for everything |
| **Cheap** | `pplx search` | ~$0.006 | Need cited synthesis, WebSearch insufficient |
| **Mid** | `pplx ask` / `pplx reason` / `grok` | ~$0.01–0.02 | Structured surveys, complex reasoning, X/Twitter |
| **Expensive** | `pplx research` | ~$0.40 | Deep novel research. Use freely when it adds value. |

**Default to free tier.** Only escalate when the cheaper tool genuinely can't answer.

## Use Case Routing

| Need | Tool | Why |
|------|------|-----|
| Quick answer / general search | `WebSearch` | Free, fast, no overhead |
| Structured survey ("list the platforms for X") | `pplx ask` | Concise, tabular, low fabrication |
| Deep analysis of novel questions | `pplx research` | Breadth + citations. ~$0.40/query |
| Complex reasoning / trade-off analysis | `pplx reason` | Reasoning chain, best for hard questions |
| Verify claims / get primary sources | `WebSearch` | Returns links, no hallucinated synthesis |
| Find specific content URLs (YouTube, podcast episodes, etc.) | `pplx search` | WebSearch doesn't index platform-internal pages well; pplx does |
| AI news / X/Twitter | `grok --x-only` → `grok` | Real-time X/Twitter data + web search via xAI API |
| Scrape a specific URL | `WebFetch` | HTML → markdown with prompt |
| Code & documentation | Context7 plugin | Best for library docs |
| Job/company research | `WebSearch` → `pplx ask` | Free first, paid for depth |

## pplx CLI

Rust CLI wrapping the Perplexity API. Source: `~/code/pplx`. Published on crates.io.

```bash
pplx search "query"     # sonar               ~$0.006
pplx ask "query"        # sonar-pro           ~$0.01
pplx reason "query"     # sonar-reasoning-pro ~$0.01
pplx research "query"   # sonar-deep-research ~$0.40 ← EXPENSIVE
pplx log                # last 20 queries
pplx log --stats        # cost summary by mode
```

**Flags:** `--raw` (JSON output), `--no-log` (skip logging).
**Log:** `~/.local/share/pplx/log.jsonl` — use `pplx log --stats` to assess cost over time.
**Fallback:** `~/scripts/perplexity.sh` (bash wrapper, same API, no logging).

Reasoning responses (`pplx reason`) strip `<think>` tags by default. Use `--raw` to preserve.

## grok CLI

Python script (`~/bin/grok`) wrapping xAI Responses API. Uses `grok-4-1-fast-reasoning` for web search, `grok-3-mini-fast` for plain LLM.

```bash
grok "query"                  # general web search       ~$0.02
grok --x-only "query"        # X/Twitter only            ~$0.02
grok --domain reddit.com "query"  # restrict to domain   ~$0.02
grok --no-search "query"     # plain LLM (no search)     ~$0.0002
grok --raw "query"           # raw JSON response
```

**Key feature:** `--x-only` restricts to `x.com` via `allowed_domains` — only way to search X/Twitter programmatically.
**Auth:** `XAI_API_KEY` in `~/.zshenv`.

### X/Twitter Search: grok vs bird

| Tool | Use When | Output |
|------|----------|--------|
| `grok --x-only "query"` | Sentiment/opinion synthesis, "what do people think of X" | AI-summarised answer from X posts |
| `bird search "query" -n 10 --plain` | Raw tweets, specific users, exact quotes | Raw tweet text with links |

**Default to `grok --x-only` for X/Twitter research.** It synthesises across many posts and surfaces patterns. Use `bird` when you need raw tweets (exact wording, photos, specific accounts) or to fetch a known user's timeline (`bird user-tweets <handle>`).

**Japanese keeb Twitter is a goldmine.** English Reddit/YouTube may have zero coverage for niche switches — Japanese X often has real user impressions, sound tests, and rankings. Search in Japanese when English comes up empty.

## Non-English Search — Match the Community's Language

**When English results are thin, search in the language of the community that actually uses the product/service.**

| Domain | Language | Example |
|--------|----------|---------|
| HK local (doctors, govt, restaurants) | Chinese (中文) | `pplx search "香港脊椎側彎骨科醫生推薦 私家 2026"` |
| Niche keeb switches/builds | Japanese (日本語) | `bird search "HMX K01 タクタイル" -n 10` |
| Taobao/Chinese products | Chinese (中文) | Reviews, Douyin/Bilibili content |
| K-beauty, Korean tech | Korean (한국어) | Naver blogs, Korean review sites |

**Pattern:** English first (free). If results are retailer copy or zero community discussion → re-search in the relevant language.

**HK product price search:** See `~/docs/solutions/hk-product-price-search.md`.

**LinkedIn people research:** See `linkedin-research` skill.

## Perplexity Quality Notes

- **All Perplexity tools inherit search index bias.** If a vendor publishes 4+ SEO comparison articles, they'll dominate results. Cross-check with WebSearch.
- **Route by question type.** `ask` for "what exists?" questions. `research` for "what does this mean?" or anything requiring depth. Cost is acceptable — use `research` freely when it adds value.
- **Never cite Perplexity metrics without checking the underlying source.** Fabricated case studies with round numbers (75% decrease, 40% increase) are common.

## WeChat Articles (mp.weixin.qq.com)

See the dedicated `wechat-article` skill.
