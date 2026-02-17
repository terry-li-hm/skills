---
name: consilium
description: Multi-model deliberation — full council (~$0.50) or quick parallel (~$0.10). Use for any question worth 5+ minutes of thought.
github_url: https://github.com/terry-li-hm/consilium
github_hash: e8043f3
user_invocable: true
---

# LLM Council

4 frontier models deliberate on a question, then Claude Opus 4.5 judges and adds its own perspective. Models see and respond to previous speakers, with a rotating challenger ensuring sustained disagreement.

**Future:** `/ask-llms` will fold into consilium as `--quick` mode (parallel queries, no debate). Until then, use `/ask-llms` directly for quick parallel comparisons.

## Routing: Which Mode?

```
Does the question have a single correct answer? (specs, facts, how-to)
  YES → Web search or ask Claude directly
  NO ↓
Is this personal preference / physical / visual? (glasses, photos, food)
  YES → Try it in person, or ask Claude directly
  NO ↓
Do you need multiple perspectives but not debate?
  YES → /ask-llms (parallel, ~$0.10)
  NO ↓
Are there genuine trade-offs requiring deliberation?
  YES → /consilium (full council, ~$0.50)
```

## When to Use

At ~$0.50/run, the cost threshold is negligible. Use whenever:

- **Genuine trade-offs with competing values** — the sweet spot (CV positioning, governance frameworks, architecture decisions)
- **Domain-specific professional decisions** — regulatory, career, strategic
- You need a synthesized recommendation, not raw comparison
- Questions with cognitive, social, or behavioural dimensions (council catches hidden angles Claude underestimates)
- **Stress-testing a plan** — "what would make this fail?"
- **Iterating on a previous council** — second passes go deeper

## When NOT to Use

- **Single correct answer** — photo crop rules, product specs, naming preferences. Use web search or a single model
- **Personal preference / physical** — glasses frames, food, clothing. Council reasons from theory; go try it in person instead
- **Thinking out loud** — exploratory discussions where you're still forming the question
- **Claude has good context** — if we've been discussing the topic, direct conversation is faster
- **Already converged** — if discussion reached a conclusion, council just validates
- **Speed matters** — takes 60-90s
- **Naming exercises** — council debates taste in circles. Use one model to brainstorm candidates, then registry-check. Council only if evaluating a shortlist against specific criteria

## Prerequisites

```bash
# Install (one-time)
uv tool install consilium

# Or install from local dev:
cd ~/code/consilium && pip install -e .

# API keys
export OPENROUTER_API_KEY=sk-or-v1-...    # Required
export GOOGLE_API_KEY=AIza...              # Optional: Gemini fallback
export MOONSHOT_API_KEY=sk-...             # Optional: Kimi fallback
```

## Instructions

### Step 0: Suitability Check

Before running the council, evaluate the question against the routing table above. If the question falls into "When NOT to Use", redirect:

- **Factual/single-answer** → answer directly or web search
- **Personal preference** → "This is better answered by trying it in person"
- **Naming** → brainstorm candidates with a single model first, then offer council to evaluate shortlist
- **Quick parallel opinions** → suggest `/ask-llms` instead

Only proceed to Step 1 if the question involves genuine trade-offs or domain-specific judgment.

### Step 1: Get the Question

Ask the user what question they want the council to deliberate, or use the question they provided.

### Step 2: Gather Context (for important decisions)

For job/career decisions, read relevant vault files and compose into `--persona`:

```bash
# Read context files
CLAUDE_MD=$(cat /Users/terry/notes/CLAUDE.md | head -100)
PIPELINE=$(cat "/Users/terry/notes/Capco Transition.md" | head -50)

# Compose persona
PERSONA="Background: Terry is AGM & Head of Data Science at CITIC, being counselled out.
Current pipeline: $PIPELINE"
```

For other decisions, use simpler context or skip this step.

### Step 3: Run the Council

**Always use these flags:**
- `--quiet` — Claude reads the transcript, not the terminal
- `--format json` — ensures cost/duration metadata is captured
- `--output ~/notes/Councils/LLM Council - {Topic} - {date}.md` — vault persistence

> **Note:** Always use `uv tool run consilium` instead of bare `consilium`. The mise shim points to system Python which can't find the module.

**Standard invocation:**
```bash
uv tool run consilium "Should we use microservices or a monolith?" \
  --quiet --format json \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**With persona context (career/professional decisions):**
```bash
uv tool run consilium "Should I accept the Standard Chartered offer?" \
  --quiet --format json \
  --persona "$PERSONA" \
  --context "job-offer" \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Common additional flags:**
```bash
--social                # Interview/networking questions
--persona "context"     # Add personal context
--rounds 3              # More deliberation (default: 1)
--domain banking        # Inject regulatory context (banking|healthcare|eu|fintech|bio)
--challenger gemini     # Assign contrarian role
--followup              # Interactive drill-down after synthesis
--practical             # Actionable rules only, no philosophy
--share                 # Upload to secret Gist
```

**Domain-specific deliberation (banking, healthcare, etc.):**
```bash
uv tool run consilium "Should we build an agent for KYC?" \
  --domain banking \
  --challenger gemini \
  --followup \
  --output counsel.md
```

Available domains: `banking`, `healthcare`, `eu`, `fintech`, `bio`

### Step 4: Parse and Present (when using --format json)

When using `--format json`, the output ends with a JSON block after `---`:

```json
{
  "schema_version": "1.0",
  "question": "Should I accept the Standard Chartered offer?",
  "decision": "Accept the offer with negotiation on start date",
  "confidence": "high",
  "reasoning_summary": "Council agreed that...",
  "dissents": [{"model": "Grok", "concern": "Consider counter-offer timing"}],
  "action_items": [
    {"action": "Send acceptance email", "priority": "high"},
    {"action": "Negotiate start date", "priority": "medium"}
  ],
  "meta": {
    "timestamp": "2026-01-31T14:30:00",
    "models_used": ["claude-opus-4.5", "gpt-5.2", "gemini-3-pro", "grok-4", "kimi-k2.5"],
    "rounds": 2,
    "duration_seconds": 67,
    "estimated_cost_usd": 0.53
  }
}
```

Parse this and present:
1. **Decision** with confidence level
2. **Key reasoning** (summary)
3. **Dissenting views** (if any)
4. **Claude's critique** — did they miss anything? Does it fit Terry's context?

### Step 5: Offer Follow-Up Actions

After presenting the council's recommendation, use AskUserQuestion:

**Question:** "What would you like to do with this decision?"

**Options:**
1. **Create tasks** — Add action_items to task list
2. **Save to vault** — Create decision record in `~/notes/Councils/`
3. **Draft messages** — Draft follow-up messages based on action_items
4. **Just note it** — No further action needed

### Step 6: Execute Selected Action

**If "Create tasks":**
Use TaskCreate for each action_item with appropriate priority.

**If "Save to vault":**
Create note at `~/notes/Councils/LLM Council - {Topic} - {YYYY-MM-DD}.md`:

```markdown
---
date: {date}
type: decision
question: "{question}"
status: pending
decision: "{decision}"
confidence: {confidence}
participants:
  - claude-opus-4.5
  - gpt-5.2
  - gemini-3-pro
  - grok-4
  - kimi-k2.5
tags:
  - decision
  - consilium
---

**Related:** [[Capco Transition]] | [[Job Hunting]]

# {Title from question}

## Question
{question}

## Decision
{decision}

## Reasoning
{reasoning_summary}

## Dissents
{for each dissent: - **{model}:** {concern}}

## Action Items
{for each action: - [ ] {action}}

---
*Council convened: {date} | {models count} models | {rounds} rounds | ~${cost}*
```

**If "Draft messages":**
Review action_items and offer to draft relevant messages (acceptance emails, follow-ups, etc.)

## Prompting Tips

**For social/conversational contexts** (interview questions, networking, outreach):

LLMs over-optimize for thoroughness. Add constraints like:
- "Make it feel like a natural conversation"
- "Something you'd actually ask over coffee"
- "Simple and human, not structured and comprehensive"

**Match context depth to question type:**
- Strategic decisions: provide rich context (full background, constraints, history)
- Social questions: minimal context + clear tone constraints

**For architecture/design questions:**

Provide scale and constraints upfront to avoid premature optimization advice:
- "This is a single-user system" (avoids multi-user concerns)
- "We have 500 notes, not 50,000" (avoids scaling infrastructure)
- "Manual processes are acceptable" (avoids automation overkill)

Without these constraints, council tends to suggest infrastructure for problems that don't exist yet.

**For skill/tool design questions:**

Council optimizes for architecture but often misses input edge cases. Add:
- "What input variations should this handle?" (e.g., URLs vs pasted content)
- "What edge cases might break this?" (e.g., hybrid content types)
- "What would make users reach for a different tool instead?"

This stress-tests the input surface, not just the processing logic.

**For domain-specific questions (banking, healthcare, etc.):**

Use `--domain` flag to auto-inject regulatory context:
```bash
uv tool run consilium "question" --domain banking   # HKMA/MAS/FCA, MRM requirements
uv tool run consilium "question" --domain healthcare # HIPAA constraints
uv tool run consilium "question" --domain eu        # GDPR/AI Act considerations
```

This surfaces compliance concerns early rather than as afterthoughts.

## Model Tendencies

| Model | Tendency | Useful For |
|-------|----------|------------|
| **GPT-5.2** | Practical, implementation-focused | Actionable steps |
| **Gemini 3 Pro** | Technical depth, systems thinking | Architecture |
| **Grok 4** | Contrarian, challenges consensus | Stress-testing ideas |
| **Kimi K2.5** | Detail-oriented, edge cases | Completeness check |
| **Claude Opus 4.5** (Judge) | Balanced, safety-conscious | Synthesis |

**Default challenger:** GPT (rotates each round). Grok is naturally contrarian regardless, so GPT as explicit challenger gives two sources of pushback.

**Override:** `--challenger gemini` (architecture), `--challenger grok` (max pushback), `--challenger kimi` (edge cases).

## Key Lessons

See `[[Frontier Council Lessons]]` for full usage lessons. Critical ones:

- **Add constraints upfront** — models default to enterprise-grade without "this is a POC" / "single-user" / "speed > perfection"
- **Include real metrics** for optimization questions, not just descriptions
- **Use `--practical`** for operational questions (models spiral into philosophy otherwise)
- **Trust the judge's framing over its action list** — it diagnoses well but over-aggregates prescriptions
- **Challenger round is the highest-value component** — GPT-5.2 as explicit challenger consistently produces the best single insight
- **Iterative councils beat single deep runs** — second pass on same topic goes deeper with sharper framing
- **Blind phase often produces agreement, not debate** — the real value comes from challenger + judge. Consider `--no-blind` for topics where you expect convergence
- **Front-load constraints in the question** — "this must work for HKMA-regulated banks" produces tighter output than "how should banks govern AI?"

## Known Issues

- **Kimi-K2.5 timeouts:** Timed out in ~20% of recent councils (3/14). Partial outputs add noise. If Kimi times out, the council still works but with 3 useful speakers instead of 4. Consider filing an issue to add timeout fallback or model substitution
- **JSON output truncation:** Use `--output file.md` to capture full transcript
- **Follow-up:** Use `--followup` flag for interactive drill-down after synthesis

## Output Formats

| Format | Use Case |
|--------|----------|
| `prose` (default) | Human reading, exploratory |
| `json` | Agent workflows, parsing, automation |
| `yaml` | Human-readable structured output |

## Roadmap

- **`--quick` mode:** Fold `/ask-llms` into consilium as a parallel-only mode (no debate, ~$0.10). Eliminates the routing decision between two tools
- **Kimi fallback:** Auto-substitute on timeout instead of partial output
- **Outcome tracking:** Add `## Outcome (Post-Decision)` template to transcripts

## See Also

- Repository: https://github.com/terry-li-hm/consilium
- PyPI: https://pypi.org/project/consilium/
- Plan: `/Users/terry/skills/plans/2026-01-31-feat-consilium-claude-code-integration-plan.md`
- Related skill: `/ask-llms` (parallel queries, future `--quick` mode)
