---
name: message
description: Draft networking and follow-up messages for job search contacts. Use when user says "message", "draft message", "follow up", "outreach", "reach out to", or "nudge".
---

# Message

Unified messaging skill for drafting networking outreach and follow-up messages. Use `--type` to select message type.

## Trigger

Use when:
- User says "message", "draft message to [name]"
- User says "follow up on [company/person]", "nudge [company]"
- User says "outreach to [name]", "reach out to [name]"
- During weekly reset when follow-ups are identified

## Inputs

- **contact**: Name of person or company (required)
- **type**: `cold` | `warm` | `followup` | `thankyou` (required or inferred)
- **channel** (optional): `linkedin` | `email` | `whatsapp` (affects tone/length)
- **context** (optional): Additional context about the relationship

## Workflow

1. **Check vault for context**:
   - `/Users/terry/notes/Job Hunting.md` — networking section
   - Any linked notes like `[[Contact Name]]`
   - Search vault for mentions

2. **Gather information**:
   - How Terry knows them
   - Last interaction date
   - Their current role/company
   - Shared history or mutual connections

3. **Research contact** (if needed):
   - Current role on LinkedIn (web search)
   - Recent activity or news
   - Mutual connections

4. **Assess timing** (for follow-ups):
   | Time Since Last Contact | Recommendation |
   |------------------------|----------------|
   | < 1 week | Too soon, wait |
   | 1-2 weeks | Good time for first follow-up |
   | 2-3 weeks | Definitely follow up |
   | 3+ weeks | Follow up, temper expectations |

5. **Draft message** based on type and channel

6. **Present draft** with timing notes

7. **Update vault** after sending

## Message Types

### Cold Outreach (`--type=cold`)
First contact with someone Terry doesn't know well.

```
Hi [Name],

I came across your work on [specific thing] and found it really interesting.

I'm currently exploring opportunities in [area] and would love to learn more about your experience at [company]. Would you have 15-20 minutes for a quick chat?

Best,
Terry
```

### Warm Reconnection (`--type=warm`)
Re-engaging with former colleagues or acquaintances.

```
Hi [Name],

Hope you're doing well! It's been a while since [shared context].

I'm currently exploring new opportunities in [area] and thought of you given your experience at [company/in field]. Would love to catch up briefly if you have a few minutes.

[Sign-off]
```

### Follow-up (`--type=followup`)
Following up on applications or previous outreach.

**Application follow-up:**
```
Hi [Name],

I wanted to follow up on my application for [Role]. I'm still very interested in the opportunity and happy to provide any additional information.

Is there an update on the process?

Best,
Terry
```

**Post-interview follow-up:**
```
Hi [Name],

Thanks again for the conversation on [day]. I enjoyed learning about [specific thing discussed].

Looking forward to hearing about next steps.

Best,
Terry
```

**Networking bump:**
```
Hi [Name],

Just bumping this in case it got buried — would still love to connect if you have a few minutes.

No worries if timing doesn't work!
```

### Thank You (`--type=thankyou`)
Post-interview or post-meeting gratitude.

```
Hi [Name],

Thank you for taking the time to speak with me today about the [Role] position at [Company].

I especially enjoyed discussing [specific topic]. It reinforced my excitement about the opportunity to [specific contribution].

Please let me know if you need any additional information. I look forward to hearing from you.

Best,
Terry
```

## Channel Guidelines

| Channel | Tone | Length | Notes |
|---------|------|--------|-------|
| LinkedIn | Professional, concise | ~100 words max | Get to point quickly |
| Email | Slightly longer OK | 150-200 words | Include subject line |
| WhatsApp | Casual, brief | ~50 words | Conversational |

## Error Handling

- **If contact not in vault**: Ask for context or offer to research
- **If timing unclear**: Ask when last contact was
- **If purpose ambiguous**: Ask what outcome Terry wants

## Output

- Draft message tailored to channel
- Suggested subject line (for email)
- Timing recommendation
- Notes on follow-up strategy

## Tips

- Specific > generic — reference something real
- Make the ask easy (short call, quick intro)
- Don't over-explain why job hunting
- For HK contacts, adjust formality as appropriate
- One follow-up is expected; three is pushy

## Migration Note

This skill replaces:
- `/outreach` → use `/message --type=cold` or `--type=warm`
- `/follow-up` → use `/message --type=followup`

The old skills are kept for backwards compatibility.
