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

## Prompting Tips

**For social/conversational contexts** (interview questions, networking messages, outreach):

LLMs tend to over-optimize for thoroughness and information extraction. When you ask "what questions should I ask in an interview?", they'll produce structured, multi-part diagnostic questions that sound like an interrogation, not a conversation.

**Fix:** Explicitly include constraints like:
- "Make it feel like a natural conversation, not a candidate asking strategic questions"
- "Something you'd actually ask over coffee"
- "Simple and human, not structured and comprehensive"

A simple "What's kept you here for 10 years?" often beats a carefully crafted "When engagements fail, who owns the narrative and how is responsibility assigned in performance reviews?"

The council optimizes for strategy; sometimes you need to optimize for being human.

**Match context depth to question type:**

- **Strategic decisions** (career moves, negotiations, trade-offs): provide rich context — full background, constraints, risks, history. Models need the full picture.
- **Social/conversational questions** (interview questions, outreach messages, networking): provide minimal context + clear tone constraints. Too much context leads to over-optimization.

The constraint ("make it natural") often does more work than the context.

## Prerequisites

**OpenRouter API key** (required):
```bash
export OPENROUTER_API_KEY=sk-or-v1-...
```

**Google AI Studio key** (optional, enables Gemini fallback):
```bash
export GOOGLE_API_KEY=AIza...
```

**Moonshot API key** (optional, enables Kimi fallback):
```bash
export MOONSHOT_API_KEY=sk-...
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

**Named mode (let models see each other's real names - may increase bias):**
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

**Skip blind phase (faster but more anchoring bias):**
```bash
uv run council.py "your question" --no-blind
```

**Add context for the judge:**
```bash
uv run council.py "your question" --context "architecture decision"
```

**Share via secret Gist:**
```bash
uv run council.py "your question" --share  # → prints gist URL
```

## Options

| Flag | Description |
|------|-------------|
| `--rounds N` | Number of deliberation rounds (default: 2, exits early on consensus) |
| `--output FILE` | Save transcript to file |
| `--named` | Let models see real names during deliberation (may increase bias) |
| `--no-blind` | Skip blind first-pass (faster, but first speaker anchors others) |
| `--context TEXT` | Context hint for judge (e.g., "architecture decision", "ethics question") |
| `--share` | Upload transcript to secret GitHub Gist and print URL |
| `--social` | Enable social calibration mode (auto-detected for interview/networking questions) |
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
### claude-opus-4.5
For a startup, I'd lean toward monolith initially. Microservices add operational
complexity that's hard to justify without a large team...

### gpt-5.2-pro
I partially agree with claude-opus-4.5 on starting simple, but I'd push back on
the "monolith first" dogma. If you have clear domain boundaries...

### gemini-3-pro-preview
Building on both points: the real question isn't architecture pattern, it's
team structure. Conway's Law applies here...

### Judge
## Points of Agreement
All council members agree that team size and operational maturity matter more
than the architecture pattern itself...

## Points of Disagreement
claude-opus-4.5 emphasizes simplicity-first, gpt-5.2-pro argues for forward-looking design...

## Synthesis
The council converges on a "modular monolith" approach...

## Recommendation
Start with a modular monolith with clear domain boundaries...
```

## vs /multi-llm

| Aspect | /multi-llm | /llm-council |
|--------|-----------|--------------|
| Pattern | Parallel queries | Blind claims → Deliberation → Synthesis |
| Output | Side-by-side responses | Consensus with reasoning |
| Speed | Fast (~10s) | ~60-90s (parallel blind), ~45-60s (--no-blind) |
| Use case | Quick comparison | Important decisions |

## How It Works

**Blind First-Pass (Anti-Anchoring):**
1. All models generate short "claim sketches" INDEPENDENTLY and IN PARALLEL (~15-25s)
2. This prevents the "first speaker lottery" where whoever speaks first anchors the debate
3. Each model commits to an initial position before seeing any other responses
4. Use `--no-blind` to skip this phase for speed

**Deliberation Protocol:**
1. All models see everyone's blind claims, then deliberate
2. Each model MUST explicitly AGREE, DISAGREE, or BUILD ON previous speakers by name
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
- Thinking models (Gemini 3 Pro, Kimi K2) use non-streaming with "(thinking...)" indicator
- Use `--quiet` to disable (waits for full response)

**Retry Logic for Thinking Models:**
- Thinking models can be flaky via OpenRouter (intermittent empty responses)
- Built-in retry (up to 3 attempts) for failed or empty responses
- If a model fails after retries, shows "[No response from model after 3 attempts]"
- Council continues with remaining models; judge synthesizes available responses

**Fallbacks for Flaky Models:**
- **Gemini**: If `GOOGLE_API_KEY` is set, falls back to AI Studio (`gemini-2.5-pro`) when OpenRouter fails
- **Kimi**: If `MOONSHOT_API_KEY` is set, falls back to Moonshot API (`kimi-k2`) when OpenRouter fails
- Helps work around OpenRouter reliability issues with thinking models

**Anonymous Deliberation, Readable Output (Karpathy-style):**
- Models see each other as "Speaker 1", "Speaker 2", etc. during deliberation
- Prevents models from playing favorites based on vendor reputation
- Reduces sycophancy ("I agree with Claude because it's Claude")
- Output transcript shows real model names for readability
- Use `--named` to let models also see real names (may increase bias)

**History Logging:**
- Each council run is logged to `council_history.jsonl` (JSONL format)
- Tracks: timestamp, question, context, rounds, models used
- Useful for reviewing past deliberations

**Social Calibration Mode:**
- Auto-detected when question contains: "interview", "ask him/her", "networking", "outreach", "message", etc.
- Or enable explicitly with `--social` flag
- Adds conversational constraints to all speakers: "feel natural, not like strategic interrogation"
- Assigns devil's advocate role to one speaker to challenge the premise
- Judge includes "Social Calibration Check" section to sanity-check if output is human-appropriate
- Helps avoid over-optimized, tone-deaf outputs for social contexts

**Model Failure Warnings:**
- Failed models are prominently displayed at the end of output
- Shows which models failed and why (HTTP errors, timeouts, empty responses)
- Reports how many models actually contributed: "Council ran with 3/5 models"

## Known Limitations

1. **~~No social calibration~~** ✅ FIXED — Use `--social` flag or let auto-detection handle it. Social mode adds conversational constraints, devil's advocate role, and judge calibration check.

2. **~~Models don't question the premise~~** ✅ FIXED — One speaker (3rd) is now assigned devil's advocate role to challenge the framing.

3. **Judge follows the herd** — The synthesis faithfully reflects the deliberation. In social mode, the judge now includes a calibration check, but may still over-index on consensus.

4. **~~Model failures can be silent~~** ✅ FIXED — Failed models are now prominently displayed at the end with a summary of how many models contributed.

## Remaining Improvements (Ideas)

- Stage awareness for multi-round processes (interviews, negotiations)
- Allow user to specify which speaker gets devil's advocate role
- Add "re-run with social mode" suggestion when output seems over-optimized

## Files

- Script: `/Users/terry/skills/llm-council/council.py`
- History: `/Users/terry/skills/llm-council/council_history.jsonl`
- This skill: `/Users/terry/skills/llm-council/SKILL.md`
