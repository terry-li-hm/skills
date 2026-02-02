---
name: whatsapp-readonly
description: Check WhatsApp messages using wacli-ro (read-only wrapper, send blocked). Use when asked to check WhatsApp, read messages, or see recent chats.
user_invocable: true
---

# WhatsApp Read-Only

Check WhatsApp messages safely using `wacli-ro` (read-only wrapper). **Send is blocked at the script level.**

## Available Commands

```bash
# List recent chats
wacli-ro chats list --limit 20

# List messages from a specific chat
wacli-ro messages list --chat "<JID>" --limit 10

# Search messages
wacli-ro messages search "<query>" --limit 10

# Search contacts
wacli-ro contacts search "<name>"
```

## Usage

1. Use `wacli-ro chats list` to see recent conversations
2. Use `wacli-ro contacts search` to find a contact's JID
3. Use `wacli-ro messages list --chat "<JID>"` to read specific chat

## Important

- **ALWAYS use `wacli-ro`** — not `wacli` directly
- `wacli-ro` blocks send commands at the script level
- JIDs look like: `85290336894@s.whatsapp.net` (phone) or `12345@g.us` (group)
- Sync if messages seem stale: `wacli-ro sync`
