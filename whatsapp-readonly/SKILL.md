---
name: whatsapp-readonly
description: Check WhatsApp messages using wacli (read-only, no sending). Use when asked to check WhatsApp, read messages, or see recent chats.
user_invocable: true
---

# WhatsApp Read-Only

Check WhatsApp messages safely using wacli CLI. **This skill cannot send messages.**

## Available Commands

```bash
# List recent chats
wacli chats list --limit 20

# List messages from a specific chat
wacli messages list --chat "<JID>" --limit 10

# Search messages
wacli messages search "<query>" --limit 10

# Search contacts
wacli contacts search "<name>"
```

## Usage

1. Use `wacli chats list` to see recent conversations
2. Use `wacli contacts search` to find a contact's JID
3. Use `wacli messages list --chat "<JID>"` to read specific chat

## Important

- **READ ONLY** — never use `wacli send`
- JIDs look like: `85290336894@s.whatsapp.net` (phone) or `12345@g.us` (group)
- Sync first if messages seem stale: `wacli sync`
