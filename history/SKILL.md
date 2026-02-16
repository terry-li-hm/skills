---
name: history
description: Scan and search chat history with proper HKT timezone handling. Use when reviewing what was discussed on a specific day or searching for past conversations.
user_invocable: true
---

# History

Search AI coding chat history from Claude Code, Codex, and OpenCode.

## Tools

- **`resurface`** (Rust CLI, `~/.cargo/bin/resurface`) — programmatic date scan, keyword search, deep transcript search, cross-tool support (Claude + Codex + OpenCode), HKT day boundaries. Works from Claude Code (non-interactive). Source: `~/code/resurface/`.
- **`claude-history`** (Rust CLI) — interactive TUI fuzzy search over Claude Code conversations. Best for browsing or resuming a session. **Requires interactive terminal** — won't work from Claude Code's Bash tool.

## Trigger

- `/history` — today's prompts across all tools
- `/history yesterday` — yesterday's prompts
- `/history 2026-01-18` — specific date
- `/history --tool=Codex` — filter by specific tool
- `/history search self-intro` — search prompts for keyword (last 7 days)
- `/history search DBS --deep` — search full transcripts (user + assistant)
- `/history search DBS --days=30` — search last 30 days
- `/history browse` — launch claude-history TUI (interactive fuzzy search)
- `/history browse --global` — search all projects at once

## resurface (Programmatic — use from Claude Code)

```bash
# --- Date scan mode ---
resurface                          # Today's prompts (last 50)
resurface yesterday                # Yesterday's prompts
resurface 2026-01-23               # Specific date
resurface --full                   # Show all prompts (not just last 50)
resurface --json                   # Output as JSON
resurface --tool Claude            # Filter by tool

# --- Search mode (prompts only — fast) ---
resurface search "self-intro"                  # Last 7 days
resurface search "DBS" --days=30               # Last 30 days
resurface search "DBS" --tool Claude           # Filter by tool

# --- Search mode (full transcripts — user + assistant, parallel with rayon) ---
resurface search "self-intro" --deep           # Last 7 days
resurface search "DBS" --deep --days=30        # Last 30 days
```

## claude-history (Interactive TUI — use from terminal)

```bash
claude-history                     # Interactive fuzzy search (current project)
claude-history --global            # Search all projects
claude-history --resume            # Resume selected conversation in Claude Code
claude-history --show-tools        # Show tool calls
claude-history --plain --no-pager  # Plain text (still needs terminal)
```

## Which Tool When

| Need | Tool |
|------|------|
| From Claude Code (any search) | `resurface` |
| "What did I do today/yesterday" | `resurface` or `resurface --full` |
| Search prompts (fast) | `resurface search "pattern"` |
| Deep transcript search | `resurface search "pattern" --deep` |
| Browse/find a conversation interactively | `claude-history` (terminal only) |
| Resume a past Claude Code session | `claude-history --resume` (terminal only) |

## Performance

- **resurface prompt search:** <0.1s
- **resurface deep search:** 0.1-0.3s (rayon parallel scan across 3.2GB)
- **claude-history TUI:** instant (fuzzy filter in-memory)
- Binary: 1.3MB (release optimised)

## Notes

- Always uses HKT (UTC+8) for day boundaries
- `chat_history.py` (`~/scripts/chat_history.py`) still works as fallback
- This skill can be called by `/daily` for chat scanning
- Deep search includes tool names (e.g. `[tool: Read]`) for context but skips tool input/output
