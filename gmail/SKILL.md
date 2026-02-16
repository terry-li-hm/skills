---
name: gmail
description: Gmail operations with status-aware checking. Use when checking inbox, viewing threads, or replying to emails. Avoids draft vs sent confusion.
user_invocable: true
---

# Gmail Skill

Status-aware Gmail operations using the `gog` CLI. Prevents confusing drafts with sent messages.

## Commands

### Check Inbox
```bash
gog gmail search "newer_than:1d" --plain | head -20
```

### View Thread (with status check)
When viewing a thread, ALWAYS check each message's labels:
```bash
# Get thread overview
gog gmail thread get <thread_id>

# For any message you need to verify was actually sent:
gog gmail get <message_id> --plain | grep "label_ids"
```

**Critical:** A message in a thread view might be a DRAFT, not sent. Always verify:
- `label_ids` contains `SENT` → actually sent
- `label_ids` contains `DRAFT` → NOT sent, still a draft

### Check Drafts
```bash
gog gmail drafts list --plain
```

### Detect Cora Multi-Option Drafts
Cora creates drafts with multiple response options separated by `###`. These need human review to pick one option before sending.

```bash
# View a draft
gog gmail get <message_id>
```

If you see `###` in the body, it's a Cora multi-option draft. Do NOT auto-send.

### Reply to Thread (Safe)
```bash
gog gmail send \
  --thread-id "<thread_id>" \
  --to "<recipient_email>" \
  --subject "Re: <original_subject>" \
  --body "<message_body>"
```

### Reply with Quoted Original
```bash
gog gmail send \
  --reply-to-message-id "<message_id>" \
  --quote \
  --to "<recipient_email>" \
  --subject "Re: <original_subject>" \
  --body "<reply_body>"
```
- `--quote` fetches the original message and includes it as a proper blockquote (HTML with blue left border + plain text with `>` prefix)
- Preserves original formatting (links, bold, images) in the quote
- Adds "On \<date\>, \<sender\> wrote:" attribution line
- Requires `--reply-to-message-id` (not just `--thread-id`)

Always confirm with user before executing send.

### Create Draft (with attachments / threading)
```bash
gog gmail drafts create \
  --to "recipient@example.com" \
  --cc "cc@example.com" \
  --subject "Re: Thread Subject" \
  --reply-to-message-id "<message_id>" \
  --body "Message body" \
  --attach /path/to/file1.pdf \
  --attach /path/to/file2.pdf
```
- `--reply-to-message-id` threads the draft correctly (sets In-Reply-To/References headers)
- `--attach` is repeatable for multiple files
- The `send` command does NOT have a `--draft` flag — use `drafts create` instead

### Delete Draft
```bash
gog gmail drafts delete <draft_id> --force
```

## Status Indicators

When reporting email status to user, always be explicit:
- ✉️ SENT — confirmed sent (has SENT label)
- 📝 DRAFT — not sent yet (has DRAFT label)
- ⚠️ CORA DRAFT — Cora multi-option draft (has ### separators)

## Common Patterns

### "Did this email go out?"
```bash
gog gmail get <message_id> --plain | grep "label_ids"
```
Check for SENT vs DRAFT label.

### "Check for replies"
```bash
gog gmail search "newer_than:1d is:unread" --plain
```

### "What did Cora draft?"
```bash
gog gmail drafts list --plain
# Then check each for ### pattern
```
