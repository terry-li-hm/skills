---
name: cora-email
description: Use when the user asks about their email, inbox, briefs, email todos, or wants to interact with Cora — an AI email assistant. Covers checking briefs, managing todos, drafting replies, and chatting with Cora via the CLI.
---

# Cora CLI — AI Email Assistant

Cora is an AI-powered email assistant that processes Gmail, generates daily briefs, manages todos, and drafts replies. You interact with Cora through the `cora` command-line tool.

## Quick Start

Before running any command, verify you're authenticated:

```
cora whoami
```

If not authenticated, log in with your API token:

```
cora login --token=BiGWzbEAgubbiHR6gBkobkDZ
```

## Commands Reference

### Check Status
```
cora status    # Account status, brief settings, usage stats
cora whoami    # Current user and account info
```

### Email Briefs
```
cora brief              # List recent briefs
cora brief show         # Show latest brief details
cora brief show <id>    # Show specific brief
cora brief show --open  # Show and open in browser
cora brief --json       # JSON output (note: briefs use --json not --format json)
```

### Todos
```
cora todo list                                           # List pending todos
cora todo list --all                                     # Include completed
cora todo show <id>                                      # View details
cora todo create "Title"                                 # Create new todo
cora todo create "Title" --priority high --due tomorrow  # With options
cora todo edit <id> --title "New" --priority low         # Update
cora todo complete <id>                                  # Mark done
cora todo delete <id> --force                            # Delete
cora todo list --format json                             # JSON output
```

### Email
```
cora email glimpse          # Quick inbox view (fast, cached)
cora email search "query"   # Search with Gmail query syntax
cora email show <id>        # Full email details
cora email archive <id>     # Archive email
cora email draft <id>       # Queue reply draft (async, returns immediately)
```

### Chat (slow — use only when no instant command fits)
```
cora chat send "message"              # New conversation (10-60s)
cora chat send "message" --chat <id>  # Continue conversation
```

## Best Practices

- **Prefer instant commands** over `cora chat send` — chat is 10-60s
- **briefs use `--json`** not `--format json` (unlike other commands)
- **Don't use `cora flow`** — requires interactive stdin, will hang
- **Don't retry failures** more than once — ask user for guidance

## Error Codes

- `0` — Success  
- `1` — General error  
- `2` — Authentication required (`cora login`)  
- `3` — Resource not found  
- `4` — Validation error
