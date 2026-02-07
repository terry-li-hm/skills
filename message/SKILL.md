---
name: message
description: Draft responses to recruiter, networking, and other messages. Use when the user asks to reply or draft a message.
user_invocable: true
---

# Message Response Skill

Draft responses to messages from recruiters, networking contacts, and others.

## Triggers

- "message" / "draft message"
- "reply to [name]"
- "[name] replied" / "[name] messaged"
- "follow up with [name]"
- "respond to [name]"

## Workflow

### 1. Find the Message

Check these sources:

- **Gmail**: `gog gmail search "from:[name]"` or `mcporter call gmail.search_emails query="from:[name]"`
- **LinkedIn**: Browser automation to check messaging
- **WhatsApp**: `wacli messages --contact "[name or number]"` or `wacli chats` to list recent

If user says "[name] replied" without specifying platform, check Gmail and LinkedIn first before asking.

### 2. Get Context from Vault

Search the vault for background on this person:

```bash
grep -ri "[name]" /Users/terry/notes/*.md
```

Key files to check:
- `Job Hunting.md` - recruiter interactions, role discussions
- `Draft Outreach Messages*.md` - previous message drafts
- Daily notes - recent interactions

### 3. Understand the Conversation

Review:
- What was the last message Terry sent?
- What is the person asking/proposing?
- What's the relationship (recruiter, hiring manager, networking contact)?
- Any pending action items or decisions?

### 4. Draft Reply

Apply Terry's messaging preferences:
- **Minimal exclamation marks** - one at most, prefer periods
- **No redundant context** - don't repeat what they already know
- **Trim filler** - keep it tight and direct
- **Match tone** - professional but warm for recruiters

For scheduling:
- Check `[[Schedule]]` for availability
- Propose specific times, not vague "next week"
- Account for HKT timezone

### 5. Review with Judge

Before presenting to Terry, run the draft through `/judge`:
- Use `outreach` criteria for networking/cold messages
- Use `default` criteria for simple replies
- If verdict is `needs_work`: revise based on feedback (max 2 iterations)
- Ensure personalization, clear ask, and appropriate length

### 6. Present and Confirm

Show:
1. Summary of their message
2. Relevant context from vault
3. Draft reply (judge-reviewed)

Ask Terry to confirm or adjust before sending.

### 7. Update Vault

After message is sent, update:
- `Job Hunting.md` with new status/next steps
- Create follow-up reminder if needed

## Example Usage

**User**: "german replied"

**Claude**:
1. Checks Gmail → finds LinkedIn notification
2. Opens LinkedIn messaging via browser
3. Reads German's message about coffee meeting
4. Finds context in vault (ConnectedGroup recruiter, senior data PM roles)
5. Drafts reply with WhatsApp number and confirms Feb 2-5 works
6. Presents draft for approval

## Outreach Templates

See `[[Networking Outreach Templates]]` in vault for message templates and principles.

## Platform Notes

- **LinkedIn:** Browser automation (requires login)
- **Gmail:** `gog gmail search/get/send` — see `gmail` skill
- **WhatsApp:** `wacli` CLI — see `whatsapp` skill
