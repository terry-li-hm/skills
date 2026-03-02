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

### Reply to Thread (DEFAULT: always quote)
**Always use `--reply-to-message-id` + `--quote` when replying.** This is the default — never omit `--quote` unless explicitly asked.
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

## Inbox Triage (Morning Email Processing)

Standard flow for clearing the inbox:

### 1. Get all unread + inbox
```bash
gog gmail search "is:unread" --max 50 --plain
gog gmail search "in:inbox" --max 20 --plain
```

### 2. Triage — categorise each as: action / informational / archive

### 3. Batch mark read + archive
```bash
gog gmail batch modify <id1> <id2> ... --remove UNREAD --remove INBOX -y
```

**Thread gotcha:** Search results show one ID per thread. If a thread has `[2 msgs]` or more, the batch modify only marks the shown message — newer messages in the thread remain unread. Fix: after the batch, re-run `gog gmail search "is:unread"` and clean up any stragglers.

### 4. Cora brief — read from website (more complete than email)
```bash
AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile" agent-browser open "https://cora.computer/14910/briefs?date=<YYYY-MM-DD>&time=morning" \
  && AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile" agent-browser wait --load networkidle \
  && AGENT_BROWSER_PROFILE="$HOME/.agent-browser-profile" agent-browser eval "document.querySelector('main')?.innerText"
```
The website brief includes payments, newsletters, and promotions that the summary email omits.

### 5. SmarTone bill — extract QR payment link
```bash
gog gmail get <smartone_id> --plain | grep -o 'href="https://myaccount.smartone.com/QRBill[^"]*"'
```
Surface as clickable link with amount and due date.

## Known Gaps
- **No trash/delete command in gog.** User must delete messages manually in Gmail.

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

