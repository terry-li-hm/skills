---
name: nodus
description: LinkedIn automation via agent-browser — read messages, send replies, check notifications. Use when checking LinkedIn messages, replying to someone on LinkedIn, or when user says "X replied on LinkedIn".
user_invocable: true
---

# nodus — LinkedIn via agent-browser

Profile auto-loaded via `AGENT_BROWSER_PROFILE` env var (`~/.agent-browser-profile`). LinkedIn session persists — no login needed.

## Read Messages

```bash
agent-browser open "https://www.linkedin.com/messaging/" \
  && agent-browser wait 3000 \
  && agent-browser eval "document.querySelector('.msg-s-message-list').innerText"
```

To check a specific conversation is active, look for the contact name in the snapshot first:
```bash
agent-browser snapshot -i -d 3
```

## Send a Message

**Do NOT use `agent-browser type`** — it escapes special characters (`!` → `\!`, `—` may break). Use `keyboard type` instead:

```bash
agent-browser click e58   # textbox "Write a message…"
agent-browser keyboard type "Your message here"
agent-browser screenshot  # verify before sending
agent-browser click e64   # Send button (verify ref from snapshot)
```

Always take a screenshot and show user before sending. Wait for confirmation.

## Check Sent Message

After sending, verify with:
```bash
agent-browser eval "document.querySelector('.msg-s-message-list').innerText" 2>&1 | tail -20
```

Look for `(Edited)` tag if user has manually edited after send.

## Gotchas

- **`agent-browser type` escapes `!` → `\!`** and may mangle em-dashes. Always use `agent-browser keyboard type` for message body text.
- **Element refs (e58, e64) may change** between sessions — always run `snapshot -i` first to confirm refs before clicking.
- **Preview before sending** — screenshot + user confirmation is mandatory. LinkedIn messages cannot be unsent, only edited.
- **Editing a sent message:** hover over the message in the UI, click the `...` menu → Edit. Then retype corrected text. Edited messages show `(Edited)` label.

## "X replied on LinkedIn" reflex

When user says someone replied on LinkedIn:
1. Open messaging URL
2. Run `eval` to extract conversation text
3. Present the reply in chat
4. Offer to draft a response

Do NOT ask the user what was said — read it directly.
