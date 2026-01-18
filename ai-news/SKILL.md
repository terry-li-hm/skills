---
name: ai-news
description: Check AI news sources for recent developments. Use when user says "ai news", "check ai news", "what's new in AI", or wants to catch up on AI developments.
---

# AI News Check

Fetch recent AI news from curated sources and summarize key developments. Quick scan for staying current without deep research.

## Trigger

Use when:
- User says "ai news", "check ai news", "what's new in AI"
- User wants to catch up on AI developments
- Interview prep needs talking points

## Inputs

- **mode** (optional): "quick" (Tier 1 only) | "deep" (all sources) | default is quick
- **smol_deep** (optional): Fetch last 3-5 full Smol AI issues for deep analysis

## Sources

Sources are defined in `sources.yaml` in this skill directory. Categories:
- **Web sources**: Blogs, newsletters (WebFetch)
- **Bank tech blogs**: Financial services AI (WebFetch)
- **Chinese sources**: 机器之心, 量子位, 新智元 (RSS)
- **X accounts**: @karpathy, @emollick, etc. (browser automation)
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

2. **Fetch X accounts** (browser automation):
   - All accounts from both tiers
   - Skip if user says "quick"

3. **YouTube videos** (Brave Video Search):
   - Search AI-related queries from `sources.yaml`
   - Pick 2-3 most relevant videos
   - Extract transcripts using youtube-transcript skill

4. **Apply stale filtering**: Skip sources with no articles <30 days old

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

## X Highlights
- **@karpathy:** [Recent post summary]

---
*Notable for your context:* [Relevance to AI/ML in banking, interview prep]
```

**Save to:** Append to `[[AI News Log]]` with date header

## Files

- Sources config: `/Users/terry/skills/ai-news/sources.yaml`
- This skill: `/Users/terry/skills/ai-news/SKILL.md`
