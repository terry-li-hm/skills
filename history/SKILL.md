---
name: history
description: Scan and search chat history with proper HKT timezone handling. Use when reviewing what was discussed on a specific day or searching for past conversations.
user_invocable: true
---

# History

Search AI coding chat history from Claude Code, Codex, and OpenCode.

## Tools

- **`claude-history`** (Rust CLI) — interactive TUI fuzzy search over Claude Code conversations. Best for browsing, finding a specific conversation, or resuming a session.
- **`chat_history.py`** (Python) — programmatic date scan, keyword search, cross-tool support (Claude + Codex + OpenCode), HKT day boundaries. Best for "what did I do today" and searching across all tools.

## Trigger

- `/history` — today's prompts across all tools (chat_history.py)
- `/history yesterday` — yesterday's prompts
- `/history 2026-01-18` — specific date
- `/history --tool=Codex` — filter by specific tool
- `/history search self-intro` — search prompts for keyword (last 7 days)
- `/history search DBS --deep` — search full transcripts (user + assistant)
- `/history search DBS --days=30` — search last 30 days
- `/history browse` — launch claude-history TUI (interactive fuzzy search)
- `/history browse --global` — search all projects at once

## claude-history (Interactive TUI)

```bash
# Interactive fuzzy search (current project)
claude-history

# Search all projects globally
claude-history --global

# Resume a conversation in Claude Code
claude-history --resume

# View a specific JSONL file
claude-history /path/to/conversation.jsonl

# Show tools / thinking blocks
claude-history --show-tools --show-thinking

# Plain text output (no TUI)
claude-history --plain --no-pager
```

Key options:
- `-g, --global` — search all conversations from all projects
- `-c, --resume` — resume selected conversation in Claude Code
- `-t, --show-tools` — show tool calls
- `--show-thinking` — show thinking blocks
- `-l, --last` — show last messages in preview (default: first)
- `-r, --relative-time` — relative timestamps ("10 minutes ago")
- `--plain` — plain text without ledger formatting
- `--pager` — pipe through less

## chat_history.py (Programmatic Search)

```bash
# --- Date scan mode ---
python ~/scripts/chat_history.py                  # Today's prompts
python ~/scripts/chat_history.py yesterday        # Yesterday's prompts
python ~/scripts/chat_history.py 2026-01-23       # Specific date
python ~/scripts/chat_history.py --full           # Show all prompts (not just last 50)
python ~/scripts/chat_history.py --json           # Output as JSON
python ~/scripts/chat_history.py --tool=Claude    # Filter by tool

# --- Search mode (prompts only — fast, <1s) ---
python ~/scripts/chat_history.py --search="self-intro"           # Last 7 days
python ~/scripts/chat_history.py --search="DBS" --days=30        # Last 30 days
python ~/scripts/chat_history.py --search="DBS" 2026-02-15       # Specific date

# --- Search mode (full transcripts — searches both user + assistant) ---
python ~/scripts/chat_history.py --search="self-intro" --deep           # Last 7 days
python ~/scripts/chat_history.py --search="DBS" --deep --days=30        # Last 30 days
```

## Which Tool When

| Need | Tool |
|------|------|
| Browse/find a conversation interactively | `claude-history` |
| Resume a past Claude Code session | `claude-history --resume` |
| "What did I do today/yesterday" | `chat_history.py` |
| Search across Claude + Codex + OpenCode | `chat_history.py --search` |
| Deep transcript search (assistant replies) | `chat_history.py --search --deep` |
| Filter by tool (Codex only, etc.) | `chat_history.py --tool=Codex` |

## Search Output Format (chat_history.py)

```
Search: "self-intro" (last 7 days, full transcripts)
Found 11 matches across 1 days

  2026-02-15:
    06:31 [d30e26ee] (claude)  ...DBS prep:** 2 short active recall reps (self-intro + Q&As)...
    07:00 [b2b70b70] (claude)  ...your prep note. No peeking.  **Round 1: Self-intro**...
    07:08 [b2b70b70] (you)     ...let me try the self-intro again with tweaks...

(0.5s)
```

## Performance

- **chat_history.py prompt search:** <0.5s (searches history.jsonl only)
- **chat_history.py deep search:** 0.5-5s depending on `--days` range
- **claude-history TUI:** instant (fuzzy filter in-memory)
- 3.2 GB across 4,170 session files — mtime filtering keeps it fast

## Notes

- Always uses HKT (UTC+8) for day boundaries (chat_history.py)
- Script location: `~/scripts/chat_history.py`
- This skill can be called by `/daily` for chat scanning
- Deep search includes tool names (e.g. `[tool: Read]`) for context but skips tool input/output
