---
name: message
description: Draft responses to recruiter, networking, and other messages. Use when the user asks to reply or draft a message.
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
- **WhatsApp**: Ask user to share the message (or check via wacli if configured)

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

## Networking Outreach Templates

Reference: `[[Networking Outreach Templates]]` in vault.

### Post-Event Contact (Direct)

Use when: Met someone at event, want to follow up with job interest.

> Hi [Name] — great meeting you at [Event], and congrats on [milestone if applicable]. I'm exploring my next chapter — if there's anything on your radar where my background might be a fit, I'd welcome the conversation. Open to a quick coffee next week?

**Principles:**
- Coffee/chat is the primary ask
- "Exploring my next chapter" signals search without desperation
- Don't ask them to "flag openings" in writing — save for verbal
- Send within 48 hours while fresh

### Softer Version (Peer Exchange First)

Use when: Build relationship before signaling job interest.

> Hi [Name] — great meeting you at [Event]. I'm exploring my next chapter and would enjoy swapping notes on [shared domain]. Would you be open to a quick coffee or call next week?

**Key difference:** Job signal is implicit. Save direct discussion for meeting.

### Key Principles (from LLM Council)

- Don't deputize contacts as informal recruiters (HR policy conflicts)
- Keep explicit job discussions verbal, off written record
- Personalize with specific event/milestone references
- Clear, single ask — don't stack requests

## Platform-Specific Notes

### LinkedIn
- Use browser automation (requires login)
- Can read and send messages via the messaging interface
- Check for InMail vs regular messages

### Gmail
- **OpenClaw:** Use `gog` skill (`gog gmail search`, `gog gmail get`)
- **MCP:** `mcporter call gmail.search_emails`, `mcporter call gmail.get_email`
- Can send via `gog gmail send` or MCP

### WhatsApp
- Use `wacli` if configured, otherwise ask user to paste the message
- Draft reply for user to send manually
