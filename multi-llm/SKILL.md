---
name: multi-llm
description: Query multiple LLMs in parallel via OpenRouter and compare their responses. Use when the user wants diverse perspectives from different models on a question.
---

# Multi-LLM Query

Query multiple LLMs simultaneously via OpenRouter and display their responses side-by-side. A simplified version of LLM Council that skips the review/synthesis stages for faster results.

## When to Use

Use this skill when the user:
- Wants to compare how different LLMs answer the same question
- Needs diverse perspectives on a coding problem or design decision
- Wants a quick "second opinion" from multiple models
- Is curious about model differences on a topic

## Prerequisites

1. **OpenRouter API key** - Get one at https://openrouter.ai
2. **Set environment variable**:
   ```bash
   export OPENROUTER_API_KEY=sk-or-v1-...
   ```
   Or add to `~/.zshrc` / `~/.bashrc`

## Instructions

### Step 1: Get the User's Question

Ask the user what question they want to send to the council, or use the question they already provided.

### Step 2: Run the Query Script

```bash
cd /Users/terry/skills/multi-llm
uv run council.py "YOUR QUESTION HERE"
```

### Step 3: Present Results

The script outputs each model's response with clear separators. Present the responses to the user, highlighting:
- Key differences between models
- Points of agreement
- Which response might be most relevant to their use case

## Configuration

### Default Models

The script queries these models by default:
- `anthropic/claude-sonnet-4` - Anthropic's Claude Sonnet
- `openai/gpt-4o` - OpenAI's GPT-4o
- `google/gemini-2.0-flash-001` - Google's Gemini Flash
- `x-ai/grok-3` - xAI's Grok 3

### Custom Models

Override models with the `--models` flag:

```bash
uv run council.py "your question" --models "openai/gpt-4o,anthropic/claude-opus-4"
```

### Timeout

Default timeout is 60 seconds. Increase for complex questions:

```bash
uv run council.py "your question" --timeout 120
```

## Available Models

Popular OpenRouter models include:
- `anthropic/claude-opus-4` - Claude Opus 4
- `anthropic/claude-sonnet-4` - Claude Sonnet 4
- `openai/gpt-4o` - GPT-4o
- `openai/o1` - OpenAI o1
- `google/gemini-2.0-flash-001` - Gemini Flash
- `google/gemini-2.5-pro-preview` - Gemini 2.5 Pro
- `x-ai/grok-2-1212` - Grok 2
- `deepseek/deepseek-chat` - DeepSeek

See full list at https://openrouter.ai/models

## Example Output

```
============================================================
anthropic/claude-sonnet-4
============================================================
[Claude's response here]

============================================================
openai/gpt-4o
============================================================
[GPT-4o's response here]

============================================================
google/gemini-2.0-flash-001
============================================================
[Gemini's response here]
```

## Error Handling

- If a model fails, others continue (graceful degradation)
- Failed models show error message instead of response
- Script exits with error only if ALL models fail

## Files

- Script: `/Users/terry/skills/multi-llm/council.py`
- This skill: `/Users/terry/skills/multi-llm/SKILL.md`
