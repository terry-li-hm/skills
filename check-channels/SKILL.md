---
name: check-channels
description: Unified sweep of WhatsApp, LinkedIn DMs, and Gmail for new messages. "check messages"
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

Run Gmail CLI and WhatsApp check in parallel, then browser for LinkedIn.

### 1. WhatsApp (wacli)
```bash
# Check connection first
wacli doctor | grep CONNECTED

# If CONNECTED=false, reconnect:
wacli sync &  # runs in background, takes ~10s

# List recent chats (unread count NOT available in JSON output)
wacli chats list --limit 15 --json | jq '.data[] | {name: .Name, last: .LastMessageTS}'
```

**Limitation:** `wacli` doesn't expose unread count. Show recent chats and let user identify what needs attention based on timestamps.

### 2. LinkedIn DMs (browser automation)
Use Claude in Chrome:
```
1. Navigate to linkedin.com/messaging
2. Read page with depth 8-10
3. Look for conversations where last message is NOT "You:" prefix
4. Check for unread badge in nav (e.g., "5 unread")
```

Key elements to find:
- Nav badge: `generic "X unread"` near Messaging link
- Conversation list: messages starting with contact name (not "You:") = incoming

### 3. Gmail (gog CLI)
```bash
# Search unread, excluding noise
gog gmail search "is:unread -category:promotions -category:social -from:jobalerts-noreply@linkedin.com" --max 10
```

Priority keywords to flag: interview, offer, recruiter, following up, schedule

## Output Format

```
## Message Check (HKT timestamp)

**WhatsApp** — Connected ✓
- Recent: [list recent chats with timestamps]
- [Note any that look like they need response based on timing]

**LinkedIn** — X unread (or "0 unread")
- [List conversations with incoming messages]
- Flag recruiters/job-related

**Gmail** — X unread (filtered)
- ⚠️ [urgent items first]
- [other items]

---
Priority: [Highlight job-hunt related messages needing response]
```

## Error Handling

| Channel | If fails | Fallback |
|---------|----------|----------|
| WhatsApp | CONNECTED=false | Run `wacli sync &`, wait 10s, retry |
| WhatsApp | "Not authenticated" | Tell user to run `wacli auth` |
| LinkedIn | Login wall | Use Claude in Chrome with active session |
| Gmail | CLI error | Use Gmail MCP tools |

## Integration

- `/morning` skill calls this as part of daily briefing
- Can be run standalone anytime
- Results can feed into `/message` skill for drafting replies

## Cautions

- LinkedIn browser automation takes 5-10 sec
- WhatsApp requires prior `wacli auth` setup
- WhatsApp unread count not available — rely on timestamps and "You:" prefix detection
- Gmail filters out promotions/social by default
