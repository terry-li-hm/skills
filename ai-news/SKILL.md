---
name: ai-news
description: Check AI news sources for recent developments. Use when user says "ai news", "check ai news", "what's new in AI", or wants to catch up on AI developments.
user_invocable: true
---

# AI News Check

Conversational AI news — read the log, synthesize, discuss. Depth adapts automatically based on how long it's been since last discussion.

## Trigger

Use when:
- User says "ai news", "check ai news", "what's new in AI"
- User wants to relax with some reading
- "anything interesting today?"

## Lens: AI Solution Lead at Capco

Terry is joining Capco as Principal Consultant / AI Solution Lead, advising bank clients. Frame news through:
- **Banking/fintech relevance:** What matters for AI in financial services?
- **Consulting talking points:** What should Capco clients know about?
- **Governance & regulatory:** What are regulators saying?
- **Perspective diversity:** How do different voices frame the same development?

## Architecture

**Cron** (silent index builder, 6:30 PM HKT daily, `lustro fetch`):
- Fetches **all sources** (Tier 1 + Tier 2) + **X accounts** via `bird --json`, cadence-gated — **zero LLM tokens**
- Tier controls **display priority**, not fetch: Tier 1 always surfaced, Tier 2 mentioned only if noteworthy or in deep mode
- Date-based + title-prefix dedup, cadence-aware skipping
- Appends delta to `[[AI News Log]]` (`~/notes/AI News Log.md`)
- State in `~/.cache/lustro/state.json`
- Log auto-rotates at 500 lines → `AI News Log - Archive YYYY-MM.md`
- Config: `~/.config/lustro/sources.yaml` + `~/.config/lustro/config.yaml`
- Health check: `lustro check`

**`/ai-news`** (pull-based, conversational):
- Terry asks whenever he feels like it
- Claude reads the log, adapts depth, discusses

## Workflow

### Step 1: Check the log

Read `[[AI News Log]]` — look for `<!-- Last discussed: YYYY-MM-DD -->` marker near the top. This is the reliable way to determine light vs weekly mode. If the marker is missing, fall back to eyeballing dates of entries.

### Step 2: Adapt depth automatically

**Light mode** (last discussion <3 days ago):
- Scan log entries since last discussion
- Highlight the **5 most significant items**. More sources = better selection, not longer output.
- Brief, conversational: "Simon Willison had a good post on X, and Jack Clark's take on Y is worth knowing about"
- Offer to go deeper on anything that catches Terry's eye
- This is relaxed evening reading, not a briefing

**Weekly synthesis** (last discussion 5+ days ago):
- Read all log entries from the past week
- Identify cross-source patterns (if Import AI AND Interconnects mention X → signal)
- Synthesize **3-5 key themes** with perspective from different sources. More items in the log means sharper curation, not more themes.
- Flag 1-2 articles genuinely worth reading in full ("read this one yourself" + link)
- Note what's relevant for Capco/banking context

**Staleness note:** If the cron log has no entries from the last 2 days, mention it — the cron may have failed. Fall back to live WebFetch for a few key sources.

### Step 3: Discuss

This is the actual value. Not a dump of headlines — a conversation:
- Terry asks follow-up questions
- Claude explains implications, connects to Terry's context
- If Terry wants to go deep on an article, Claude WebFetches it live and discusses

### Step 4: Update marker + log (optional)

**Always** update the discussion marker at the top of the log:
```
<!-- Last discussed: 2026-02-24 -->
```
Place it on the line after `# AI News Log`. Create or replace the existing marker.

Only if the discussion surfaced something worth preserving:
- Append a brief synthesis to `[[AI News Log]]` with discussion date
- Don't log if it was just a light chat

## Sources

Defined in `~/.config/lustro/sources.yaml`. Key high-signal sources for perspective:
- **Import AI** (Jack Clark) — policy + research framing, weekly
- **Interconnects** (Nathan Lambert) — scaling, alignment, "what's next", 2x/week
- **Simon Willison** — hands-on LLM practitioner, daily
- **机器之心 / 量子位** — Chinese AI ecosystem, daily
- **Bank tech blogs** (Layer 6, Sardine, Plaid) — peer patterns, biweekly/weekly

Full source list with cadence and RSS URLs in `~/.config/lustro/sources.yaml`.

## Paywalled Sources (Latent Space / Substack)

Terry has a paid Latent Space subscription. Browser profile is authenticated.

**Latent Space AINews** is the same digest as `news.smol.ai` but with editorial framing (cross-source narrative, key voices like Karpathy/Brockman, "why this matters" context). Prefer it over smol.ai when fetching live.

To fetch full paywalled articles:
```bash
# Open with authenticated profile
agent-browser --profile open "https://www.latent.space/p/<slug>"
# Extract full text
agent-browser eval "document.querySelector('article').innerText"
```

WebFetch will only get the free portion (~25% of content). Always use `agent-browser --profile` for Latent Space.

## WeChat Articles

WeChat 公众号 (e.g. 机器之心, 量子位, 歸藏的AI工具箱) are major Chinese AI commentary sources. To extract:

```bash
# Extract text only
summarize "https://mp.weixin.qq.com/s/ARTICLE_ID" --extract-only --model anthropic/claude-sonnet-4

# With summary
summarize "https://mp.weixin.qq.com/s/ARTICLE_ID" --model anthropic/claude-sonnet-4
```

Works because `summarize` uses a Chrome User-Agent that bypasses WeChat's CAPTCHA. See `content-fetch` skill for details.

## Deep Mode

When user says "deep", "full", "all sources":
- Surface **all** log entries (Tier 1 + Tier 2), not just Tier 1 highlights
- Verify X account coverage in cron log (now fetched by cron daily)
- WeChat articles via `summarize` CLI (live fetch, bypasses CAPTCHA)
- See `~/.config/lustro/sources.yaml` for full list

### Deep Mode Checklist

**1. Cron log** — review ALL entries since last discussion (Tier 1 + Tier 2 + X accounts)

**2. X accounts** — cron now fetches these daily via `bird --json`. Check log for `X:` prefixed entries. If any are missing (bird auth expired, rate limit), live fetch:
```bash
bird user-tweets <handle> -n 5 --plain
```
Tier 1: `@karpathy`, `@steipete`, `@emollick`, `@eugeneyan`
Tier 2: `@brendangregg`, `@rauchg`, `@shl`, `@atroyn`, `@dotey`, `@danshipper`, `@jerryjliu0`, `@AndrewYNg`, `@ylecun`, `@EpochAIResearch`, `@_philschmid`, `@axtonliu`, `@svpino`, `@morganhousel`, `@shaneparrish`, `@benjaminwfelix`

**3. X Discovery review** — check `### X Discovery (For You)` section in log. Interesting new handles → add to `~/.config/lustro/sources.yaml` x_accounts. Keywords configurable in `sources.yaml` `x_discovery` section.

**4. WeChat articles:**
- WeWe RSS feeds are in the cron (`localhost:4000`) — check log entries
- Ad-hoc extraction: `summarize "https://mp.weixin.qq.com/s/ID" --model anthropic/claude-sonnet-4`
- WeChat search: WebSearch with `site:mp.weixin.qq.com/s/` queries (see `sources.yaml` `wechat_search` section)

**5. Parallelise** — use background agents for independent sweeps:
- Missing X accounts not in cron log
- WeChat search queries (3-5 queries from sources.yaml)
- Any stale RSS feeds the cron might have missed

### Coverage Report

After deep mode, briefly report what was checked:
- How many cron log sources had entries since last discussion
- How many X accounts had entries vs needed live fetch
- WeChat/WeWe coverage
- Any sources intentionally skipped and why

This prevents the "did we really check all sources?" question.

## Monthly Thematic Digest

Monthly evidence-grounded synthesis of AI developments. Reads archived article full text from the cron's article cache and clusters by theme.

```bash
lustro digest                    # Current month
lustro digest --month 2026-02    # Specific month
lustro digest --dry-run           # Preview themes only
lustro digest --themes 5          # Limit to 5 themes
```

**Pipeline:**
1. Loads archived Tier 1 articles (full text) + AI News Log headlines
2. Pass 1: Theme identification via Gemini Flash (~5-8 clusters)
3. Pass 2: Per-theme evidence synthesis (claims, quotes, echo count, banking implications)
4. Writes to `~/notes/AI & Tech/YYYY-MM AI Thematic Digest.md`

**Prerequisites:** Cron must have run with article archival enabled (default). Check `~/.cache/lustro/articles/` for cached articles.

**Cost:** ~$0.05-0.15/month at Gemini Flash rates.

## Files

- Package source: `~/code/lustro` ([GitHub](https://github.com/terry-li-hm/lustro))
- Sources config: `~/.config/lustro/sources.yaml`
- App config: `~/.config/lustro/config.yaml`
- Log: `~/notes/AI News Log.md`
- Article cache: `~/.cache/lustro/articles/`
- State: `~/.cache/lustro/state.json`
- LaunchAgent: `~/agent-config/launchd/com.terry.ai-news-daily.plist`
