---
name: whatsapp
description: Read and send WhatsApp messages using the wacli CLI. Use when user asks to check WhatsApp, read messages, or send a WhatsApp message.
user_invocable: false
github_url: https://github.com/nickschwab/wacli
---

# WhatsApp Access

Read and send WhatsApp messages using the `wacli` CLI.

## Trigger

Use when:
- User asks "check WhatsApp" or "any WhatsApp messages?"
- User wants to read messages from a contact
- User wants to send a WhatsApp message
- Following up on a conversation mentioned in WhatsApp

## Prerequisites

- `wacli` CLI installed (`/opt/homebrew/bin/wacli`)
- Authenticated: run `wacli auth` once to scan QR code
- Store directory: `~/.wacli` (default)

## Commands

### Check Auth Status
```bash
wacli doctor
```

### List Recent Chats
```bash
wacli chats --limit 20
wacli chats --limit 20 --json  # For structured output
```

### Search Messages
```bash
# Search by contact (phone number or name)
wacli messages --contact "+85261872354" --limit 10

# Search by keyword across all chats
wacli messages --search "interview" --limit 20

# Combine contact + keyword
wacli messages --contact "German" --search "coffee" --limit 10
```

### Read Specific Chat
```bash
# By phone number
wacli messages --contact "+85298765432" --limit 20

# By chat ID (from chats list)
wacli messages --chat "85298765432@s.whatsapp.net" --limit 20
```

### Send Message
```bash
# Send text
wacli send --to "+85298765432" --text "Thanks for your message!"

# Send to group (use group JID from chats list)
wacli send --to "120363123456789@g.us" --text "Hello group"
```

### Download Media
```bash
# Download media from a message
wacli media --message-id "ABC123" --output ~/Downloads/
```

### Contact Management
```bash
# List contacts
wacli contacts --limit 50

# Search contacts
wacli contacts --search "recruiter"
```

## Output Formats

Add `--json` to any command for structured JSON output:
```bash
wacli chats --limit 10 --json
wacli messages --contact "+852..." --json
```

## Common Patterns

### Check for new messages from recruiters
```bash
wacli chats --limit 10 --json | jq '.[] | select(.unread > 0)'
```

### Find messages from a specific person
```bash
wacli messages --search "German" --limit 20
```

### Reply to last message in a chat
```bash
# Get last message to see context
wacli messages --contact "+852..." --limit 1

# Send reply
wacli send --to "+852..." --text "Your reply here"
```

## Message Direction

In `wacli messages` output:
- `from_me: true` — Messages you sent
- `from_me: false` — Messages you received

## Cautions

- **QR expires**: If disconnected, need to re-auth with `wacli auth`
- **Rate limits**: Don't send too many messages too quickly
- **Media**: Large media downloads may take time
- **Groups**: Use group JID (ends with `@g.us`) not phone number

## Integration with Message Skill

The `/message` skill uses `wacli` for WhatsApp message retrieval and sending. This is the underlying CLI reference.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not authenticated" | Run `wacli auth` and scan QR |
| "Session expired" | Run `wacli auth` again |
| Contact not found | Use phone number with country code (+852...) |
| Messages not syncing | Run `wacli sync` to backfill history |
| Sent messages missing | See LID/JID splitting issue below |

## Known Issue: LID/JID Splitting

**Symptom:** Querying a chat shows only incoming messages — your sent messages are missing.

**Cause:** WhatsApp uses two JID formats for the same contact:
- `XXXXXXXXXX@s.whatsapp.net` (phone number format)
- `YYYYYYYY@lid` (Linked ID format)

Messages get split between them. When you query one JID, you only see half the conversation.

**Diagnosis:**
```bash
sqlite3 ~/.wacli/wacli.db "SELECT chat_jid, from_me, COUNT(*) FROM messages WHERE chat_name LIKE '%ContactName%' GROUP BY chat_jid, from_me;"
```

**Workaround:** Query the phone number JID (`@s.whatsapp.net`) which usually has both directions:
```bash
wacli messages list --chat "85298765432@s.whatsapp.net" --limit 20
```

**Or merge in database** (one-time):
```bash
sqlite3 ~/.wacli/wacli.db "UPDATE messages SET chat_jid='85298765432@s.whatsapp.net' WHERE chat_jid='YYYYYYYY@lid';"
```

**Upstream:** [Issue #31](https://github.com/steipete/wacli/issues/31)
