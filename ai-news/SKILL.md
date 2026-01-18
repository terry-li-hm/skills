---
name: ai-news
description: Check AI news sources for recent developments. Use when user says "ai news", "check ai news", "what's new in AI", or wants to catch up on AI developments. Sources include Smol AI News (swyx), Simon Willison's blog, Evident Banking Brief (AI in financial services), Every (Dan Shipper), Hacker News, Import AI (Jack Clark), Chinese AI news (机器之心, 量子位, 新智元 via Wechat2RSS), bank tech blogs, YouTube videos (with transcript extraction), and X accounts (@karpathy, @dotey, @jerryjliu0, @danshipper, @ylecun, @emollick, @AndrewYNg, @EpochAIResearch).
---

# AI News Check

Fetch recent AI news from curated sources and summarize key developments. Quick scan for staying current without deep research.

## Fetch Strategy

**Tier 1 (Always fetch):** High-signal sources with frequent updates. ~20 sources, fast scan.

**Tier 2 (Deep scan only):** Fetch when user says "deep", "full", or "all sources". Slower, comprehensive.

**Stale filtering:** Skip sources returning only articles >30 days old. Note stale sources for future pruning.

**Quick mode:** When user says "quick", fetch Tier 1 web sources only (skip X, YouTube, Tier 2).

**Note:** Medium-hosted blogs (Wise, Revolut, Upstart, etc.) and JS-heavy sites (Stripe, Gradient Labs) don't work with WebFetch — demoted to Tier 2. Use browser automation in deep mode if needed.

## Sources

### Web (WebFetch)

| Source | URL | Focus | Tier |
|--------|-----|-------|------|
| Smol AI News | https://news.smol.ai | Practitioner-focused, swyx | 1 |
| Simon Willison | https://simonwillison.net | LLMs, open source, hands-on | 1 |
| Evident Banking Brief | https://evidentinsights.com/bankingbrief/ | AI in financial services | 2 |
| Every | https://every.to | AI business strategy, Dan Shipper | 2 |
| Hacker News | https://news.ycombinator.com | Tech/startup news, community picks | 2 |
| Import AI | https://jack-clark.net | AI research, policy, Jack Clark | 2 |
| Anthropic Blog | https://www.anthropic.com/news | Claude updates, research, safety | 1 |
| OpenAI Developer Blog | https://developers.openai.com/blog | Codex, APIs, developer guides | 1 |
| Eugene Yan | https://eugeneyan.com | Applied ML, RecSys, LLMs in production | 1 |
| Latent.Space | https://www.latent.space | AI practitioner podcast (swyx), deep dives | 2 |

### Bank Tech Blogs (WebFetch)

| Source | URL | Focus | Tier |
|--------|-----|-------|------|
| Layer 6 (TD Bank) | https://layer6.ai/blog | ML research, recommender systems, Toronto | 1 |
| Capital One Tech | https://www.capitalone.com/tech/machine-learning/ | ML in banking, MLOps, fraud | 2 |
| JPMorgan AI Research | https://www.jpmorgan.com/technology/artificial-intelligence | Finance AI, NLP, quant research | 2 |
| Goldman Sachs Insights | https://www.goldmansachs.com/insights/topics/artificial-intelligence.html | AI market analysis, enterprise AI | 2 |
| Monzo Tech | https://monzo.com/blog/topic/technology | ML platform, fraud, UK neobank | 1 |
| Nubank (Building) | https://building.nubank.com/data-science-machine-learning/ | ML ops, real-time ML, Brazil | 2 |
| Stripe Blog | https://stripe.com/blog | Payments ML, fraud detection, Radar | 2 |
| Klarna Engineering | https://engineering.klarna.com/tagged/machine-learning | BNPL risk ML, product classification | 2 |
| Gradient Labs | https://gradient-labs.ai/blog | AI agents for FS customer ops | 2 |
| DBS Tech Blog | https://medium.com/dbs-tech-blog | Singapore, AI-fuelled banking | 2 |
| Cash App AI | https://ai.cash.app | Block/Square ML, feature systems | 2 |
| Wise Engineering | https://medium.com/wise-engineering | 150+ ML models, fraud/AML | 2 |
| PayPal Tech | https://medium.com/paypal-tech/tagged/machine-learning | Fraud graph ML, sentiment | 2 |
| N26 Engineering | https://n26.com/en-eu/blog/topic/n26-engineering | German neobank | 2 |
| Affirm Tech | https://tech.affirm.com/tagged/machine-learning | BNPL credit ML, feature stores | 2 |
| Adyen Tech | https://medium.com/adyen/tagged/machine-learning | Payments fraud ML, risk scoring | 2 |
| Brex Tech | https://medium.com/brexeng | Corporate cards, GPT-4, Flink | 2 |
| Ramp Builders | https://builders.ramp.com | Corporate cards, Metaflow ML | 2 |
| ING Blog | https://medium.com/ing-blog | Dutch bank, AI engineering | 2 |
| Coinbase Engineering | https://www.coinbase.com/blog/landing/engineering | Crypto, EasyML, fraud | 2 |
| Robinhood Engineering | https://medium.com/robinhood-engineering | Trading, payments | 2 |
| Revolut Tech | https://medium.com/revolut/tagged/machine-learning | Fraud detection, Sherlock | 2 |
| Toast Technology | https://technology.toasttab.com | Restaurant fintech | 2 |
| Plaid Blog | https://plaid.com/blog | Open banking, MCP, infra | 1 |
| Mercury Eng Blog | https://mercury.com/blog/topics/engineering-blog | Startup banking | 2 |
| Checkout.com Tech | https://medium.com/checkout-com-techblog | Payments, dbt, fraud | 2 |
| Marqeta Engineering | https://medium.marqeta.com/tagged/engineering | Card issuing platform | 2 |
| Square Corner | https://developer.squareup.com/blog | MLOps, APIs, data science | 2 |
| Ripple Engineering | https://engineering.ripple.com | XRP, blockchain analytics | 2 |
| Wealthfront Eng | https://eng.wealthfront.com | Robo-advisor, data science | 2 |
| Betterment Eng | https://www.betterment.com/engineering | Robo-advisor, SLOs | 2 |
| Lemonade Blog | https://www.lemonade.com/blog | Insurtech, AI claims | 2 |
| BBVA AI Factory | https://www.bbvaaifactory.com/blog/ | Spanish bank, ML monitoring | 2 |
| GoCardless Blog | https://gocardless.com/blog | Direct debit, ML retries | 2 |
| Thought Machine | https://www.thoughtmachine.net/blog | Core banking, Kubernetes | 2 |
| 10x Banking Eng | https://www.10xbanking.com/engineering | Core banking, microservices | 2 |
| Tink Blog | https://tink.com/blog | Open banking (Visa) | 2 |
| Solaris Engineering | https://engineering.solarisbank.com | BaaS, Germany | 2 |
| Column Blog | https://column.com/blog | Developer-first bank | 2 |
| Lithic Blog | https://www.lithic.com/blog | Card issuing | 2 |
| Alloy Blog | https://www.alloy.com/blog | Identity, fraud prevention | 2 |
| Sardine Blog | https://www.sardine.ai/blog | Fraud ML, feature stores | 1 |
| Moov Blog | https://moov.io/blog | Payments platform | 2 |
| Modern Treasury | https://www.moderntreasury.com/topics/engineering | Payment ops, ledgers | 2 |
| Finix Blog | https://finix.com/resources/blogs | Embedded payments | 2 |
| Dwolla Blog | https://www.dwolla.com/updates | A2A payments | 2 |
| Stytch Eng Blog | https://stytch.com/blog/category/engineering | Identity, auth, AI agents | 2 |
| Persona Blog | https://withpersona.com/blog | Identity verification | 2 |
| Socure Tech Blog | https://www.socure.com/tech-blog | Identity verification ML | 2 |
| Sift Engineering | https://engineering.sift.com | Fraud detection, deep learning | 2 |
| Onfido Tech | https://medium.com/onfido-tech | Identity verification, biometrics ML | 2 |
| Forter Blog | https://www.forter.com/blog | E-commerce fraud prevention ML | 2 |
| Signifyd Blog | https://www.signifyd.com/blog | Fraud prevention, ML models | 2 |
| ComplyAdvantage Tech | https://technology.complyadvantage.com | AML, financial crime ML | 2 |
| Chainalysis Blog | https://www.chainalysis.com/blog | Crypto compliance, blockchain analytics | 1 |
| Elliptic Blog | https://www.elliptic.co/blog | Crypto compliance, blockchain forensics | 2 |
| TrueLayer Engineering | https://truelayer.com/blog/engineering/ | Open banking, payments API | 2 |
| ClearBank Tech | https://clear.bank/news-category/technology | UK clearing bank, API | 2 |
| Currencycloud Blog | https://blog.currencycloud.com | FX, cross-border payments | 2 |
| Modulr Blog | https://www.modulrfinance.com/blog-insights | UK B2B payments, API | 2 |
| Belvo Blog | https://belvo.com/blog | Open finance LATAM, API | 2 |
| Rapyd Blog | https://www.rapyd.net/blog | Global payments, fintech API | 2 |
| Zeta Engineering | https://www.zeta.tech/us/resources/engineering-blog/ | Core banking platform, cryptography | 2 |
| Galileo Blog | https://www.galileo-ft.com/blog | Card issuing, digital banking API | 2 |
| MX Blog | https://www.mx.com/blog | Financial data, open finance | 2 |
| Finicity Blog | https://www.finicity.com/category/blog | Open banking, Mastercard | 2 |
| Upstart Tech | https://medium.com/upstart-tech | AI lending, credit ML | 2 |
| SoFi Engineering | https://sofietyblog.sofi.com/tag/engineering | Neobank, fintech products | 2 |
| Blend Blog | https://blend.com/blog | Mortgage tech, AI origination | 2 |
| nCino Blog | https://www.ncino.com/blog | Bank cloud, lending AI | 2 |
| Plum Fintech | https://medium.com/plum-fintech | Savings app, UK fintech | 2 |
| Temenos Blog | https://www.temenos.com/blogs | Core banking, AI transformation | 2 |

### Chinese AI News (RSS via Wechat2RSS)

| Source | RSS URL | Focus | Tier |
|--------|---------|-------|------|
| 机器之心 (Synced) | https://wechat2rss.xlab.app/feed/51e92aad2728acdd1fda7314be32b16639353001.xml | AI research, industry news (CN) | 1 |
| 量子位 (QbitAI) | https://wechat2rss.xlab.app/feed/7131b577c61365cb47e81000738c10d872685908.xml | AI startups, products, China scene (CN) | 1 |
| 新智元 | https://wechat2rss.xlab.app/feed/ede30346413ea70dbef5d485ea5cbb95cca446e7.xml | AI news, Western research translations (CN) | 2 |

### X/Twitter (browser automation)

| Account | Handle | Focus | Tier |
|---------|--------|-------|------|
| Dotey | @dotey | AI tutorials, Chinese AI scene | 2 |
| Dan Shipper | @danshipper | AI for knowledge work, Every | 2 |
| Jerry Liu | @jerryjliu0 | LlamaIndex, RAG, agents | 2 |
| Andrej Karpathy | @karpathy | Deep learning, AI education | 1 |
| Andrew Ng | @AndrewYNg | The Batch, DeepLearning.AI | 2 |
| Yann LeCun | @ylecun | Meta AI Chief, contrarian takes | 2 |
| Ethan Mollick | @emollick | AI + work/productivity, Wharton | 1 |
| Epoch AI | @EpochAIResearch | AI compute, research trends, trajectory | 2 |
| Eugene Yan | @eugeneyan | Applied ML, RecSys, Amazon, practical AI | 1 |


### YouTube Videos (Brave Video Search + Transcript)

Search for recent AI-related videos and extract transcripts for deeper insights. Skip if user says "quick".

**Search queries:**
- `AI agents 2026`
- `LLM enterprise applications`
- `AI in banking fintech`
- `machine learning production`

**Transcript extraction:** Use `youtube-transcript-api` Python package:
```python
from youtube_transcript_api import YouTubeTranscriptApi
ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id, languages=['en'])
full_text = ' '.join([snippet.text for snippet in transcript])
```

**Selection criteria:**
- Recent uploads (within last month)
- High view count or from reputable channels (a16z, Google, IBM, etc.)
- Relevant to AI/ML in enterprise or banking

## Workflow

### Quick mode (default)
Fetch Tier 1 sources only (~20 sources, fast):

1. **Tier 1 Web sources** (parallel WebFetch):
   - General: Smol AI News, Simon Willison, Eugene Yan, Anthropic Blog, OpenAI Developer Blog
   - Bank Tech: Layer 6, Monzo, Plaid, Sardine, Chainalysis
   - Chinese AI: 机器之心, 量子位

2. **Tier 1 X sources** (browser automation):
   - @karpathy, @emollick, @eugeneyan
   - Skip if user says "quick"

3. **Extract & output:**
   - Last 3-5 articles from each source
   - Title, date, one-line summary
   - Highlight relevance to AI/ML in banking

### Deep mode (user says "deep", "full", or "all sources")
Fetch all Tier 1 + Tier 2 sources:

1. **All Web sources** (parallel WebFetch):
   - All sources from both tiers
   - Apply stale filtering: skip sources with no articles <30 days old

2. **All X sources** (browser automation):
   - All accounts from both tiers

3. **YouTube videos** (Brave Video Search):
   - Use `mcp__brave-search__brave_video_search` with AI-related queries
   - Pick 2-3 most relevant/popular videos
   - Extract transcripts using `youtube-transcript-api`

4. **Extract & output:**
   - Full summary organized by source category
   - Note any stale sources for future pruning

### Always
- **Save to vault**: Append to `[[AI News Log]]` with date header
- **Track stale sources**: Note sources with no recent updates for review

## Output Format

```
## Smol AI News (swyx)
- **[Title]** (Date) — One-line summary

## Simon Willison
- **[Title]** (Date) — One-line summary

## Evident Banking Brief
- **[Title]** (Date) — One-line summary

## Every (Dan Shipper)
- **[Title]** (Date) — One-line summary

## Hacker News
- **[Title]** — One-line summary (top AI-related posts)

## Import AI (Jack Clark)
- **[Title]** (Date) — One-line summary

## Anthropic Blog
- **[Title]** (Date) — One-line summary

## OpenAI Blog
- **[Title]** (Date) — One-line summary

## Bank Tech Blogs
### Layer 6 (TD Bank)
- **[Title]** (Date) — One-line summary

### Capital One Tech
- **[Title]** (Date) — One-line summary

### JPMorgan AI Research
- **[Title]** (Date) — One-line summary

### Goldman Sachs Insights
- **[Title]** (Date) — One-line summary

### Monzo Tech
- **[Title]** (Date) — One-line summary

### Nubank (Building)
- **[Title]** (Date) — One-line summary

### Stripe Blog
- **[Title]** (Date) — One-line summary

### Klarna Engineering
- **[Title]** (Date) — One-line summary

### Gradient Labs
- **[Title]** (Date) — One-line summary

### DBS Tech Blog
- **[Title]** (Date) — One-line summary

### Cash App AI
- **[Title]** (Date) — One-line summary

### Wise Engineering
- **[Title]** (Date) — One-line summary

### PayPal Tech
- **[Title]** (Date) — One-line summary

### N26 Engineering
- **[Title]** (Date) — One-line summary

### Affirm Tech
- **[Title]** (Date) — One-line summary

### Adyen Tech
- **[Title]** (Date) — One-line summary

### Brex Tech
- **[Title]** (Date) — One-line summary

### Ramp Builders
- **[Title]** (Date) — One-line summary

### ING Blog
- **[Title]** (Date) — One-line summary

### Coinbase Engineering
- **[Title]** (Date) — One-line summary

### Robinhood Engineering
- **[Title]** (Date) — One-line summary

### Revolut Tech
- **[Title]** (Date) — One-line summary

### Toast Technology
- **[Title]** (Date) — One-line summary

### Plaid Blog
- **[Title]** (Date) — One-line summary

### Mercury Eng Blog
- **[Title]** (Date) — One-line summary

### Checkout.com Tech
- **[Title]** (Date) — One-line summary

### Marqeta Engineering
- **[Title]** (Date) — One-line summary

### Square Corner
- **[Title]** (Date) — One-line summary

### Ripple Engineering
- **[Title]** (Date) — One-line summary

### Wealthfront Eng
- **[Title]** (Date) — One-line summary

### Betterment Eng
- **[Title]** (Date) — One-line summary

### Lemonade Blog
- **[Title]** (Date) — One-line summary

### BBVA AI Factory
- **[Title]** (Date) — One-line summary

### GoCardless Blog
- **[Title]** (Date) — One-line summary

### Thought Machine
- **[Title]** (Date) — One-line summary

### 10x Banking Eng
- **[Title]** (Date) — One-line summary

### Tink Blog
- **[Title]** (Date) — One-line summary

### Solaris Engineering
- **[Title]** (Date) — One-line summary

### Column Blog
- **[Title]** (Date) — One-line summary

### Lithic Blog
- **[Title]** (Date) — One-line summary

### Alloy Blog
- **[Title]** (Date) — One-line summary

### Sardine Blog
- **[Title]** (Date) — One-line summary

### Moov Blog
- **[Title]** (Date) — One-line summary

### Modern Treasury
- **[Title]** (Date) — One-line summary

### Finix Blog
- **[Title]** (Date) — One-line summary

### Dwolla Blog
- **[Title]** (Date) — One-line summary

### Stytch Eng Blog
- **[Title]** (Date) — One-line summary

### Persona Blog
- **[Title]** (Date) — One-line summary

### Socure Tech Blog
- **[Title]** (Date) — One-line summary

### Sift Engineering
- **[Title]** (Date) — One-line summary

### Onfido Tech
- **[Title]** (Date) — One-line summary

### Forter Blog
- **[Title]** (Date) — One-line summary

### Signifyd Blog
- **[Title]** (Date) — One-line summary

### ComplyAdvantage Tech
- **[Title]** (Date) — One-line summary

### Chainalysis Blog
- **[Title]** (Date) — One-line summary

### Elliptic Blog
- **[Title]** (Date) — One-line summary

### TrueLayer Engineering
- **[Title]** (Date) — One-line summary

### ClearBank Tech
- **[Title]** (Date) — One-line summary

### Currencycloud Blog
- **[Title]** (Date) — One-line summary

### Modulr Blog
- **[Title]** (Date) — One-line summary

### Belvo Blog
- **[Title]** (Date) — One-line summary

### Rapyd Blog
- **[Title]** (Date) — One-line summary

### Zeta Engineering
- **[Title]** (Date) — One-line summary

### Galileo Blog
- **[Title]** (Date) — One-line summary

### MX Blog
- **[Title]** (Date) — One-line summary

### Finicity Blog
- **[Title]** (Date) — One-line summary

### Upstart Tech
- **[Title]** (Date) — One-line summary

### SoFi Engineering
- **[Title]** (Date) — One-line summary

### Blend Blog
- **[Title]** (Date) — One-line summary

### nCino Blog
- **[Title]** (Date) — One-line summary

### Plum Fintech
- **[Title]** (Date) — One-line summary

### Temenos Blog
- **[Title]** (Date) — One-line summary

## Chinese AI News (中文)
### 机器之心 (Synced)
- **[Title]** (Date) — One-line summary

### 量子位 (QbitAI)
- **[Title]** (Date) — One-line summary

### 新智元
- **[Title]** (Date) — One-line summary

## YouTube Insights
- **[Video Title]** (Channel) — Key insight or quote from transcript

## X Highlights
- **@AndrewYNg:** [The Batch / recent post]
- **@karpathy:** [Recent post summary]
- **@jerryjliu0:** [Recent post summary]
- **@danshipper:** [Recent post summary]
- **@dotey:** [Recent post summary]
- **@ylecun:** [Recent post summary]
- **@emollick:** [Recent post summary]
- **@EpochAIResearch:** [Recent post summary]

---
*Notable for your context:* [Relevance to AI/ML in banking, interview prep, etc.]
```

## Edge Cases

**Site unreachable:** Report error, continue with other sources

**Paywall/login:** Report and skip — these are public newsletters

**Too much content:** Limit to 5 most recent per source, summarize aggressively
