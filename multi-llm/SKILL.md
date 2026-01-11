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

**Expensive mode (default)** - frontier models with thinking enabled:
```bash
cd /Users/terry/skills/multi-llm
uv run council.py "YOUR QUESTION HERE"
```

**Cheap mode** - fast and affordable:
```bash
uv run council.py "YOUR QUESTION HERE" --cheap
```

### Step 3: Present Results

The script outputs each model's response with clear separators. Present the responses to the user, highlighting:
- Key differences between models
- Points of agreement
- Which response might be most relevant to their use case

## Configuration

### Model Tiers

**Expensive (default)** - 2026 frontier models with thinking/reasoning:
- `anthropic/claude-opus-4.5` - Claude Opus 4.5
- `openai/gpt-5.2` - GPT-5.2
- `google/gemini-3-pro-preview` - Gemini 3 Pro
- `x-ai/grok-4.1` - Grok 4.1
- `deepseek/deepseek-r1` - DeepSeek R1

**Cheap** (`--cheap` flag) - fast and affordable:
- `anthropic/claude-sonnet-4` - Claude Sonnet 4
- `openai/gpt-4o` - GPT-4o
- `google/gemini-2.0-flash-001` - Gemini Flash
- `deepseek/deepseek-v3.2` - DeepSeek V3.2

### Options

| Flag | Description |
|------|-------------|
| `--cheap` | Use cheaper/faster models |
| `--no-thinking` | Disable reasoning mode for expensive models |
| `--timeout N` | Timeout in seconds (default: 60 cheap, 180 expensive) |
| `--models "a,b,c"` | Override with custom models |

### Examples

```bash
# Expensive with thinking (default)
uv run council.py "How should I architect a microservices system?"

# Cheap and fast
uv run council.py "What's the syntax for Python list comprehension?" --cheap

# Expensive without thinking
uv run council.py "Compare REST vs GraphQL" --no-thinking

# Custom models
uv run council.py "your question" --models "openai/o1,deepseek/deepseek-r1"
```

## Error Handling

- If a model fails, others continue (graceful degradation)
- Failed models show error message instead of response
- Script exits with error only if ALL models fail

## Files

- Script: `/Users/terry/skills/multi-llm/council.py`
- This skill: `/Users/terry/skills/multi-llm/SKILL.md`
