# Web Search Skill

Use this skill when performing web searches.

## Search Tool Selection

| Tool | Best For | Output |
|------|----------|--------|
| **Built-in WebSearch** | Quick factual answers | Synthesized summary + source URLs |
| **Brave Search** | Raw rankings, snippets, news | Title + description snippets |
| **Tavily** | Deep research, full content | Extracted page content |

## When to Use Each

### Built-in WebSearch (Default for Facts)
- Quick factual questions ("When was X released?")
- General information lookups
- When you want a pre-synthesized answer with sources
- Fast, single-call answers

### Brave Search
- **`brave_web_search`** — Raw search results when you need to see what's ranking
- **`brave_news_search`** — Breaking news (last 24h-7d), recent events
- **`brave_video_search`** — Finding videos on a topic
- **`brave_image_search`** — Finding images
- **`brave_local_search`** — Local businesses (requires Pro plan)

### Tavily
- **`tavily-search`** — When you need actual page content, not just snippets
  - Use `search_depth: "advanced"` for thorough research
  - Use `topic: "news"` for news-specific searches
- **`tavily-extract`** — Extract content from specific URLs
- **`tavily-crawl`** — Map and crawl entire sites
- Best for research requiring full context analysis

### Google Search (Currently Broken)
- `mcp__google-search__search` returns API access error
- Skip until API is configured

## Hong Kong Local Searches

For Hong Kong local searches (restaurants, activities, places), use Chinese/Cantonese keywords for better results:
- "柴灣遊戲室" instead of "Chai Wan playhouse"
- "銅鑼灣餐廳" instead of "Causeway Bay restaurant"

## Search Strategy

1. **Single fact needed?** → Built-in WebSearch
2. **Need to see raw results?** → Brave
3. **Need full page content?** → Tavily with `search_depth: "advanced"`
4. **News specifically?** → Brave News or Tavily with `topic: "news"`
5. **Multiple sources to compare?** → Tavily extract on specific URLs
