---
name: frontier-council
description: 4 frontier models deliberate, then Claude judges. For high-stakes decisions needing diverse AI perspectives.
github_url: https://github.com/terry-li-hm/frontier-council
github_hash: 196ec8c
user_invocable: true
---

# LLM Council

4 frontier models deliberate on a question, then Claude Opus 4.5 judges and adds its own perspective. Unlike `/ask-llms` which shows parallel responses, this creates an actual debate where models see and respond to previous speakers, with a rotating challenger ensuring sustained disagreement.

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
frontier-council "question" --practical             # Actionable rules only, no philosophy
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

**Council (deliberators):**

| Model | Tendency | Useful For |
|-------|----------|------------|
| **GPT-5.2** | Practical, implementation-focused | Actionable steps |
| **Gemini 3 Pro** | Technical depth, systems thinking | Architecture |
| **Grok 4** | Contrarian, challenges consensus | Stress-testing ideas |
| **Kimi K2.5** | Detail-oriented, edge cases | Completeness check |

**Judge (Claude Opus 4.5):** Balanced, thorough, safety-conscious. Synthesizes deliberation and adds independent perspective via "Judge's Own Take" section.

**If you want more disagreement:** The rotating challenger ensures someone is always pushing back. For extra tension, use `--challenger grok` to start with Grok (naturally contrarian + explicit challenger prompt = maximum pushback).

**If council is too cautious:** Add constraint "Assume this is a startup, not an enterprise" or "Speed matters more than perfection."

## Challenger Strategy

**Default challenger: GPT** (rotates each round)

Reasoning:
- Grok is naturally contrarian — it pushes back regardless of the `--challenger` flag
- GPT as default challenger = practical skepticism + explicit contrarian framing
- This gives you **two sources of pushback**: prompted-GPT + natural-Grok
- Challenger rotates: GPT R1 → Gemini R2 → Grok R3 → Kimi R4 → GPT R5...

**When to override:**
- `--challenger gemini` — For architecture questions where Gemini's systems thinking + contrarian = interesting angles
- `--challenger grok` — If you want Grok to be *even more* contrarian (rare)
- `--challenger kimi` — For edge-case-focused pushback

## Lessons from Usage

**Tension is where the value is.** Consensus is boring — dissent forces sharper thinking. When Grok pushed back on "over-engineering" while others defended compliance depth, that tension produced the best insight (stage-appropriate compliance). If council reaches quick agreement, probe harder.

**Models default to enterprise-grade.** Without constraints, the council models suggest infrastructure for problems that don't exist yet. Always add constraints upfront: "this is a POC", "single-user system", "speed > perfection", "manual processes acceptable".

**Domain expertise emerges when prompted.** Banking-specific concerns (Records & Evidence Layer, eDiscovery, escalation burden) only surfaced because "banking clients" was in the question. Use `--domain` flag or state regulatory context explicitly.

**Vocabulary translation matters.** "Audit trail" lands better than "episodic memory" with compliance stakeholders. Council caught this — useful reminder to code-switch terminology for audience.

**Synthesis > individual responses.** Individual answers overlap. Judge pulling out consensus vs dissent is where value concentrates. The debate format earns its cost in the synthesis.

### Lessons from Technical Optimization (Feb 2026)

**Include real metrics, not just descriptions.** Council gave theoretical advice ("kill the reranker") that backfired in practice. If we'd included actual latency breakdown (`rewrite=2s, retrieve=2s, rerank=1s, select=3s`), they could have identified the real bottleneck.

**State deployment constraints explicitly.** Council assumed we could "move reranker local" — but we're on serverless (Railway/Vercel). Add constraints like:
- "API-only, no local inference"
- "Serverless deployment"
- "Can't self-host models"

**Ask for testable hypotheses, not just recommendations.** Instead of "kill the reranker", ask council to frame as: "IF you disable X, THEN expect Y. Test by Z." This makes advice actionable and falsifiable.

**Separate quick wins from rearchitecture.** Council mixed "reduce candidates" (5 min fix) with "index-time expansion" (days of work). Ask them to categorize by effort/impact.

**Test > theorize.** Some council recommendations were wrong when tested. For optimization questions, run quick benchmarks yourself rather than debating theory. Council is better for **directional** guidance than specific parameter tuning.

### Lessons from Judge Over-Aggregation (Feb 2026)

**The judge's diagnosis is sharper than its prescription.** In a CV review, the judge correctly identified "minimum effective change is the goal" — then recommended 6 changes. The deliberation generates momentum: 4 models produce detailed suggestions, and even the synthesiser aggregates instead of filtering.

**Fix applied:** Judge prompt now enforces "Prescription Discipline" — max 3 "Do Now" items, must argue against each before including it, and must explicitly list what it's dropping. The gravitational pull of the council is "add more"; the judge's pull must be "do less."

**Pattern for callers:** When presenting council results, treat the judge's *framing* as more reliable than its *action list*. If the framing says "this is mostly fine, small adjustments needed" but the action list has 6 items, trust the framing.

### Lessons from Operational Questions (Feb 2026)

**Models spiral into philosophy on operational questions.** When asked "when should I read vs extract?", the council spent rounds debating cognitive science and "psychological ownership" instead of producing concrete triggers. The judge flagged it: "spent too much energy debating 'do you need the vibe?'"

**Fix applied:** Added `--practical` flag that injects "focus on actionable triggers and concrete rules, avoid philosophy/theory" into all prompts (blind, first-speaker, subsequent, judge). Also added baseline "Prioritize PRACTICAL, ACTIONABLE advice" to blind and first-speaker prompts (previously only in subsequent-speaker prompt, so the spiral started in round 1).

**JSON extraction was fundamentally broken.** The old `extract_structured_summary()` used naive string matching (`'recommend' in line_lower`) on the judge's prose — producing garbled action_items and truncated reasoning. Replaced with a Haiku second-pass that extracts structured JSON from the prose. New fields: `do_now`, `consider_later`, `skip` (matching the judge's triage structure). Falls back to old method if the API call fails. Cost: ~$0.005/extraction.

**Rule of thumb:** Use `--practical` for operational/workflow questions. Skip it for strategic decisions where the philosophical dimensions are actually useful.

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
