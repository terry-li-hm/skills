---
name: summarize
description: Summarize or extract text/transcripts from URLs, podcasts, and local files. Use when user asks to summarize a link, transcribe a YouTube video, or extract content from a URL.
user_invocable: true
github_url: https://github.com/steipete/summarize
---

# Summarize

Fast CLI to summarize URLs, local files, and YouTube links.

## Trigger

Use when:
- User says "summarize this URL/article"
- User asks "what's this link/video about?"
- User says "transcribe this YouTube/video"
- User wants to extract content from a webpage or PDF

## Prerequisites

- `summarize` CLI installed: `brew install steipete/tap/summarize`
- API key for chosen model provider (OpenRouter, Anthropic, Google, etc.)

## Commands

### Summarize URL

```bash
summarize "https://example.com/article" --model google/gemini-3-flash-preview
```

### Summarize Local File

```bash
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
```

### YouTube Transcript

```bash
# Summary
summarize "https://youtu.be/VIDEO_ID" --youtube auto

# Extract transcript only (no summary)
summarize "https://youtu.be/VIDEO_ID" --youtube auto --extract-only
```

### Model Selection

```bash
# Fast + cheap
summarize "URL" --model google/gemini-3-flash-preview

# Higher quality
summarize "URL" --model anthropic/claude-sonnet-4
```

## Tips

- For huge transcripts, return a tight summary first, then ask which section to expand
- Use `--extract-only` when user explicitly wants the raw transcript
- Supports PDFs, articles, YouTube, and most web content
