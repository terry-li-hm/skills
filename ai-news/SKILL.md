---
name: ai-news
description: Check AI news sources for recent developments. Use when user says "ai news", "check ai news", "what's new in AI", or wants to catch up on AI developments.
user_invocable: true
---

# AI News Check

Fetch recent AI news from curated sources and summarize key developments. Quick scan for staying current without deep research.

## Trigger

Use when:
- User says "ai news", "check ai news", "what's new in AI"
- User wants to catch up on AI developments
- Interview prep needs talking points

## Default Lens: Capco Principal Consultant

Terry is a Principal Consultant, AI Solution Lead at Capco. Frame AI news through this lens:
- **Governance & regulatory:** What are banks struggling to comply with?
- **Client advisory angle:** What would you tell a bank CRO/CTO?
- **Competitive landscape:** What are other consultancies saying?
- **Gaps:** Where is adoption outpacing oversight?

Always include governance-focused web searches alongside regular sources:
- "AI governance financial services banking [year]"
- "HKMA GenAI regulation" (for HK context)
- "site:capco.com AI" (know your employer's positions)

## Inputs

- **mode** (optional): "quick" (Tier 1 only) | "deep" (all sources) | default is quick
- **smol_deep** (optional): Fetch last 3-5 full Smol AI issues for deep analysis

## Sources

Sources are defined in `sources.yaml` in this skill directory. Categories:
- **Web sources**: Blogs, newsletters (WebFetch)
- **Bank tech blogs**: Financial services AI (WebFetch)
- **Chinese sources**: 机器之心, 量子位, 新智元 (RSS)
- **X accounts**: @karpathy, @emollick, etc. (via `bird` CLI)
- **YouTube**: Video search + transcript extraction

**Tier 1**: Always fetch (~15 sources, fast)
**Tier 2**: Deep scan only (~50+ sources, comprehensive)

## Workflow

### Quick Mode (default)

1. **Load sources** from `sources.yaml`, filter to Tier 1

2. **Fetch web sources in parallel** (WebFetch):
   - Smol AI News, Simon Willison, Eugene Yan
   - Anthropic Blog, OpenAI Developer Blog
   - Layer 6, Monzo, Plaid, Sardine, Chainalysis
   - 机器之心, 量子位 (RSS)

3. **Extract & summarize**:
   - Last 3-5 articles from each source
   - Title, date, one-line summary
   - Highlight relevance to AI/ML in banking

4. **Output to chat** + append to `[[AI News Log]]` in vault

### Deep Mode (user says "deep", "full", "all sources")

1. **Fetch all Tier 1 + Tier 2 sources**

2. **Fetch X accounts** (via `bird` CLI — portable):
   ```bash
   bird user-tweets karpathy -n 5 --cookie-source chrome
   bird user-tweets emollick -n 5 --cookie-source chrome
   ```
   - All accounts from both tiers
   - Skip if user says "quick"
   - See `/x-twitter` skill for full CLI reference

3. **YouTube videos** (Brave Video Search):
   - Search AI-related queries from `sources.yaml`
   - Pick 2-3 most relevant videos
   - Extract transcripts using youtube-transcript skill

4. **WeChat scan** (Chinese practitioner content):
   - WebSearch with `site:mp.weixin.qq.com/s/` queries from `sources.yaml`
   - Filter to short URLs only (format: `/s/ABC123`)
   - Extract via `wechat.imagenie.us/extract` API
   - Limit to 5 articles to avoid rate limits
   - See `wechat-article` skill for full extraction details

5. **Apply stale filtering**: Skip sources with no articles <30 days old

### Smol AI Deep Read

When user says "smol deep" or "full smol":
- Fetch last 3-5 full issues from `news.smol.ai/issues/YY-MM-DD-slug`
- Full issues contain: swyx's analysis, community insights, technical highlights, smaller stories

## Error Handling

- **If site unreachable**: Report error, continue with other sources
- **If paywall/login required**: Report and skip
- **If too much content**: Limit to 5 most recent per source
- **If source stale (>30 days)**: Note for future pruning

## Output

```markdown
## Smol AI News (swyx)
- **[Title]** (Date) — One-line summary

## Simon Willison
- **[Title]** (Date) — One-line summary

## Bank Tech Blogs
### Layer 6 (TD Bank)
- **[Title]** (Date) — One-line summary

## Chinese AI News (中文)
### 机器之心 (Synced)
- **[Title]** (Date) — One-line summary

## WeChat Articles (微信公众号) [Deep mode only]
- **[Title]** — One-line summary
- **[Title]** — One-line summary

## X Highlights
- **@karpathy:** [Recent post summary]

---
*Notable for your context:* [Relevance to AI/ML in banking, interview prep]
```

**Save to:** Append to `[[AI News Log]]` with date header

## Files

- Sources config: `sources.yaml` (in this skill directory)
- Related: `/x-twitter` skill for X account fetching
