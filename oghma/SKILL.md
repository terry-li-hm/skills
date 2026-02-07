---
name: oghma
description: Search AI coding memories from Claude Code, Codex, OpenClaw, OpenCode transcripts. "search memories"
---

# Oghma Memory Search

Search memories extracted from AI coding tool transcripts.

## MCP Tools (Claude Code, Codex — preferred when available)

Use these directly — no CLI needed:

| Tool | Purpose |
|------|---------|
| `oghma_search` | Search memories (keyword, vector, or hybrid mode) |
| `oghma_get` | Get a memory by ID |
| `oghma_stats` | Database statistics |
| `oghma_add` | Write a memory directly |
| `oghma_categories` | List categories with counts |

**Search modes:**
- `keyword` — FTS5 full-text search, ordered by recency
- `vector` — semantic similarity via embeddings
- `hybrid` (default) — RRF fusion of keyword + vector with recency boost

**Adding memories directly:**
```
oghma_add(content="insight here", category="gotcha", source_tool="manual")
```

## CLI (OpenClaw, OpenCode, or any shell)

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
