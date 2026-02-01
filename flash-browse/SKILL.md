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

---

# chatbot_tester

Deterministic chatbot testing — no AI in the loop, just systematic Q&A extraction.

## When to use

- Testing your FAQ chatbot with many questions
- Batch verification of chatbot responses
- Regression testing after chatbot updates

## Usage

```bash
# Single question
uv run /Users/terry/skills/flash-browse/chatbot_tester.py \
  --url "https://inmotion-faq.vercel.app" \
  --questions "what are your opening hours"

# Multiple questions (comma-separated)
uv run /Users/terry/skills/flash-browse/chatbot_tester.py \
  --url "https://inmotion-faq.vercel.app" \
  --questions "question 1,question 2,question 3" \
  --output results.json

# Questions from file (one per line)
uv run /Users/terry/skills/flash-browse/chatbot_tester.py \
  --url "https://inmotion-faq.vercel.app" \
  --questions questions.txt \
  --output results.json \
  -v
```

### Options

| Flag | Description |
|------|-------------|
| `--url` | Chatbot URL (required) |
| `--questions` | Comma-separated questions OR path to file |
| `--output` | Save results as JSON |
| `--verbose`, `-v` | Show browser commands |

## Output

Prints each Q&A pair. With `--output`, saves JSON:
```json
[
  {"question": "...", "response": "...", "error": null},
  ...
]
```
