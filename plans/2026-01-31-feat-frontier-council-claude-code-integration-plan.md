---
title: "feat: Frontier Council Claude Code Integration"
type: feat
date: 2026-01-31
deepened: 2026-01-31
research_agents: 9
---

# feat: Frontier Council Claude Code Integration

## Enhancement Summary

**Deepened on:** 2026-01-31
**Research agents used:** 9 (async-python, yaml-schemas, cli-tiers, kieran-python-reviewer, architecture-strategist, code-simplicity-reviewer, performance-oracle, obsidian-patterns, agent-native-architecture)

### Key Finding: Radical Simplification Required

The research agents produced a **strong consensus**: the original 5-phase plan is over-engineered.

> "The plan has 5 phases for a tool that works. That's a smell. Prior research said 'don't framework it' — that's the answer."
> — Code Simplicity Reviewer

**Revised scope:** 2 features, ~50 lines of code, 1-2 sessions total.

### Critical Architecture Decision

**Keep vault operations in the skill, not the CLI.**

The architecture review identified that `--vault` and `--inject-context` flags would tightly couple the CLI to Terry's vault structure, violating portability. The CLI should remain a generic, PyPI-distributable tool.

**New boundary:**
- **CLI** = computation engine (deliberation, synthesis, structured output)
- **Skill** = orchestration (context gathering, vault integration, post-actions)

---

## Overview

Make `frontier-council` more Claude Code friendly by adding structured output format. Keep vault integration and post-decision hooks in the skill layer.

## Problem Statement

Currently `frontier-council` outputs prose that Claude Code can't act on. After a council deliberation:
- No structured way to extract the decision/recommendation
- No bridge from "council decided X" to "now do X"

The tool works well standalone but doesn't integrate into Claude Code workflows.

## Prior Research

**Archived plan:** `/Users/terry/skills/.archive/plans/feat-llm-council-improvements.md` (2026-01-20)

Key findings:
- Parallelize blind phase: 50-100s → 15-25s (**defer** — optimization before validation)
- Simplicity reviewer: "The current tool is already good. Don't framework it."

**Already implemented:**
- `--context` flag for judge hint
- `--persona` flag for user context (USE THIS for context injection)
- Auto-save to `~/.frontier-council/sessions/`
- `--output` for explicit save
- `--sessions` to list recent

---

## Proposed Solution (Simplified)

### Feature 1: Structured Output Mode (`--format`)

**Research insight:** Use `--format` flag instead of `--actionable`. JSON over YAML for easier agent parsing.

```bash
frontier-council "question" --format json   # Machine-parseable
frontier-council "question" --format yaml   # Structured but readable
frontier-council "question"                 # Default: prose (unchanged)
```

**Output schema (JSON):**
```json
{
  "schema_version": "1.0",
  "question": "Should we use microservices or monolith?",
  "decision": "Use monolith architecture for initial MVP",
  "confidence": "high",
  "reasoning_summary": "Council agreed that...",
  "dissents": [
    {"model": "Grok", "concern": "scaling concerns at 10K users"}
  ],
  "action_items": [
    {"action": "Create database schema plan", "priority": "high"},
    {"action": "Set up Rails with Hotwire", "priority": "medium"}
  ],
  "meta": {
    "timestamp": "2026-01-31T14:30:00Z",
    "models_used": ["claude-opus-4.5", "gpt-5.2", "gemini-3-pro", "grok-4", "kimi-k2.5"],
    "rounds": 2,
    "duration_seconds": 67,
    "estimated_cost_usd": 0.85
  }
}
```

**Implementation:**
1. Add `--format` flag with choices: `json`, `yaml`, `prose` (default)
2. Add final judge call for structured summary when format != prose
3. Append structured block to output
4. Include schema version for forward compatibility

**Why JSON over YAML:**
- Natively parseable without extra dependencies
- No YAML multi-line string gotchas
- Easier for agents to extract fields

### Feature 2: Skill Enhancement (Vault + Hooks)

**Research insight:** Keep vault operations in the skill layer, not the CLI.

The skill (`/llm-council`) will:
1. Compose context via existing `--persona` flag (no new CLI flag needed)
2. Parse `--format json` output
3. Offer post-decision actions
4. Save to vault when warranted

**Skill workflow:**
```
1. Gather context (read vault files, compose into --persona)
2. Call: frontier-council "$question" --format json --persona "$context"
3. Parse JSON output
4. Present decision with critique
5. Offer follow-up actions via AskUserQuestion:
   - Create tasks from action_items
   - Save to vault as decision record
   - Draft follow-up messages
   - Just note the advice
6. Execute selected actions
```

**Vault save format (when user selects "Save to vault"):**
```markdown
---
date: 2026-01-31
type: decision
question: "Should we use microservices or monolith?"
status: pending
decision: "Use monolith for MVP"
confidence: high
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

**Related:** [[Active Pipeline]] | [[Architecture Decisions]]

# Architecture Decision: Monolith for MVP

## Question
Should we use microservices or monolith for the MVP?

## Decision
Use monolith for MVP.

## Reasoning
[Council synthesis]

## Dissents
- **Grok:** scaling concerns at 10K users

## Action Items
- [ ] Create database schema plan
- [ ] Set up Rails with Hotwire

---
*Council convened: 2026-01-31 | 5 models | 2 rounds | ~$0.85*
```

**Folder:** `~/notes/Decisions/` (flat structure)
**Filename:** `LLM Council - {Topic} - {YYYY-MM-DD}.md`

---

## What We're NOT Doing (Deferred)

Based on research consensus, these features are **deferred until proven needed:**

| Feature | Original Plan | Why Deferred |
|---------|---------------|--------------|
| `--vault` flag | Phase 3 | Couples CLI to Terry's vault; keep in skill |
| `--inject-context` | Phase 4 | Use existing `--persona` instead |
| `--quick/--deep` tiers | Phase 2 | Explicit flags are clearer; presets hide what's happening |
| Async blind phase | Phase 0 | Optimization before validation; current latency is acceptable |
| Context manifests | — | Over-engineering; copy/paste works |

**Principle:** Use the tool for a month with just `--format json`. Then decide what's actually missing.

---

## Implementation Plan (Simplified)

### Phase 1: Structured Output (`--format`)

**Effort:** 1-2 sessions

1. Add `--format` flag to `cli.py`:
```python
parser.add_argument('--format', '-f',
    choices=['json', 'yaml', 'prose'],
    default='prose',
    help='Output format (default: prose)')
```

2. Add structured summary extraction in `council.py`:
```python
if args.format != 'prose':
    summary = extract_structured_summary(judge_response, question, meta)
    if args.format == 'json':
        output_parts.append(json.dumps(summary, indent=2))
    else:
        output_parts.append(yaml.dump(summary))
```

3. Schema:
```python
from pydantic import BaseModel
from typing import Literal

class ActionItem(BaseModel):
    action: str
    priority: Literal["high", "medium", "low"] = "medium"

class Dissent(BaseModel):
    model: str
    concern: str

class CouncilOutput(BaseModel):
    schema_version: str = "1.0"
    question: str
    decision: str
    confidence: Literal["low", "medium", "high"]
    reasoning_summary: str
    dissents: list[Dissent]
    action_items: list[ActionItem]
    meta: dict
```

**Files:** `frontier_council/cli.py`, `frontier_council/council.py`
**OpenCode candidate:** Yes (well-specified schema + extraction)

### Phase 2: Skill Update

**Effort:** 1 session

1. Update `/Users/terry/skills/frontier-council/SKILL.md`
2. Add workflow for:
   - Context composition via `--persona`
   - JSON output parsing
   - Post-decision action menu
   - Vault save logic

**Files:** `/Users/terry/skills/frontier-council/SKILL.md`
**Keep in Claude Code:** All (skill logic, UX decisions)

---

## Research Insights

### Async Python Patterns (for future Phase 0)

If async optimization is needed later:

```python
import asyncio
import httpx

async def fetch_all_models(
    client: httpx.AsyncClient,
    models: list[str],
    prompt: str,
    max_concurrent: int = 5
) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(model: str) -> dict:
        async with semaphore:
            try:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                    timeout=60.0
                )
                return {"model": model, "success": True, "data": response.json()}
            except Exception as e:
                return {"model": model, "success": False, "error": str(e)}

    return await asyncio.gather(*[fetch_one(m) for m in models])
```

**Key patterns:**
- Semaphore for rate limiting (max 5 concurrent)
- `return_exceptions=True` or wrapper function for error isolation
- Single `httpx.AsyncClient` with connection pooling
- Stagger initial requests by 150ms to avoid thundering herd

**Realistic performance:** 20-35s typical (not 15-25s), 40s worst case.

### CLI Tier Patterns (for future reference)

If tiers are needed:
```python
from dataclasses import dataclass
from enum import Enum

class Tier(Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

@dataclass(frozen=True)
class TierConfig:
    models: int
    rounds: int
    blind_phase: bool

TIER_CONFIGS = {
    Tier.QUICK: TierConfig(models=3, rounds=1, blind_phase=False),
    Tier.STANDARD: TierConfig(models=5, rounds=2, blind_phase=True),
    Tier.DEEP: TierConfig(models=5, rounds=3, blind_phase=True),
}

# Mutually exclusive flags
tier_group = parser.add_mutually_exclusive_group()
tier_group.add_argument('--quick', dest='tier', action='store_const', const=Tier.QUICK)
tier_group.add_argument('--deep', dest='tier', action='store_const', const=Tier.DEEP)
parser.set_defaults(tier=Tier.STANDARD)
```

### Obsidian Frontmatter Schema

For vault saves:
```yaml
---
date: 2026-01-31
type: decision
question: "..."
status: pending | resolved | superseded
decision: "..."
confidence: low | medium | high
participants: [list of models]
context_link: "[[Related Note]]"
tags: [decision, llm-council]
aliases: []
---
```

### Agent-Native Principles Applied

1. **Rich outputs:** JSON includes meta (cost, duration, models) for agent decisions
2. **Files as interface:** Vault saves create audit trail both agent and human can read
3. **Composable primitives:** CLI does computation; skill orchestrates workflow
4. **Approval pattern:** Post-decision hooks ask before sending/saving

---

## Acceptance Criteria

### Functional
- [ ] `--format json` produces valid JSON with schema
- [ ] `--format yaml` produces valid YAML
- [ ] Default (prose) behavior unchanged
- [ ] Skill parses JSON and offers follow-up actions
- [ ] Skill saves to `~/notes/Decisions/` with proper frontmatter

### Non-Functional
- [ ] JSON output validates against Pydantic schema
- [ ] Backwards compatible (no existing flags changed)
- [ ] Skill handles parse failures gracefully

### Quality
- [ ] Tests for JSON/YAML output
- [ ] SKILL.md fully documents new workflow

---

## OpenCode Delegation Summary

| Component | OpenCode? | Reason |
|-----------|-----------|--------|
| `--format` flag + schema | ✅ Yes | Well-specified, clear schema |
| JSON extraction from judge | ✅ Yes | Prompt + parsing logic |
| Skill workflow | ❌ No | Claude Code tools, UX decisions |
| Vault save formatting | ❌ No | Obsidian conventions, wikilinks |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| JSON parse rate | >95% valid output |
| Time to action | <30s from council output to task creation |
| Adoption | Used for important decisions |

---

## Risk Analysis (from research)

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| LLM doesn't follow JSON schema | Medium | Retry with explicit schema in prompt; fallback to prose |
| Over-engineering after "simple" phase | High | Stop after Phase 2; use for 1 month before adding features |
| Skill complexity creep | Medium | Keep skill under 150 lines |

---

## References

### Internal
- Archived plan: `/Users/terry/skills/.archive/plans/feat-llm-council-improvements.md`
- Current skill: `/Users/terry/skills/frontier-council/SKILL.md`
- Repo: https://github.com/terry-li-hm/frontier-council (c25ffcc)

### External
- OpenRouter docs: https://openrouter.ai/docs
- Pydantic: https://docs.pydantic.dev/
- HTTPX async: https://www.python-httpx.org/async/
- Obsidian properties: https://help.obsidian.md/properties

### Research Sources
- Async patterns: httpx docs, SuperFastPython asyncio guides
- CLI patterns: argparse docs, Typer, Click
- Agent-native architecture: compound-engineering skill
