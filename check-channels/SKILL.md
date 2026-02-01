---
name: check-channels
description: Unified sweep of WhatsApp, LinkedIn DMs, and Gmail for new messages. Use when user says "check messages", "any replies?", "check channels", or wants to see if anyone reached out.
user_invocable: true
---

# Check All Channels

Sweep WhatsApp, LinkedIn, and Gmail in parallel to surface new messages—especially useful during job hunt when replies can come from anywhere.

## Trigger

Use when:
- User asks "any messages?" or "any replies?"
- User says "check channels" or "check messages"
- Morning briefing needs message status
- User returns from AFK and wants to catch up

## Workflow

Run all three checks in parallel:

### 1. WhatsApp (wacli)
```bash
wacli chats --limit 15 --json | jq '[.[] | select(.unread > 0)] | length'
# If unread > 0, get details:
wacli chats --limit 15 --json | jq '.[] | select(.unread > 0) | {name: .name, unread: .unread, last: .last_message.text[0:80]}'
```

### 2. LinkedIn DMs (browser automation)
Use agent-browser or Claude in Chrome:
- Navigate to linkedin.com/messaging
- Check for unread indicator (badge count)
- List recent conversations with unread status

### 3. Gmail (MCP)
```
mcp__gmail__search_emails with query: "is:unread -category:promotions -category:social"
```
Or use `gog`:
```bash
gog gmail messages list --query "is:unread -category:promotions -category:social" --max 10
```

## Output Format

Present a unified summary:

```
## Message Check (HKT timestamp)

**WhatsApp** — 2 unread
- German Recruiter: "Thanks for your time yesterday..."
- Family Group: "Dinner Sunday?"

**LinkedIn** — 1 unread
- Sarah Chen (HSBC Recruiter): New message

**Gmail** — 3 unread (excluding promos/social)
- interview@company.com: "Interview confirmation..."
- recruiter@firm.com: "Following up on..."
- newsletter@... (skipped, low priority)

---
Priority: [Highlight any job-hunt related messages]
```

## Error Handling

| Channel | If fails | Fallback |
|---------|----------|----------|
| WhatsApp | "Not authenticated" | Tell user to run `wacli auth` |
| LinkedIn | Login wall | Use Claude in Chrome with active session |
| Gmail | MCP error | Try `gog gmail` CLI instead |

## Integration

- `/morning` skill calls this as part of daily briefing
- Can be run standalone anytime
- Results can feed into `/message` skill for drafting replies

## Cautions

- LinkedIn browser automation may be slow (5-10 sec)
- WhatsApp requires prior `wacli auth` setup
- Gmail filters out promotions/social by default (override with explicit query if needed)
