---
name: llm-council
description: LLM Council with 5 frontier models (Opus 4.5, GPT-5.2, Gemini 3 Pro, Grok 4, Kimi K2). Models deliberate on a question, each seeing previous responses, then a judge synthesizes consensus. Use for important decisions needing diverse AI perspectives.
---

# LLM Council

5 frontier models deliberate on a question. Unlike `/multi-llm` which shows parallel responses, this creates an actual debate where models see and respond to previous speakers, followed by a judge synthesizing the consensus.

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

```bash
cd /Users/terry/skills/llm-council
uv run council.py "Should we use microservices or a monolith for this project?"
```

**Save transcript to file:**
```bash
uv run council.py "your question" --output transcript.md
```

**Named mode (show real model names instead of Speaker 1, 2, etc.):**
```bash
uv run council.py "your question" --named
```

**Multiple rounds (deeper deliberation):**
```bash
uv run council.py "your question" --rounds 3
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
| `--rounds N` | Number of deliberation rounds (default: 2, exits early on consensus) |
| `--output FILE` | Save transcript to file |
| `--named` | Show real model names (default is anonymous: Speaker 1, 2, etc.) |
| `--quiet` | Suppress progress output |

## Council Members

- Claude (claude-opus-4.5)
- GPT (gpt-5.2-pro)
- Gemini (gemini-3-pro-preview)
- Grok (grok-4)
- Kimi (kimi-k2-thinking)
- Judge: Claude Opus 4.5

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
| Speed | Fast (~10s) | Slower (~60-90s) |
| Use case | Quick comparison | Important decisions |

## How It Works

**True Deliberation Protocol:**
1. Claude speaks first, staking a clear position with key claims
2. Each subsequent model MUST explicitly AGREE, DISAGREE, or BUILD ON previous speakers by name
3. After each round, the system checks for consensus (4/5 agreement triggers early exit)
4. Judge synthesizes the full deliberation

**Engagement Requirements:**
- Models reference previous speakers by name (e.g., "I agree with Claude that..." or "GPT's point overlooks...")
- Explicit position statements prevent passive agreement
- Anti-sycophancy prompts encourage genuine disagreement

**Consensus Detection:**
- Looks for explicit "CONSENSUS:" statements
- Detects agreement language ("I agree with", "building on", "I concur")
- Exits early when 4/5 models align, saving time and tokens

**Live Streaming Output:**
- Responses stream token-by-token as they're generated
- See the discussion unfold in real-time
- Use `--quiet` to disable (waits for full response)

**Anonymous by Default (Karpathy-style):**
- Models see each other as "Speaker 1", "Speaker 2", etc.
- Prevents models from playing favorites based on vendor reputation
- Reduces sycophancy ("I agree with Claude because it's Claude")
- Identity legend revealed at the end of the transcript
- Use `--named` to show real model names instead

## Files

- Script: `/Users/terry/skills/llm-council/council.py`
- This skill: `/Users/terry/skills/llm-council/SKILL.md`
