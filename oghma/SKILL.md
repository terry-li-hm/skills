---
name: oghma
description: Search AI coding memories from Claude Code, Codex, OpenCode transcripts. "search memories"
user_invocable: true
---

# Oghma Memory Search

Search memories extracted from AI coding tool transcripts via CLI.

## CLI Usage

**Search:**
```bash
oghma search "query" --mode hybrid --limit 5
oghma search "query" --category learning    # or: preference, project_context, gotcha, workflow
oghma search "query" --tool claude_code     # or: codex, opencode
```

**Status:**
```bash
oghma status
```

**Search modes:**
- `keyword` (default) — FTS5 full-text search, ordered by recency
- `vector` — semantic similarity via embeddings
- `hybrid` — RRF fusion of keyword + vector with recency boost (best quality)

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
- Prefer `--mode hybrid` for best results
