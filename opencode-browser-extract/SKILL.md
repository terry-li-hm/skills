---
name: opencode-browser-extract
description: Extract web page content using OpenCode + Playwright MCP. Use when you need to scrape text from authenticated pages (like GARP Learning) while saving Claude tokens. Requires Playwright MCP configured with extended timeouts.
user_invocable: false
---

# OpenCode Browser Extraction

Use OpenCode (GLM-4.7) with Playwright MCP to extract web page content. Saves Claude tokens for mechanical extraction tasks.

## Prerequisites

Playwright MCP must have extended timeouts in `~/.opencode/mcp.json`:

```json
"playwright": {
  "command": "npx",
  "args": [
    "-y",
    "@playwright/mcp@latest",
    "--extension",
    "--timeout-action",
    "60000",
    "--timeout-navigation",
    "60000"
  ]
}
```

Without these timeouts, complex pages (like GARP Learning) will timeout during JS evaluation.

## Working Pattern

Simple, single-task prompts work best. GLM overthinks multi-step instructions.

```bash
# Basic extraction
opencode run "Playwright: go to [URL], click OK if dialog, JS: document.body.innerText.slice(0,8000), save to /tmp/output.txt"

# Targeted extraction (smaller content)
opencode run "Playwright: go to [URL], JS: document.querySelector('main')?.innerText?.slice(0,5000), save to /tmp/output.txt"
```

## What Works

- Single-page extraction
- Simple navigation + extract + save
- Pages that load within 60 seconds
- Authenticated pages (uses Chrome session via --extension)

## What Doesn't Work Well

- Multi-step sequences (GLM starts planning "subagents")
- Very long prompts with many instructions
- Pages with 60+ second load times

## Hybrid Pattern (Best for Complex Tasks)

When extracting multiple pages:

1. **Claude in Chrome** extracts text → saves to `/tmp/section_N.txt`
2. **OpenCode** appends files to vault (cheap file ops)

```bash
# OpenCode for file operations only
opencode run "Append contents of /tmp/s1.txt, /tmp/s2.txt to /path/to/note.md"
```

## Tab Management (IMPORTANT)

Each OpenCode + Playwright session creates new Chrome tabs. Parallel sessions multiply this quickly.

**Best practices:**
- **Limit parallelism:** Max 2-3 concurrent OpenCode sessions on iMac
- **Clean up after:** Close tabs after extraction completes
- **Sequential for reliability:** One section at a time works better than parallel

**Quick tab cleanup:**
```bash
# Get tab IDs
# Use mcp__browser-tabs__get_tabs to list, then close_tab_by_id for each duplicate
```

Or manually: Cmd+W to close tabs in Chrome.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| JS evaluate timeout | Default Playwright timeout too short | Add `--timeout-action 60000` |
| URL typos (garpleearning) | GLM hallucination | Usually self-corrects, or spell out carefully |
| "Using subagents" stall | Prompt too complex | Simplify to single task |
| Chrome tabs accumulating | Playwright creates new tabs | Clean up manually after each session |
| Parallel sessions conflict | Multiple sessions share browser | Run sequentially or limit to 2-3 |
| Exit code 124 | Timeout (often on "Done" message) | File may still be created - check |

## Example: GARP Learning Extraction

```bash
timeout 120 opencode run "Playwright: go to https://garplearning.benchprep.com/app/rai26#read/section/231-problem-specification-and-feature-selection, click OK, JS: document.body.innerText.slice(0,8000), save to /tmp/garp231.txt"
```
