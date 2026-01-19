---
name: llm-council
description: Karpathy-style LLM Council using AutoGen. Multiple models deliberate on a question and a judge synthesizes consensus. Use for important decisions needing diverse AI perspectives.
---

# LLM Council

Multi-model deliberation using AutoGen's RoundRobinGroupChat. Unlike `/multi-llm` which just shows parallel responses, this creates an actual debate where models respond to each other, followed by a judge synthesizing the consensus.

## When to Use

Use this skill when:
- Making an important decision that benefits from diverse perspectives
- You want models to actually debate, not just answer in parallel
- You need a synthesized recommendation, not raw comparison
- Exploring trade-offs where different viewpoints matter

For quick parallel comparisons, use `/multi-llm` instead (faster, simpler).

## Prerequisites

**OpenRouter API key** set in environment:
```bash
export OPENROUTER_API_KEY=sk-or-v1-...
```

## Instructions

### Step 1: Get the Question

Ask the user what question they want the council to deliberate, or use the question they provided.

### Step 2: Run the Council

**Standard (3 frontier models deliberate, then judge synthesizes):**
```bash
cd /Users/terry/skills/llm-council
uv run council.py "Should we use microservices or a monolith for this project?"
```

**Cheap mode (faster, less expensive):**
```bash
uv run council.py "your question" --cheap
```

**Multiple rounds (deeper deliberation):**
```bash
uv run council.py "your question" --rounds 2
```

### Step 3: Present the Synthesis

The judge's output includes:
- **Points of Agreement** - Where all models align
- **Points of Disagreement** - Different perspectives and why
- **Synthesis** - Integrated view
- **Recommendation** - Final guidance

Present this to the user, highlighting the key insights.

## Options

| Flag | Description |
|------|-------------|
| `--cheap` | Use cheaper/faster models (haiku, gpt-4o-mini, gemini-flash-lite) |
| `--rounds N` | Number of deliberation rounds before judge (default: 1) |
| `--quiet` | Suppress progress output |

## Council Members

**Expensive (default):**
- Claude (claude-sonnet-4)
- GPT (gpt-4o)
- Gemini (gemini-2.0-flash)
- Judge: Claude Sonnet 4

**Cheap (`--cheap`):**
- Claude (claude-3.5-haiku)
- GPT (gpt-4o-mini)
- Gemini (gemini-2.0-flash-lite)
- Judge: Claude Sonnet 4

## Example Output

```
### ClaudeAgent
For a startup, I'd lean toward monolith initially. Microservices add operational
complexity that's hard to justify without a large team...

### GPTAgent
I partially agree with Claude on starting simple, but I'd push back on the
"monolith first" dogma. If you have clear domain boundaries...

### GeminiAgent
Building on both points: the real question isn't architecture pattern, it's
team structure. Conway's Law applies here...

### Judge
## Points of Agreement
All council members agree that team size and operational maturity matter more
than the architecture pattern itself...

## Points of Disagreement
Claude emphasizes simplicity-first, GPT argues for forward-looking design...

## Synthesis
The council converges on a "modular monolith" approach...

## Recommendation
Start with a modular monolith with clear domain boundaries...
```

## vs /multi-llm

| Aspect | /multi-llm | /llm-council |
|--------|-----------|--------------|
| Pattern | Parallel queries | Deliberation + synthesis |
| Output | Side-by-side responses | Consensus with reasoning |
| Speed | Fast (~10s) | Slower (~30-60s) |
| Use case | Quick comparison | Important decisions |
| Framework | Raw httpx | AutoGen |

## Files

- Script: `/Users/terry/skills/llm-council/council.py`
- This skill: `/Users/terry/skills/llm-council/SKILL.md`
