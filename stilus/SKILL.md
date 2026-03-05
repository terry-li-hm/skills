---
name: stilus
description: Gmail CLI wrapper — compose, send, reply, and thread operations via gog gmail. Use when sending or replying to email.
triggers: ["send email", "reply email", "gog gmail send", "email reply", "compose email", "stilus"]
---
# stilus — Gmail Send/Reply CLI

Wraps `gog gmail send` for compose, reply, and thread operations.

## Sending a reply

Always use these three flags together for replies:

```bash
gog gmail send \
  --reply-to-message-id <message-id> \
  --reply-all \
  --quote \
  --subject "Re: <original subject>" \
  --body "..."
```

- `--reply-to-message-id` — sets In-Reply-To/References and keeps the thread intact
- `--reply-all` — auto-populates recipients from the original message (no `--to` needed)
- `--quote` — appends the original message below your reply
- Do NOT combine `--reply-to-message-id` with `--thread-id` — they are mutually exclusive

## Finding the message ID to reply to

```bash
# Search for threads
gog gmail search "<query>" --limit 10

# Read a thread (use the thread ID from search results)
gog gmail thread <thread-id>
```

Use the **last message's ID** (shown as `=== Message N/N: <id> ===`) as `--reply-to-message-id`.

## Before replying: fetch first

Always read the thread before sending. Duplicate sends have happened (same body sent twice). Check for recent outbound messages before composing.

## Composing a new email

```bash
gog gmail send \
  --to "recipient@example.com" \
  --subject "Subject" \
  --body "..."
```

## Auth gotcha

`gog` requires `GOG_KEYRING_PASSWORD` in env. If not set:

```bash
GOG_KEYRING_PASSWORD=<password> gog gmail send ...
```

Password is in 1Password: item `sge746vsbefyi6pojwwodzu3o4`, field `gog_keyring_password`.
