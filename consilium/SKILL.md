---
name: consilium
description: Multi-model deliberation — auto-routes by difficulty. Full council (~$0.50), quick parallel (~$0.10), red team (~$0.20), and more.
github_url: https://github.com/terry-li-hm/consilium
github_hash: 7b804ef
user_invocable: true
---

# LLM Council

5 frontier models deliberate on a question, then Claude Opus 4.6 judges and adds its own perspective. Models see and respond to previous speakers, with a rotating challenger ensuring sustained disagreement. Auto-routes by difficulty — simple questions get quick parallel, complex ones get full council.

## Modes

| Mode | Flag | Cost | Description |
|------|------|------|-------------|
| Auto (default) | *(none)* | varies | Opus classifies difficulty, picks quick or council |
| Quick | `--quick` | ~$0.10 | Parallel queries, no debate/judge |
| Council | `--council` | ~$0.50 | Full multi-round debate + judge |
| Discuss | `--discuss` | ~$0.30 | Hosted roundtable exploration |
| Socratic | `--socratic` | ~$0.30 | Probing questions to expose assumptions |
| Oxford | `--oxford` | ~$0.40 | Binary for/against with rebuttals + verdict |
| Red Team | `--redteam` | ~$0.20 | Adversarial stress-test of a plan |
| Solo | `--solo` | ~$0.40 | Claude debates itself in multiple roles |

## Routing: Which Mode?

```
Does the question have a single correct answer? (specs, facts, how-to)
  YES → Web search or ask Claude directly
  NO ↓
Is this personal preference / physical / visual? (glasses, photos, food)
  YES → Try it in person, or ask Claude directly
  NO ↓
Do you need multiple perspectives but not debate?
  YES → consilium --quick (or /ask-llms)
  NO ↓
Do you want to stress-test a specific plan?
  YES → consilium --redteam
  NO ↓
Are there genuine trade-offs requiring deliberation?
  YES → consilium (auto-routes, or --council to force full debate)
```

## When to Use

At ~$0.50/run, the cost threshold is negligible. Use whenever:

- **Genuine trade-offs with competing values** — the sweet spot (CV positioning, governance frameworks, architecture decisions)
- **Domain-specific professional decisions** — regulatory, career, strategic
- You need a synthesized recommendation, not raw comparison
- Questions with cognitive, social, or behavioural dimensions (council catches hidden angles Claude underestimates)
- **Stress-testing a plan** — `--redteam` for adversarial, `--socratic` for assumption-probing
- **Iterating on a previous council** — second passes go deeper

## When NOT to Use

- **Single correct answer** — photo crop rules, product specs, naming preferences. Use web search or a single model
- **Personal preference / physical** — glasses frames, food, clothing. Council reasons from theory; go try it in person instead
- **Thinking out loud** — exploratory discussions where you're still forming the question
- **Claude has good context** — if we've been discussing the topic, direct conversation is faster
- **Already converged** — if discussion reached a conclusion, council just validates
- **Speed matters** — takes 60-90s for full council
- **Naming exercises** — council debates taste in circles. Use one model to brainstorm candidates, then registry-check. Council only if evaluating a shortlist against specific criteria

## Prerequisites

```bash
# Install (one-time)
uv tool install consilium

# Or install from local dev:
cd ~/code/consilium && uv tool install --force --reinstall .

# API keys
export OPENROUTER_API_KEY=sk-or-v1-...    # Required
export GOOGLE_API_KEY=AIza...              # Optional: Gemini fallback
```

## Instructions

### Step 0: Suitability Check

Before running the council, evaluate the question against the routing table above. If the question falls into "When NOT to Use", redirect:

- **Factual/single-answer** → answer directly or web search
- **Personal preference** → "This is better answered by trying it in person"
- **Naming** → brainstorm candidates with a single model first, then offer council to evaluate shortlist
- **Quick parallel opinions** → `--quick`

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
PERSONA="Background: Terry is Principal Consultant / AI Solution Lead at Capco.
Current context: $PIPELINE"
```

For other decisions, use simpler context or skip this step.

### Step 3: Run the Council

**Always use these flags:**
- `--format json` — ensures cost/duration metadata is captured
- `--output ~/notes/Councils/LLM Council - {Topic} - {date}.md` — vault persistence

**Do NOT use `--quiet` by default.** Run with `run_in_background: true` on the Bash tool so the user can watch live via `consilium --watch` in another tmux tab. Read the `--output` file when the task completes.

> **Note:** Always use `uv tool run consilium` instead of bare `consilium`. The mise shim points to system Python which can't find the module.

**Standard invocation (auto-routes by difficulty):**
```bash
uv tool run consilium "Should we use microservices or a monolith?" \
  --format json \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Force full council with persona context:**
```bash
uv tool run consilium "Should I accept the Standard Chartered offer?" \
  --council --format json \
  --persona "$PERSONA" \
  --context "job-offer" \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Red team a plan:**
```bash
uv tool run consilium "My plan: migrate the monolith to microservices over 6 months..." \
  --redteam \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Common additional flags:**
```bash
--persona "context"     # Add personal context
--rounds 3              # More deliberation (default: 1)
--domain banking        # Inject regulatory context (banking|healthcare|eu|fintech|bio)
--challenger gemini     # Assign contrarian role
--decompose             # Break complex question into sub-questions before blind phase
--followup              # Interactive drill-down after synthesis
--share                 # Upload to secret Gist
--quiet                 # Suppress live output (when user doesn't need to watch)
```

**Oxford debate (binary decisions):**
```bash
uv tool run consilium "Should we use microservices?" --oxford
uv tool run consilium "Hire seniors or train juniors?" --oxford --motion "This house believes..."
```

**Solo council (Claude debates itself in roles):**
```bash
uv tool run consilium "Pricing strategy" --solo --roles "investor,founder,customer"
uv tool run consilium --list-roles  # See predefined roles
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
    "models_used": ["GPT", "Gemini", "Grok", "DeepSeek", "GLM"],
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
5. **Static note candidates** — if the judge proposed any, flag them for review

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
participants: {from meta.models_used}
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

## Session Management

```bash
consilium --sessions              # List recent sessions
consilium --stats                 # Cost breakdown by mode
consilium --watch                 # Live tail from another tmux tab
consilium --view                  # View latest session in pager
consilium --view "career"         # View session matching term
consilium --search "career"       # Search all session content
```

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
| **DeepSeek R1** | Analytical, thorough reasoning | Deep analysis |
| **GLM-5** | Strategic, pragmatic | Business decisions |
| **Claude Opus 4.6** (Judge) | Balanced, integrates critique | Synthesis |

**Default challenger:** GPT (rotates each round). Grok is naturally contrarian regardless, so GPT as explicit challenger gives two sources of pushback.

**Override:** `--challenger gemini` (architecture), `--challenger grok` (max pushback).

## Research Foundations

Consilium's architecture is grounded in group deliberation research. See `[[Group Deliberation Research - Consilium Design]]` for full synthesis with sources.

**Why the blind phase matters most** (Surowiecki, Delphi, Tetlock): Independence before exposure is the single most validated principle. The blind phase captures independent positions before herding kicks in. These outputs should weigh heavily in final synthesis.

**Why the challenger works** (Nemeth 2001): Assigned devil's advocates produce bolstering, not reconsideration. Consilium mitigates this by framing the challenger with questions (not assertions) and different epistemic priors — but the limitation is real. Authentic dissent > role-played dissent.

**Why convergence is a strong signal** (Tetlock/GJP): When independent agents with different models/priors agree, the evidence is multiplicative. The judge should extremize convergent conclusions — push confidence further than a simple average.

**Why sycophancy is the #1 risk** (ICLR 2025, ACL 2025): Multi-agent debate produces "correct-to-incorrect" flips that exceed improvements. Position changes without new evidence are sycophancy, not reasoning. The debate and judge prompts include anti-sycophancy measures.

**Why the judge uses ACH** (Heuer/CIA): Analysis of Competing Hypotheses — list competing conclusions, evaluate evidence against each, eliminate rather than confirm. This counters confirmation bias in synthesis.

**What consilium can't fix** (MAD literature): Most of the apparent value of multi-agent debate comes from generating multiple independent samples, not from the debate itself. Consilium's real value is divergent thinking (strategy, framing, angles) — not convergent reasoning (math, facts).

## Key Lessons

See `[[Frontier Council Lessons]]` for full usage lessons. Critical ones:

- **Add constraints upfront** — models default to enterprise-grade without "this is a POC" / "single-user" / "speed > perfection"
- **Include real metrics** for optimization questions, not just descriptions
- **Trust the judge's framing over its action list** — it diagnoses well but over-aggregates prescriptions
- **Challenger round is the highest-value component** — GPT-5.2 as explicit challenger consistently produces the best single insight
- **Iterative councils beat single deep runs** — second pass on same topic goes deeper with sharper framing
- **Blind phase often produces agreement, not debate** — the real value comes from challenger + judge
- **Front-load constraints in the question** — "this must work for HKMA-regulated banks" produces tighter output than "how should banks govern AI?"
- **Critic phase catches real gaps** — the Gemini critique of the judge's synthesis frequently identifies tactical errors (e.g., "email HR" vs "use disclosure form")

## Known Issues

- **Model timeouts:** Some models (historically Kimi, now DeepSeek/GLM) occasionally time out. Partial outputs add noise but the council still works with remaining speakers
- **JSON output truncation:** Use `--output file.md` to capture full transcript
- **JSON `decision` field can be noisy:** The structured output sometimes captures mid-synthesis text rather than a clean decision. Read the prose synthesis instead.
- **`--redteam` incompatible with `--format json`:** Red team mode only outputs prose. Use `--output file.md` to capture the transcript. Same applies to `--oxford`, `--socratic`, `--discuss`, `--solo`.

## Output Formats

| Format | Use Case |
|--------|----------|
| `prose` (default) | Human reading, exploratory |
| `json` | Agent workflows, parsing, automation |
| `yaml` | Human-readable structured output |

## See Also

- Repository: https://github.com/terry-li-hm/consilium
- PyPI: https://pypi.org/project/consilium/
- Related skill: `/ask-llms` (simpler parallel queries)
