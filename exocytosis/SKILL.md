---
name: exocytosis
description: Compress an insight to 280 chars and post to X (@zkMingLi). Use when a sharp standalone claim surfaces.
user_invocable: false
context: fork
---

# tweet — compress and post to X

## Posting

```bash
bird tweet "text"
```

- **280 char limit.** Compress ruthlessly. Cut adjectives, use arrows, no filler.
- **One attempt only.** 226 error → stop. Don't escalate (agent-browser, curl, GraphQL — makes it worse).
- **Account:** @zkMingLi. Auth via `AUTH_TOKEN` env var (.zshenv.local).
- **No smart quotes** in bird CLI — use straight quotes only.

## Compression

1. One-sentence thesis
2. Cut everything that doesn't serve it
3. Assertions over explanations
4. Parallel structure (X gives Y. Z gives W.)
5. Sharpest line last, not a summary

## Fallback (226 block)

```bash
deltos_send_text "tweet text"
```

Then provide intent URL: `https://x.com/intent/tweet?text=<url-encoded>`

Wait hours, try next session. One attempt per session.

## Telemetry

After a successful tweet, append one row to `~/notes/Meta/Content Telemetry.md`:

```
| {date} | tweet | — | {tweet-text truncated to 50 chars} | {source-topic} | — |
```

- **date**: ISO date (YYYY-MM-DD)
- **tweet-text**: first 50 chars of the tweet (no newlines)
- **source-topic**: the topic or idea that prompted this tweet (1–5 words)

If the file doesn't exist, create it with this header first:

```markdown
# Content Telemetry

| date | channel | slug | title | source-skill | tags |
|------|---------|------|-------|--------------|------|
```

## When to tweet

- Insight survives 280 chars as a standalone claim
- A position, not a summary
- If it needs explaining → garden it (`publish new "Title"`), don't tweet it

## Pipeline

Tweet is step 1. The full pipeline: **tweet** (probe) → **publish** (expand to garden) → **announce** (LinkedIn, blindspot-aware). Each step earns the next. Never skip to announce without tweeting first.
