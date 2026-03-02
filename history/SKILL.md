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

# --- Filtering (deep mode) ---
resurface search "weekly" --deep --role claude     # Only AI responses
resurface search "weekly" --deep --role you         # Only user messages
resurface search "W09" --deep --session b1b94317   # Specific session (prefix match)
resurface search "weekly" --deep --role claude --session b1b94317  # Combined
```

### Role aliases

| Filter value | Matches |
|---|---|
| `you` / `user` / `me` | User messages |
| `claude` / `assistant` / `ai` | AI responses (Claude + OpenCode) |
| `opencode` | OpenCode responses only |

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
| "Did X happen today?" | **Check daily note first** (`~/notes/Daily/$(date +%Y-%m-%d).md`), then `resurface search --deep --role claude` |
| Search prompts (fast) | `resurface search "pattern"` |
| Deep transcript search | `resurface search "pattern" --deep` |
| Filter out noise (intent vs execution) | `--role claude` (AI confirmations only) |
| Drill into specific session | `--session <8-char-prefix>` |
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
- **Session storage gotcha:** Claude Code stores entries from session A inside session B's JSONL file (via context compaction/continuity). The `--session` filter checks the entry-level `sessionId`, not the filename — this is correct.
- **"Did X happen?" strategy:** Search for execution markers (e.g. "synthesis complete", "note written", week number) not trigger words (e.g. "weekly"). Use `--role claude` to filter out intent mentions.
- **Use single keywords, not phrases.** `resurface search` matches the full query as a literal substring in each prompt. Multi-word queries like `"winnie joel lunch"` miss cases where terms appeared separately. Always start with the most distinctive single word (e.g. `"winnie"`), then narrow with `--session` if needed.
