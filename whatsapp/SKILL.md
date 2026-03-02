---
name: whatsapp
description: Read and send WhatsApp messages using the wacli CLI. Use when user asks to check WhatsApp, read messages, or send a WhatsApp message.
user_invocable: false
github_url: https://github.com/steipete/wacli
---

# WhatsApp Access

Read and send WhatsApp messages using the `wacli` CLI.

## Prefer keryx for name-based lookups

**Use `keryx` instead of raw `wacli` when working by contact name:**
```bash
keryx read "Herman"          # merges dual-JID automatically
keryx send "Herman" "..."    # resolves JID + prints daemon-safe block
keryx chats                  # recent chats
```
Fall back to `wacli` directly for JID-based queries, search, auth, and admin.

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

All commands use subcommand pattern: `wacli <resource> <action> [flags]`.

### Check Auth Status
```bash
wacli doctor
```

### Sync Messages
```bash
wacli sync --once               # Sync until idle, then exit
wacli sync --once --refresh-contacts  # Also refresh contact names
```
**Always sync before reading** — database can be stale.

### List Recent Chats
```bash
wacli chats list --limit 20
wacli chats list --limit 20 --json       # Structured output
wacli chats list --query "Gavin"         # Filter by name
```

### Read Messages from a Chat
```bash
# By chat JID (from chats list output)
wacli messages list --chat "85298765432@s.whatsapp.net" --limit 20

# With date filters
wacli messages list --chat "85298765432@s.whatsapp.net" --after 2026-02-01 --limit 20
```

### Search Messages
```bash
# Search by keyword across all chats
wacli messages search "interview" --limit 20

# Search within a specific chat
wacli messages search "buyout" --chat "85298765432@s.whatsapp.net" --limit 10

# With date filters
wacli messages search "coffee" --after 2026-01-01 --limit 10
```

### Send Message
**`wacli send` requires an interactive terminal** — Claude cannot run it directly.
Draft the command for the user to copy-paste:
```bash
# Send to contact (user runs this themselves)
wacli send text --to "85298765432@s.whatsapp.net" --message "Thanks for your message!"

# Send to group (use group JID from chats list)
wacli send text --to "120363123456789@g.us" --message "Hello group"
```
**Note:** Subcommand is `send text`, and both `--to` (JID, not phone number) and `--message` are required flags.

### Contacts
```bash
wacli contacts search "Gavin" --limit 10
wacli contacts show "85298765432@s.whatsapp.net"
```

### Download Media
```bash
wacli media download --id "ABC123" --chat "85298765432@s.whatsapp.net" --output ~/Downloads/
```

## Output Formats

Add `--json` to any command for structured JSON output:
```bash
wacli chats list --limit 10 --json
wacli messages list --chat "852..." --json
```

## Common Patterns

### Check for new messages from a contact
```bash
wacli sync --once 2>/dev/null
wacli messages list --chat "<JID>" --after 2026-02-10 --limit 10
```

### Find a contact's JID
```bash
wacli chats list --query "Gavin"
# Or:
wacli contacts search "Gavin"
```

### View full conversation context
```bash
wacli messages list --chat "<JID>" --limit 30
```

### Contact has both phone JID and LID — query both
When `chats list` shows a contact with two entries (one `@s.whatsapp.net`, one `@lid`), **always query both** and merge mentally. Outgoing messages are typically on the phone JID; incoming on the LID.
```bash
wacli messages list --chat "85297096240@s.whatsapp.net" --limit 20
wacli messages list --chat "243649350766774@lid" --limit 20
```
Don't stop at the phone JID — you'll miss their replies.

## Message Direction

In `wacli messages` output:
- `FROM: me` — Messages you sent
- `FROM: <JID>` — Messages you received (shows sender JID)

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

**Workaround:** Query the phone number JID (`@s.whatsapp.net`) which usually has both directions. If only `@lid` exists, query that instead. Check `wacli chats list` for available JIDs.

**Upstream:** [Issue #31](https://github.com/steipete/wacli/issues/31)

## Query Gotchas

- **JID must use `--chat` flag, not positional arg.** `wacli messages list 123@lid` silently ignores the JID and returns all chats. Always: `wacli messages list --chat 123@lid`.
- **`--limit N` without `--chat` pulls from ALL chats.** Group chat noise (especially active groups like 9up) will push DM messages out of results. Always pass `--chat <JID>` when reading a specific conversation. Use `--limit 50` minimum for DM history — a `--limit 15` across all chats returned zero DMs.
- **Before diagnosing "missing messages" as a wacli bug, verify the data isn't just outside your query window.** Re-query with higher limit + chat filter before concluding messages weren't captured.

## Daemon & Lock

- **Daemon running via launchd:** `com.terry.wacli-sync` — persistent `sync --follow`. No need for manual sync before reading.
- **DB lock:** Only one wacli process at a time. Stop daemon before running backfill or other write commands: `launchctl unload ~/Library/LaunchAgents/com.terry.wacli-sync.plist`
- **Daemon silently dies:** Check `launchctl list com.terry.wacli-sync` (exit 113 = not running). Restart: `launchctl load ~/Library/LaunchAgents/com.terry.wacli-sync.plist`.
- **Missed messages before daemon start:** WhatsApp doesn't re-deliver to linked devices. `history backfill` is unreliable (often times out). Just ask user to paste.

## Cautions

- **QR expires**: If disconnected, need to re-auth with `wacli auth`
- **Rate limits**: Don't send too many messages too quickly
- **Groups**: Use group JID (ends with `@g.us`) not phone number
- **Send safety**: `wacli send` is blocked from non-interactive terminals — always draft command for user
- **Automated contexts**: For cron scripts or non-interactive agents, use read-only commands only (`chats list`, `messages list`, `messages search`). Never attempt `wacli send` from automated pipelines.

## Sending — Daemon Lock

`wacli send` will fail with "store is locked" if the daemon is running. Stop daemon first, send, restart:

```bash
launchctl unload ~/Library/LaunchAgents/com.terry.wacli-sync.plist
wacli send text --to "<JID>" --message "<text>"
launchctl load ~/Library/LaunchAgents/com.terry.wacli-sync.plist
```

**Always draft the full 3-command block for Terry to run.** Don't just give the `wacli send` line.

## Drafting Messages

**Always read recent exchange before drafting.** Match the tone, language (Cantonese/English mix), and formality of Terry's previous messages to that contact. Don't draft in isolation — pull the last 5–10 messages first and mirror the register.

## Integration with Message Skill

The `/message` skill uses `wacli` for WhatsApp message retrieval and sending. This is the underlying CLI reference.
