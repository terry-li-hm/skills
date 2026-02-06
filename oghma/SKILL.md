---
name: oghma
description: Search AI coding memories extracted from Claude Code, Codex, OpenClaw, and OpenCode transcripts. Use when user asks "what did we learn about X", "search memories for Y", "do I have any gotchas about Z", or wants to recall past insights.
---

# Oghma Memory Search

Search memories extracted from AI coding tool transcripts.

## MCP Tools (Preferred)

Use these directly — no CLI needed:

| Tool | Purpose |
|------|---------|
| `oghma_search` | Search memories (keyword, vector, or hybrid mode) |
| `oghma_get` | Get a memory by ID |
| `oghma_stats` | Database statistics |
| `oghma_add` | Write a memory directly |
| `oghma_categories` | List categories with counts |

**Search modes:**
- `keyword` (default) — FTS5 full-text search, ordered by recency
- `vector` — semantic similarity via embeddings, with mild recency tiebreaker
- `hybrid` — RRF fusion of keyword + vector with recency boost (~1.5x for today, decaying)

**Adding memories directly:**
```
oghma_add(content="insight here", category="gotcha", source_tool="manual")
```

## CLI Commands

**Search:**
```bash
oghma search "query" --limit 10
oghma search "query" --category learning    # or: preference, project_context, gotcha, workflow
oghma search "query" --tool claude_code     # or: codex, openclaw, opencode
```

**Status:**
```bash
oghma status
```

## Categories

| Category | What it contains |
|----------|------------------|
| `learning` | Technical insights, how things work |
| `preference` | User preferences, style choices |
| `project_context` | Project-specific facts, people, dates |
| `gotcha` | Pitfalls, bugs, things that don't work as expected |
| `workflow` | Processes, commands, how to do things |

## When to Use

- User asks "what did we discuss about X?"
- User wants to recall past insights or decisions
- Before starting work on a topic, check for relevant memories
- After discovering something worth persisting, use `oghma_add`
