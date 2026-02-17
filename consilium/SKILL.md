---
name: consilium
description: 4 frontier models deliberate, then Claude judges. ~$0.50/run — use for any question worth 5+ minutes of thought.
github_url: https://github.com/terry-li-hm/consilium
github_hash: e8043f3
user_invocable: true
---

# LLM Council

4 frontier models deliberate on a question, then Claude Opus 4.5 judges and adds its own perspective. Unlike `/ask-llms` which shows parallel responses, this creates an actual debate where models see and respond to previous speakers, with a rotating challenger ensuring sustained disagreement.

## When to Use

At ~$0.50/run, the cost threshold is negligible. Use whenever:

- **Any question worth >5 minutes of deliberation** — the council is cheaper than your time
- You want models to actually debate, not just answer in parallel
- You need a synthesized recommendation, not raw comparison
- Exploring trade-offs where different viewpoints matter
- **Brainstorming and exploration** — free-flow intellectual discussion, not just binary decisions
- Questions with cognitive, social, or behavioural dimensions (council catches hidden angles Claude underestimates)

## When NOT to Use

- **Thinking out loud** — exploratory discussions where you're still forming the question
- **Claude has good context** — if we've been discussing the topic, direct conversation is faster
- **Personal preference** — council excels at objective trade-offs, not "what would I enjoy"
- **Physical/visual data required** — if the answer depends on seeing something (body fit, face shape, appearance), council reasons from theory only and produces generic advice. Go try it in person instead
- **Already converged** — if discussion reached a conclusion, council just validates
- **Speed matters** — takes 60-90s (cost is negligible at ~$0.50)

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

**Basic usage (--quiet since Claude reads the transcript, not the terminal):**
```bash
uv tool run consilium "Should we use microservices or a monolith?" --quiet \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

> **Always save transcripts to vault.** Use `--output ~/notes/Councils/LLM Council - {Topic} - {date}.md`. `/tmp/` files get wiped on reboot — you lose the raw reasoning.

> **Note:** Always use `uv tool run consilium` instead of bare `consilium`. The mise shim points to system Python which can't find the module.

**With structured output (recommended for agent workflows):**
```bash
uv tool run consilium "Should I accept the Standard Chartered offer?" \
  --quiet \
  --format json \
  --persona "$PERSONA" \
  --context "job-offer"
```

**Common options:**
```bash
uv tool run consilium "question" --format json           # Machine-parseable output
uv tool run consilium "question" --format yaml           # Structured but readable
uv tool run consilium "question" --social                # Interview/networking questions
uv tool run consilium "question" --persona "context"     # Add personal context
uv tool run consilium "question" --rounds 3              # More deliberation
uv tool run consilium "question" --output file.md        # Save transcript
uv tool run consilium "question" --share                 # Upload to secret Gist
uv tool run consilium "question" --domain banking        # Inject regulatory context
uv tool run consilium "question" --challenger gemini     # Assign contrarian role
uv tool run consilium "question" --followup              # Interactive drill-down after synthesis
uv tool run consilium "question" --practical             # Actionable rules only, no philosophy
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

## Known Issues

- **JSON output truncation:** Use `--output file.md` to capture full transcript
- **Follow-up:** Use `--followup` flag for interactive drill-down after synthesis

## Output Formats

| Format | Use Case |
|--------|----------|
| `prose` (default) | Human reading, exploratory |
| `json` | Agent workflows, parsing, automation |
| `yaml` | Human-readable structured output |

## See Also

- Repository: https://github.com/terry-li-hm/consilium
- PyPI: https://pypi.org/project/consilium/
- Plan: `/Users/terry/skills/plans/2026-01-31-feat-consilium-claude-code-integration-plan.md`
