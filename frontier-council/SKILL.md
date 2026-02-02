---
name: frontier-council
description: Frontier Council with 5 frontier models (Opus 4.5, GPT-5.2, Gemini 3 Pro, Grok 4, Kimi K2.5). Models deliberate on a question, each seeing previous responses, then a judge synthesizes consensus. Use for important decisions needing diverse AI perspectives.
github_url: https://github.com/terry-li-hm/frontier-council
github_hash: 89696b9
---

# LLM Council

5 frontier models deliberate on a question. Unlike `/ask-llms` which shows parallel responses, this creates an actual debate where models see and respond to previous speakers, followed by a judge synthesizing the consensus.

## When to Use

- Important decisions that benefit from diverse perspectives
- You want models to actually debate, not just answer in parallel
- You need a synthesized recommendation, not raw comparison
- Exploring trade-offs where different viewpoints matter

## When NOT to Use

- **Thinking out loud** — exploratory discussions where you're still forming the question
- **Claude has good context** — if we've been discussing the topic, direct conversation is faster
- **Personal preference** — council excels at objective trade-offs, not "what would I enjoy"
- **Already converged** — if discussion reached a conclusion, council just validates
- **Speed matters** — takes 60-90s and costs several dollars

## Prerequisites

```bash
# Install (one-time)
uv tool install frontier-council

# Or install from local dev:
cd ~/code/frontier-council && pip install -e .

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
PIPELINE=$(cat "/Users/terry/notes/Active Pipeline.md" | head -50)

# Compose persona
PERSONA="Background: Terry is AGM & Head of Data Science at CITIC, being counselled out.
Current pipeline: $PIPELINE"
```

For other decisions, use simpler context or skip this step.

### Step 3: Run the Council

**Basic usage:**
```bash
frontier-council "Should we use microservices or a monolith?"
```

**With structured output (recommended for agent workflows):**
```bash
frontier-council "Should I accept the Standard Chartered offer?" \
  --format json \
  --persona "$PERSONA" \
  --context "job-offer"
```

**Common options:**
```bash
frontier-council "question" --format json           # Machine-parseable output
frontier-council "question" --format yaml           # Structured but readable
frontier-council "question" --social                # Interview/networking questions
frontier-council "question" --persona "context"     # Add personal context
frontier-council "question" --rounds 3              # More deliberation
frontier-council "question" --output file.md        # Save transcript
frontier-council "question" --share                 # Upload to secret Gist
frontier-council "question" --domain banking        # Inject regulatory context
frontier-council "question" --challenger gemini     # Assign contrarian role
frontier-council "question" --followup              # Interactive drill-down after synthesis
```

**Domain-specific deliberation (banking, healthcare, etc.):**
```bash
frontier-council "Should we build an agent for KYC?" \
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
    "estimated_cost_usd": 0.85
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
2. **Save to vault** — Create decision record in `~/notes/Decisions/`
3. **Draft messages** — Draft follow-up messages based on action_items
4. **Just note it** — No further action needed

### Step 6: Execute Selected Action

**If "Create tasks":**
Use TaskCreate for each action_item with appropriate priority.

**If "Save to vault":**
Create note at `~/notes/Decisions/LLM Council - {Topic} - {YYYY-MM-DD}.md`:

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
  - llm-council
---

**Related:** [[Active Pipeline]] | [[Job Hunting]]

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
frontier-council "question" --domain banking   # HKMA/MAS/FCA, MRM requirements
frontier-council "question" --domain healthcare # HIPAA constraints
frontier-council "question" --domain eu        # GDPR/AI Act considerations
```

This surfaces compliance concerns early rather than as afterthoughts.

## Model Tendencies

Each model has predictable biases. Use this to interpret results:

| Model | Tendency | Useful For |
|-------|----------|------------|
| **Claude Opus** | Balanced, thorough, safety-conscious | Synthesis, nuance |
| **GPT-5.2** | Practical, implementation-focused | Actionable steps |
| **Gemini 3 Pro** | Technical depth, systems thinking | Architecture |
| **Grok 4** | Contrarian, challenges consensus | Stress-testing ideas |
| **Kimi K2.5** | Detail-oriented, edge cases | Completeness check |

**If you want more disagreement:** Explicitly ask "Have one model argue the contrarian position" or "Challenge the consensus view."

**If council is too cautious:** Add constraint "Assume this is a startup, not an enterprise" or "Speed matters more than perfection."

## Challenger Strategy

**Default challenger: Claude** (not Grok)

Reasoning:
- Grok is naturally contrarian — it will push back regardless of the `--challenger` flag
- Claude is normally agreeable but has deep domain knowledge
- Assigning Claude as challenger = Claude's depth + explicit contrarian framing
- This gives you **two sources of pushback**: prompted-Claude + natural-Grok

**When to override:**
- `--challenger gemini` — For architecture questions where Gemini's systems thinking + contrarian = interesting angles
- `--challenger gpt` — For implementation questions where practical skepticism helps
- `--challenger grok` — If you want Grok to be *even more* contrarian (rare)

**Anti-pattern:** Don't double up on Grok (e.g., adding second Grok instance as challenger). Same model = similar reasoning patterns, more cost without more diversity.

## Lessons from Usage

**Tension is where the value is.** Consensus is boring — dissent forces sharper thinking. When Grok pushed back on "over-engineering" while others defended compliance depth, that tension produced the best insight (stage-appropriate compliance). If council reaches quick agreement, probe harder.

**Models default to enterprise-grade.** Without constraints, 4/5 models suggest infrastructure for problems that don't exist yet. Always add constraints upfront: "this is a POC", "single-user system", "speed > perfection", "manual processes acceptable".

**Domain expertise emerges when prompted.** Banking-specific concerns (Records & Evidence Layer, eDiscovery, escalation burden) only surfaced because "banking clients" was in the question. Use `--domain` flag or state regulatory context explicitly.

**Vocabulary translation matters.** "Audit trail" lands better than "episodic memory" with compliance stakeholders. Council caught this — useful reminder to code-switch terminology for audience.

**Synthesis > individual responses.** Individual answers overlap. Judge pulling out consensus vs dissent is where value concentrates. The debate format earns its cost in the synthesis.

## Known Issues

**JSON output truncation:** For long deliberations, the JSON block may get cut off. Always use `--output file.md` to capture the full transcript:

```bash
frontier-council "complex question" --format json --output /tmp/council.md
```

Then parse the JSON from the saved file.

**Follow-up friction:** ~~After council concludes, there's no built-in way to drill into specific points.~~ **Fixed:** Use `--followup` flag for interactive drill-down after judge synthesis.

## Output Formats

| Format | Use Case |
|--------|----------|
| `prose` (default) | Human reading, exploratory |
| `json` | Agent workflows, parsing, automation |
| `yaml` | Human-readable structured output |

## See Also

- Repository: https://github.com/terry-li-hm/frontier-council
- PyPI: https://pypi.org/project/frontier-council/
- Plan: `/Users/terry/skills/plans/2026-01-31-feat-frontier-council-claude-code-integration-plan.md`
