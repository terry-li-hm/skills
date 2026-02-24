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

English search is the default, but niche topics often have zero English coverage. **When English results are thin, search in the language of the community that actually uses the product/service.**

| Domain | Language | Why |
|--------|----------|-----|
| HK local services (doctors, restaurants, govt) | Chinese (中文) | Surfaces Sundaykiss, OpenRice, HK01, 親子王國 |
| Niche mechanical keyboard switches/builds | Japanese (日本語) | JP keeb Twitter has real impressions when Reddit/YouTube have nothing |
| Taobao/Chinese consumer products | Chinese (中文) | Reviews, comparisons, Douyin/Bilibili content |
| K-beauty, Korean tech | Korean (한국어) | Naver blogs, Korean review sites |

**Pattern:** Search English first (free). If results are retailer copy or zero community discussion → re-search in the relevant language.

**HK local example:** `pplx search "香港脊椎側彎骨科醫生推薦 私家 2026 口碑好"` returned 3 named doctors with fees and MTR exits — English query only found institutional websites.

**JP keeb example:** HMX K01 had zero Reddit/English reviews. `bird search "HMX K01 タクタイル" -n 10` surfaced real user rankings, sound test links, and comparisons from Japanese enthusiasts.

## HK Product Price Search — Search Retailers Directly

**Don't rely on aggregators alone.** price.com.hk has coverage gaps and stale prices. Search individual HK retailers by name for accurate stock + pricing:

| Retailer | Strength | URL |
|----------|----------|-----|
| **Yoho (友和)** | Electronics, competitive pricing, FPS discount | yohohongkong.com |
| **HKTVmall** | Broad catalog, fast delivery | hktvmall.com |
| **2000Fun** | PC hardware | openshop.com.hk |
| **豐澤 Fortress** | Official retail, reliable stock | fortress.com.hk |
| **百老匯 Broadway** | Electronics, appliances | broadway.com.hk |
| **price.com.hk** | Aggregator — check but don't stop here | price.com.hk |

**Pattern:** Simple query wins. `"WD Elements Desktop 12TB 香港"` finds Yoho instantly. Don't stuff queries with `site:` operators, multiple brands, price terms, and year — that dilutes results. Search **one product + one retailer** (or just + 香港) per query. Run parallel searches across 2-3 retailers instead of one mega-query.

## Perplexity Quality Notes

- **All Perplexity tools inherit search index bias.** If a vendor publishes 4+ SEO comparison articles, they'll dominate results. Cross-check with WebSearch.
- **Route by question type.** `ask` for "what exists?" questions. `research` for "what does this mean?" or anything requiring depth. Cost is acceptable — use `research` freely when it adds value.
- **Never cite Perplexity metrics without checking the underlying source.** Fabricated case studies with round numbers (75% decrease, 40% increase) are common.

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
- **Perplexity MCP** — Removed Feb 2026. Replaced by `pplx` CLI.

API keys preserved in `~/.secrets`. Re-enable if needed.
