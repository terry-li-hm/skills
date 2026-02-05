---
name: oghma
description: Search AI coding memories extracted from Claude Code, Codex, OpenClaw, and OpenCode transcripts. Use when user asks "what did we learn about X", "search memories for Y", "do I have any gotchas about Z", or wants to recall past insights.
---

# Oghma Memory Search

Search memories extracted from AI coding tool transcripts.

## Commands

**Search memories:**
```bash
oghma search "query" --limit 10
```

**Filter by category:**
```bash
oghma search "query" --category learning    # or: preference, project_context, gotcha, workflow
```

**Filter by tool:**
```bash
oghma search "query" --tool claude_code     # or: codex, openclaw, opencode
```

**Check status:**
```bash
oghma status
```

**Export memories:**
```bash
oghma export --output-dir /path/to/dir --format markdown
```

## Categories

| Category | What it contains |
|----------|------------------|
| `learning` | Technical insights, how things work |
| `preference` | User preferences, style choices |
| `project_context` | Project-specific facts, people, dates |
| `gotcha` | Pitfalls, bugs, things that don't work as expected |
| `workflow` | Processes, commands, how to do things |

## Examples

```bash
# Find Python-related learnings
oghma search "python" --category learning

# Find interview context
oghma search "interview" --category project_context

# Find gotchas about a tool
oghma search "playwright" --category gotcha

# Search across all categories
oghma search "async"
```

## When to Use

- User asks "what did we discuss about X?"
- User wants to recall past insights or decisions
- User asks about gotchas or pitfalls
- Before starting work on a topic, check for relevant memories
