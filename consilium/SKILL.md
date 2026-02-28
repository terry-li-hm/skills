---
name: consilium
description: Multi-model deliberation — auto-routes by difficulty. Full council (~$0.50), quick parallel (~$0.10), red team (~$0.20), and more.
aliases: [ask-llms, council, ask llms]
github_url: https://github.com/terry-li-hm/consilium
user_invocable: true
cli_version: 0.1.5
cli_verified: 2026-02-28
runtime: rust
---

# LLM Council

5 frontier models deliberate on a question, then Claude Opus 4.6 judges and adds its own perspective. Models see and respond to previous speakers, with a rotating challenger ensuring sustained disagreement. Auto-routes by difficulty — simple questions get quick parallel, complex ones get full council.

> **Rust rewrite (2026-02-28).** consilium is now a Rust binary (4.7MB, ~50ms cold start). Same CLI interface, same modes, same output format. Python version preserved as `consilium-py` fallback. Source: `~/code/consilium/`. GitHub: `terry-li-hm/consilium` (Rust), `terry-li-hm/consilium-py` (Python legacy). Site: [consilium.sh](https://consilium.sh). crates.io: [consilium](https://crates.io/crates/consilium).

## Modes

| Mode | Flag | Cost | Description |
|------|------|------|-------------|
| Auto (default) | *(none)* | varies | Opus classifies difficulty, picks quick or council |
| Quick | `--quick` | ~$0.10 | Parallel queries, no debate/judge |
| Council | `--council` | ~$0.50 | Full multi-round debate + judge |
| Deep | `--deep` | ~$0.90 | Council + auto-decompose + 2 debate rounds. For complex multi-part questions. |

**Modifiers** (combine with council/deep):
| Flag | Cost Delta | Description |
|------|-----------|-------------|
| `--xpol` | ~+$0.15 | Cross-pollination: second parallel pass where each model reads all blind claims and investigates gaps. Extends, not argues. |
| Discuss | `--discuss` | ~$0.30 | Hosted roundtable exploration |
| Socratic | `--socratic` | ~$0.30 | Probing questions to expose assumptions |
| Oxford | `--oxford` | ~$0.40 | Binary for/against with rebuttals + verdict |
| Red Team | `--redteam` | ~$0.20 | Adversarial stress-test of a plan |
| Solo | `--solo` | ~$0.40 | Claude debates itself in multiple roles |

## Routing: Which Mode?

```
Does the question have a single correct answer? (specs, facts, how-to)
  YES → Web search or ask Claude directly. Don't use consilium.
  NO ↓
Is this personal preference / physical / visual? (glasses, photos, food)
  YES → Try it in person. Don't use consilium.
  NO ↓
Do you need multiple perspectives but not debate?
  YES → consilium --quick
  NO ↓
Binary decision with clear for/against?
  YES → consilium --oxford
  NO ↓
Stress-testing a specific plan?
  YES → consilium --redteam
  NO ↓
Exploratory — still forming the question?
  YES → consilium --discuss (or --socratic to probe assumptions)
  NO ↓
Genuine trade-offs requiring deliberation?
  YES → consilium (auto-route, or --council to force full debate)
```

Auto-routing works well for most questions — Opus classifies and picks the right mode. Use explicit flags when you're confident about the format (e.g., `--oxford` for "A vs B" decisions, `--redteam` for plans).

## When to Use

At ~$0.50/run, the cost threshold is negligible. Use whenever:

- **Genuine trade-offs with competing values** — the sweet spot (CV positioning, governance frameworks, architecture decisions)
- **Domain-specific professional decisions** — regulatory, career, strategic
- You need a synthesized recommendation, not raw comparison
- Questions with cognitive, social, or behavioural dimensions (council catches hidden angles Claude underestimates)
- **Stress-testing a plan** — `--redteam` for adversarial, `--socratic` for assumption-probing
- **Code review / security audit** — `--redteam` with actual code pasted into the prompt. Models can't read files, so concatenate source files into the prompt text. ~55K chars (8 modules) works fine. Produces compound attack chains that single-model review misses (SSRF→prompt injection→LLM exfil). ~$1.50 for full codebase review.
- **Iterating on a previous council** — second passes go deeper

## When NOT to Use

- **Single correct answer** — photo crop rules, product specs, naming preferences. Use web search or a single model
- **Personal preference / physical** — glasses frames, food, clothing. Council reasons from theory; go try it in person instead
- **Thinking out loud** — exploratory discussions where you're still forming the question
- **Claude has good context** — if we've been discussing the topic, direct conversation is faster
- **Already converged** — if discussion reached a conclusion, council just validates
- **Speed matters** — takes 60-90s for full council
- **Naming exercises (full council)** — council debates taste in circles. But `--quick` works well: independent samples beat single-model brainstorming, and convergence (4/5 models picking the same name) is a strong signal. Use `--quick` to brainstorm candidates, then registry-check. Full council only if evaluating a shortlist against specific criteria

## Prerequisites

```bash
# Binary is symlinked: ~/.local/bin/consilium → ~/code/consilium/target/release/consilium
# After code changes: cd ~/code/consilium && cargo build --release

# Python fallback still available as consilium-py

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

### Step 0.5: Propose Mode and Confirm

Before running, tell the user which mode you recommend and why (one line), then confirm. If auto-routing is appropriate, say so — don't force an explicit mode when auto would work. Example:

> "This is a binary decision with clear trade-offs — I'd use **--oxford**. Good?"
> "Exploratory question with genuine trade-offs — I'd let it auto-route (likely council). Good?"

Don't run the council until the user confirms or picks a different mode.

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

**Auto-routing is the default** — Opus classifies the question and picks the best mode. Pass an explicit mode flag only when you know what you want (e.g., `--oxford` for a binary decision, `--redteam` to stress-test a plan).

**Always use these flags:**
- `--output ~/notes/Councils/LLM Council - {Topic} - {date}.md` — vault persistence
- `--format json` — **only for council mode** (incompatible with discuss/redteam/solo/socratic/oxford)
- ~~`--named`~~ — **NOT IMPLEMENTED** (skill doc was ahead of CLI). Models show as Speaker 1, 2, etc. Real names appear in council mode output regardless.

**Do NOT use `--quiet` by default.** Run with `run_in_background: true` on the Bash tool so the user can watch live via `consilium --watch` or `--tui` in another tmux tab. Read the `--output` file when the task completes.


**Standard invocation (auto-routes by difficulty):**
```bash
consilium "Should we use microservices or a monolith?" \
 \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Force full council with persona context:**
```bash
consilium "Should I accept the Standard Chartered offer?" \
  --council --format json \
  --persona "$PERSONA" \
  --context "job-offer" \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Red team a plan:**
```bash
consilium "My plan: migrate the monolith to microservices over 6 months..." \
  --redteam \
  --output ~/notes/Councils/LLM\ Council\ -\ {Topic}\ -\ $(date +%Y-%m-%d).md
```

**Common flags:**
```bash
# Context & persona
--persona "context"     # Personal context injected into prompts
--domain banking        # Regulatory context (banking|healthcare|eu|fintech|bio)
--context "hint"        # Context hint for the judge

# Deliberation control
--challenger gemini     # Assign contrarian role (council mode only)
--decompose             # Break complex question into sub-questions first
--rounds 3              # Rounds for --discuss or --socratic (0 = unlimited)
--followup              # Interactive drill-down after judge synthesis (council only)
# Output
--format json           # Machine-parseable output (council mode only)
--share                 # Upload to secret Gist
--quiet                 # Suppress live output
--no-save               # Don't auto-save to ~/.consilium/sessions/
--no-judge              # Skip judge synthesis (for external judge integration)
--no-color              # Disable colored output (auto-disabled in pipes)
--feedback              # Prompt for 1-5 rating after session
--thorough              # Skip consensus early exit + context compression (full deliberation)
```

**Oxford debate (binary decisions):**
```bash
consilium "Should we use microservices?" --oxford
consilium "Hire seniors or train juniors?" --oxford --motion "This house believes..."
```

**Solo council (Claude debates itself in roles):**
```bash
consilium "Pricing strategy" --solo --roles "investor,founder,customer"
consilium --list-roles  # See predefined roles
```

**Domain-specific deliberation (banking, healthcare, etc.):**
```bash
consilium "Should we build an agent for KYC?" \
  --domain banking \
  --challenger gemini \
  --followup \
  --output counsel.md
```

Available domains: `banking`, `healthcare`, `eu`, `fintech`, `bio`

### Flag Compatibility

| Flag | council | quick | discuss | socratic | oxford | redteam | solo |
|------|---------|-------|---------|----------|--------|---------|------|
| `--format json` | yes | yes | **no** | **no** | **no** | **no** | **no** |
| `--challenger` | yes | **no** | **no** | **no** | **no** | **no** | **no** |
| `--followup` | yes | **no** | **no** | **no** | **no** | **no** | **no** |
| `--rounds` | no | no | yes | yes | no | no | no |
| `--motion` | no | no | no | no | yes | no | no |
| `--roles` | no | no | no | no | no | no | yes |
| `--decompose` | yes | no | no | no | no | no | no |
| `--xpol` | yes | no | no | no | no | no | no |

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
consilium --sessions              # List recent 20 sessions
consilium --stats                 # Cost breakdown by mode, 7-day summary
consilium --watch                 # Live tail from another tmux tab (rich formatted)
consilium --tui                   # TUI with phase/cost/time tracking
consilium --view                  # View latest session in pager
consilium --view "career"         # View session matching term (filename or content)
consilium --search "career"       # Search all session content
consilium --list-roles            # Show predefined roles for --solo
consilium --doctor               # Check API keys and connectivity
```

## Prompting Tips

**For draft reviews** (LinkedIn comments, emails, messages, posts):

Always include the source material in the prompt — models can't judge tone, positioning, or reception risk without seeing what the draft responds to. Structure the prompt as:
1. The original post/email/thread being responded to (full text or key excerpts)
2. The drafted response
3. Context about the author's relationship to the recipient and goals
4. Specific review criteria (tone, positioning risk, information leaks, reception)

Mode selection by stakes:
- `--quick` (~$0.10): Internal messages, Slack replies, low-visibility comments
- `--redteam` (~$0.20): Plans or proposals being stress-tested
- `--council --domain <X>` (~$0.50): **Public comments, LinkedIn posts, anything that builds or risks reputation.** Reputation-building content is not a tone check — it needs full deliberation on positioning, strategic value, and network effects. Include `--persona` with career context and goals.

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

**For philosophical/contemplative questions:**

Council excels at finding structural cracks in propositional claims — but blind to teachings that are *instructions* rather than *arguments*. "Look for the self" is a direction to look, not a truth claim. When evaluating non-propositional frameworks (meditation, therapy, coaching), add:
- "Distinguish claims (testable assertions) from pointers (instructions for seeing)"
- "Rate practical utility separately from philosophical coherence"
- `--decompose` works well here — breaks apart the sub-questions that a philosophical system bundles together

Without this framing, council will evaluate a ladder as a floor.

**For domain-specific questions (banking, healthcare, etc.):**

Use `--domain` flag to auto-inject regulatory context:
```bash
consilium "question" --domain banking   # HKMA/MAS/FCA, MRM requirements
consilium "question" --domain healthcare # HIPAA constraints
consilium "question" --domain eu        # GDPR/AI Act considerations
```

This surfaces compliance concerns early rather than as afterthoughts.

## Model Tendencies

| Model | Tendency | Useful For |
|-------|----------|------------|
| **GPT-5.2** | Practical, implementation-focused | Actionable steps |
| **Gemini 3.1 Pro** | Technical depth, systems thinking | Architecture |
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

## Cost & ROI

- ~$0.60 for full discuss mode. Worth it when genuinely novel insights emerge (bouncer pattern, compliance flag). Diminishing returns on second pass of same topic.
- **2 novel insights per council = good; 0 = should have used `--quick`.**
- **Tone/networking review = good ROI.** Substack comment review caught "unguided AI" phrasing that could read as "consultant advocates shipping AI without governance" in banking context — reputational risk invisible to the drafter. When your name is public + reader could be a future client, $0.50 is cheap insurance.
- **Framing bias:** 6/6 unanimity in quick mode is a red flag — means the prompt is one-sided, not that the answer is obvious. Always include "Option: fix the existing thing" for deprecation/migration decisions. No council will challenge the frame you give them — the user has to. See [[Frontier Council Lessons]].

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

- **Colored output** (v0.1.3+): Semantic colors for phase banners, model headers, notices, stats. Auto-disabled in pipes (`IsTerminal`). Use `--no-color` to force plain. Colors match `--watch` styling.
- **Context compression** (v0.1.4+): Multi-round debates compress prior rounds via Llama 3.3 70B. Judge always gets full transcripts. Use `--thorough` to disable compression + consensus early exit for maximum deliberation depth.
- **Challenger dissent protection** (v0.1.5+): If the challenger is actively dissenting, consensus early exit is blocked — prevents suppressing the most important minority view.
- **Binary can go stale after code changes.** Source at `~/code/consilium`. After edits: `cd ~/code/consilium && cargo build --release`. Binary is symlinked from `~/.local/bin/consilium`.
- **Model timeouts:** Some models (historically Kimi, now DeepSeek/GLM) occasionally time out. Partial outputs add noise but the council still works with remaining speakers.
- **JSON output truncation:** Use `--output file.md` to capture full transcript.
- **JSON `decision` field can be noisy:** The structured output sometimes captures mid-synthesis text rather than a clean decision. Read the prose synthesis instead.
- **`--format json` only works with council and quick modes.** All other modes (discuss, redteam, solo, socratic, oxford) output prose only. Use `--output file.md` to capture. See flag compatibility table above.
- **`--challenger` and `--followup` are council-only.** The CLI will error if combined with other modes.

## Output Formats

| Format | Use Case |
|--------|----------|
| `prose` (default) | Human reading, exploratory |
| `json` | Agent workflows, parsing, automation |
| `yaml` | Human-readable structured output |

## See Also

- Repository (Rust): https://github.com/terry-li-hm/consilium
- Repository (Python legacy): https://github.com/terry-li-hm/consilium-py
- PyPI (Python): https://pypi.org/project/consilium/
- Related skill: `/ask-llms` (simpler parallel queries)
