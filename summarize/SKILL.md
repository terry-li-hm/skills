---
name: summarize
description: Summarize or extract text from URLs, podcasts, and local files. "summarize this"
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

## Consultant-Style Summaries

For consulting-style outputs, use these templates:

### Executive Summary Template

```
## Executive Summary

### Situation
[Context and background of the material]

### Key Findings
1. [Finding 1] — [supporting detail]
2. [Finding 2] — [supporting detail]
3. [Finding 3] — [supporting detail]

### Recommendations
1. [Action 1] — [rationale and impact]
2. [Action 2] — [rationale and impact]
3. [Action 3] — [rationale and impact]

### Conclusion
[2-3 sentence wrap-up with next steps]
```

### Key Findings Template

```
## Key Findings

1. **[Finding Title]**
   - Evidence: [supporting detail from source]
   - Impact: [why this matters]

2. **[Finding Title]**
   - Evidence: [supporting detail from source]
   - Impact: [why this matters]

3. **[Finding Title]**
   - Evidence: [supporting detail from source]
   - Impact: [why this matters]
```

### Recommendations Structure

```
## Recommendations

### Priority 1: [High-Impact Action]
**Rationale:** [why this is critical]
**Expected Outcome:** [concrete result]
**Timeline:** [suggested timeframe]

### Priority 2: [Medium-Impact Action]
**Rationale:** [why this matters]
**Expected Outcome:** [concrete result]
**Timeline:** [suggested timeframe]

### Priority 3: [Optional/Low-Impact Action]
**Rationale:** [nice to have]
**Expected Outcome:** [concrete result]
**Timeline:** [suggested timeframe]
```

## Tips

- For huge transcripts, return a tight summary first, then ask which section to expand
- Use `--extract-only` when user explicitly wants the raw transcript
- Supports PDFs, articles, YouTube, and most web content
