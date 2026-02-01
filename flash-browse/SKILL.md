---
name: flash-browse
description: Cheap browser automation using Gemini Flash. Use for high-volume testing, repetitive form filling, or when Claude token limits are a concern. Ideal for chatbot testing. NOT for tasks needing judgment or vault context.
user_invocable: true
---

# flash-browse

Browser automation using Gemini 2.0 Flash via OpenRouter (~$0.00005/step).

## When to use

- Testing chatbots with many queries
- High-volume, repetitive browser tasks
- When hitting Claude usage limits
- Simple navigation that doesn't need judgment

## When NOT to use

- Tasks needing vault context (job evaluation, personalized messages)
- Complex multi-step flows requiring judgment
- Anything needing Terry's preferences or history

## Usage

```bash
uv run /Users/terry/skills/flash-browse/flash_browse.py \
  --url "https://example.com" \
  --task "click the login button"
```

### Options

| Flag | Description |
|------|-------------|
| `--url` | URL to open (required) |
| `--task` | Task description (required) |
| `--max-steps` | Max steps before stopping (default: 20) |
| `--verbose`, `-v` | Print each step |

### Examples

**Test chatbot:**
```bash
uv run /Users/terry/skills/flash-browse/flash_browse.py \
  --url "https://inmotion-faq.vercel.app" \
  --task "ask 'what are your opening hours' and report the response" \
  -v
```

**Fill a form:**
```bash
uv run /Users/terry/skills/flash-browse/flash_browse.py \
  --url "https://example.com/contact" \
  --task "fill name with 'Terry Li', email with 'test@example.com', then submit" \
  -v
```

**Navigate and extract:**
```bash
uv run /Users/terry/skills/flash-browse/flash_browse.py \
  --url "https://news.ycombinator.com" \
  --task "find the top 3 headlines and report them" \
  -v
```

## Requirements

- `OPENROUTER_API_KEY` environment variable
- `agent-browser` CLI installed
- `uv` for running with dependencies

## Cost

~$0.00005 per step. A 20-step task costs ~$0.001 (0.1 cents).
