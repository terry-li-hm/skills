---
name: chrome-automation
description: Reference skill for Claude in Chrome browser automation best practices. Not user-invocable — use as internal guidance when automating Chrome.
user_invocable: false
platform: claude-code
platform_note: Reference for Claude in Chrome MCP tools. OpenClaw has equivalent browser tools with different API.
---

# Chrome Automation Best Practices

Reference for Claude in Chrome MCP tools. Consult when doing browser automation.

## Session Startup

1. **Always create a new tab** at session start using `tabs_create_mcp`
2. Only use tabs you created in this session — never reuse tab IDs from previous sessions
3. If a tool returns "tab doesn't exist", call `tabs_context_mcp` to get fresh tab IDs

## Reading Page Content

- **`read_page` captures the full accessibility tree** including content below the viewport
- No scrolling needed to get below-fold content
- Workflow: navigate → wait 2 seconds → `read_page` once
- Use `max_chars` parameter if page is large (default 50000)

## Window Sizing

- **Resize window before `read_page`** to reduce tokens
- 800x600 for chat apps (WhatsApp, messaging)
- 1024x768 for general browsing
- Large viewports waste context on empty space

## Page Load

- Always **wait 2 seconds** after navigation before reading
- If content shows loading placeholders, wait longer or refresh
- LinkedIn job pages may need extra time to hydrate

## Common Gotchas

| Issue | Solution |
|-------|----------|
| Tab ID invalid | Call `tabs_context_mcp` to refresh |
| Content not loading | Wait longer, or navigate directly to URL |
| Screenshot from wrong tab | Verify `tabId` in tool response matches intended tab |
| LinkedIn "Saved" toggles | Clicking "Saved" unsaves — use three-dot menu for actions |
| WhatsApp message direction | Left/white = incoming, right/green = outgoing |
| Gmail contenteditable | `form_input` unreliable on Gmail compose — write draft to file instead |

## Tool Selection

| Task | Tool |
|------|------|
| Get page structure/content | `read_page` |
| Extract article text | `get_page_text` |
| Click elements | `computer` with `ref` parameter |
| Type text | `computer` action=type |
| Navigate | `navigate` |
| Screenshot for debugging | `computer` action=screenshot |
| Create new tab | `tabs_create_mcp` |
| List available tabs | `tabs_context_mcp` |

## Login-Required Sites

These sites return login walls via web scraping tools — must use browser automation:
- LinkedIn
- X/Twitter
- WhatsApp Web
- Gmail (for some operations)

## Alerts and Dialogs

**Avoid triggering JavaScript alerts, confirms, or prompts** — they block all further browser events. If you must interact with dialog-triggering elements, warn the user first.

## Session Cleanup

**Always navigate to the idle page after completing browser automation tasks:**

```
https://terry-li-hm.github.io/claude-home/
```

This keeps the browser in a clean, non-distracting state instead of leaving it on a logged-in dashboard or sensitive page. The idle page shows a minimal dark background with subtle day/time in the corner.

## Related Skills

- `/evaluate-job` — Uses Chrome for LinkedIn job extraction
- `/review-saved-jobs` — Batch processes LinkedIn saved jobs
