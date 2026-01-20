# Web Search Skill

Use this skill when performing web searches.

## Search Tool Priority

When searching the web, use tools in this order:

1. **Google** (`mcp__google-search__search`) — Best result quality, use as default for general searches
2. **Google Read** (`mcp__google-search__read_webpage`) — To extract content from URLs found via Google
3. **Brave News** (`mcp__brave-search__brave_news_search`) — Only for recent news specifically (last 24h-7d)
4. **Tavily** (`mcp__tavily__tavily-search`) — Only when deep content extraction needed (`search_depth: advanced`)

Avoid defaulting to Tavily/Brave for general searches when Google is available.

## When to Use Each

### Google (Default)
- General information searches
- Company/product research
- Technical documentation
- Job listings
- Local Hong Kong searches (use Chinese/Cantonese keywords for better results)

### Brave News
- Breaking news (last 24 hours)
- Recent events (last week)
- News-specific queries

### Tavily
- When you need to extract and analyze full page content
- Deep research requiring `search_depth: advanced`
- When Google results need more context

## Hong Kong Local Searches

For Hong Kong local searches (restaurants, activities, places), use Chinese/Cantonese keywords for better results:
- "柴灣遊戲室" instead of "Chai Wan playhouse"
- "銅鑼灣餐廳" instead of "Causeway Bay restaurant"
