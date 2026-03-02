---
name: keryx
description: WhatsApp CLI wrapper — contact name resolution, dual-JID conversation merging, daemon-aware send block. Use instead of raw wacli when working with contacts by name.
---

# keryx

Thin wrapper around `wacli` that fixes its three friction points: manual JID lookup, split conversations across phone/LID JIDs, and daemon lock on send.

## Commands

```bash
keryx read "Herman"            # merged conversation (phone + LID JIDs)
keryx read "Herman" --limit 5  # last 5 messages
keryx send "Herman" "Hi"           # prints daemon-safe 3-command block
keryx send "Herman" "Hi" --copy   # same + copies to clipboard
keryx chats                    # recent chats (passthrough)
keryx chats --limit 10
```

## How It Works

**`keryx read`**
1. Resolves name → all JIDs via `wacli contacts search --json` + `wacli chats list --query --json`
2. Queries all JIDs (both `@s.whatsapp.net` and `@lid`)
3. Merges and deduplicates by timestamp
4. Shows last N messages as `[HH:MM] Me: ...` / `[HH:MM] Name: ...`

**`keryx send`**
Prints the 3-command block — does NOT execute. Copy-paste to run:
```bash
launchctl unload ~/Library/LaunchAgents/com.terry.wacli-sync.plist
wacli send text --to "<JID>" --message "<message>"
launchctl load ~/Library/LaunchAgents/com.terry.wacli-sync.plist
```

## Files

- Binary: `~/bin/keryx` (also at `~/code/keryx/target/release/keryx`)
- Source: `~/code/keryx/src/main.rs`
- Contact cache: `~/.config/keryx/contacts.json` (1h TTL, auto-refreshed)

## Gotchas

- **wacli daemon must be running** for reads to have current data. Check: `launchctl list com.terry.wacli-sync` (exit 113 = dead, restart with `launchctl load ~/Library/LaunchAgents/com.terry.wacli-sync.plist`)
- **`brew upgrade wacli` overwrites the patched binary.** keryx itself is fine but wacli may break — see `~/docs/solutions/wacli-business-message-fix.md` to re-patch.
- **Multiple name matches** are only an error if they're different people. Same-name / multiple-JID (dual-JID case) is handled automatically.
- **Send requires interactive terminal** — keryx intentionally outputs the command block rather than executing. Paste and run in your shell.
- **Cache** at `~/.config/keryx/contacts.json` — delete to force refresh if a new contact isn't found.

## When to Use keryx vs wacli Directly

| Task | Use |
|------|-----|
| Read conversation by name | `keryx read "Name"` |
| Send message by name | `keryx send "Name" "..."` |
| List chats | `keryx chats` |
| Lookup by JID | `wacli messages list --chat <jid>` directly |
| Search across chats | `wacli messages search "keyword"` directly |
| Admin (sync, auth, contacts) | `wacli` directly |
