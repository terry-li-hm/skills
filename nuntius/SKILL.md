---
name: nuntius
description: "Cora CLI — AI email assistant. Use for Cora-specific actions: reading briefs, managing email todos, chatting with Cora, or searching email via the Cora interface. NOT for direct Gmail operations (send, archive, triage) — use expedio for those."
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

## Known Gotchas

### `important_draft` emails are excluded from briefs (by design)
Cora keeps `important_draft` emails in the inbox rather than digesting them into the brief — and they do NOT generate todos either. High-stakes emails (interview invitations, time-sensitive replies) can go completely unnoticed.

**Mitigation:** When expecting a reply from a specific sender, proactively search:
```
cora email search "from:domain.com"
cora email search "interview"
```

Real case: MTR interview invitation (Mar 4 2026, 18:15) was categorised `important_draft` — missed by both the 16:08 brief and the todo queue. Found only via manual `cora email search "MTR"`.

## Error Codes

- `0` — Success  
- `1` — General error  
- `2` — Authentication required (`cora login`)  
- `3` — Resource not found  
- `4` — Validation error
