# feat: True Council Deliberation

Transform the LLM Council from a sequential "panel" into genuine multi-model deliberation with back-and-forth debate.

## Enhancement Summary

**Deepened on:** 2026-01-20
**Research agents used:** simplicity-reviewer, architecture-strategist, performance-oracle, agent-native-architecture, academic-patterns, python-regex

### Key Improvements from Research
1. **Simplified to 2 phases** - Removed @mention parsing (YAGNI)
2. **Academic grounding** - ReConcile paper patterns for sycophancy mitigation
3. **Performance optimized** - Early exit saves 40-60s on consensus

### Research Insights Applied
- Anti-sycophancy prompts from ReConcile (ACL 2024)
- Explicit AGREE/DISAGREE requirement prevents passive agreement
- 4/5 threshold for consensus is optimal (allows one dissenter)

---

## Overview

Current state: 5 frontier models speak in fixed order (Claude -> GPT -> Gemini -> Grok -> Kimi), each seeing prior responses, with a single judge synthesis. This is a panel, not a council.

Target state: Models actively engage with each other's points and detect consensus for early exit.

## Problem Statement

The current implementation has two fundamental gaps:

1. **No real engagement** - Models can ignore each other; prompts say "respond to points" but don't enforce it
2. **No convergence detection** - Runs exactly N rounds regardless of whether consensus is reached

## Proposed Solution

### Phase 1: Engagement Prompts (Low Risk, High Impact)

Update system prompts to require explicit engagement:

```python
# council.py - new council_system prompt
council_system = """You are {name}, participating in Round {round_num} of a council deliberation.

REQUIREMENTS for your response:
1. Reference at least ONE previous speaker by name (e.g., "I agree with Claude that..." or "GPT's point about X overlooks...")
2. State explicitly: AGREE, DISAGREE, or BUILD ON their specific point
3. Add ONE new consideration not yet raised

If you fully agree with emerging consensus, say: "CONSENSUS: [the agreed position]"

Previous speakers this round: {previous_speakers}

Be direct. Challenge weak arguments. Don't be sycophantic."""

# First speaker gets different prompt (no one to reference yet)
first_speaker_system = """You are {name}, speaking first in Round {round_num} of a council deliberation.

As the first speaker, stake a clear position on the question. Be specific and substantive so others can engage with your points.

End with 2-3 key claims that others should respond to."""
```

**Files to modify:**
- `council.py:97-105` - Replace `council_system` with round-aware version

### Phase 2: Convergence Detection (Medium Risk)

Add early exit when consensus is detected:

```python
# council.py - new function after line 69
def detect_consensus(conversation: list[tuple[str, str]], council_size: int) -> tuple[bool, str]:
    """Detect if council has converged. Returns (converged, reason)."""
    if len(conversation) < council_size:
        return False, "insufficient responses"

    recent = [text for _, text in conversation[-council_size:]]

    # Check for explicit CONSENSUS signals
    consensus_count = sum(1 for text in recent if "CONSENSUS:" in text.upper())
    if consensus_count >= council_size - 1:  # 4 of 5
        return True, "explicit consensus signals"

    # Check for agreement language
    agreement_phrases = ["i agree with", "building on", "i concur", "we all seem to agree"]
    agreement_count = sum(
        1 for text in recent
        if any(phrase in text.lower() for phrase in agreement_phrases)
    )
    if agreement_count >= council_size - 1:
        return True, "agreement language detected"

    return False, "no consensus"
```

**Integration in deliberation loop:**

```python
# After each round (after line 127)
if round_num >= 1:  # Check after first full round
    converged, reason = detect_consensus(conversation, len(council_config))
    if converged:
        if verbose:
            print(f"\n>>> CONSENSUS DETECTED ({reason}) - proceeding to judge\n")
        break
```

**Files to modify:**
- `council.py:70` (new) - Add `detect_consensus()` function
- `council.py:127` (after) - Add convergence check in loop

### Phase 3: CLI Updates

```python
# council.py - change default rounds to 2
parser.add_argument(
    "--rounds",
    type=int,
    default=2,  # Changed from 1
    help="Number of deliberation rounds (default: 2)",
)
```

**Files to modify:**
- `council.py:191` - Change default rounds from 1 to 2
- `SKILL.md` - Update documentation with new default

## Technical Considerations

### Architecture
- Keep the simple httpx approach - no frameworks needed
- Add ~25 lines for new features (prompts + consensus detection)
- Maintain backwards compatibility (existing CLI usage still works)

### Performance
- Early exit on consensus saves 40-60s and tokens
- Default 2 rounds: ~120s typical
- With early exit: can complete in ~60s if consensus reached

### Error Handling
- If a model fails, skip it and continue
- Require minimum 3 healthy models to proceed
- Note missing perspectives in output

## Acceptance Criteria

### Functional Requirements
- [ ] System prompts require explicit engagement with previous speakers
- [ ] First speaker gets different prompt (no prior speakers to reference)
- [ ] Convergence detection triggers early exit when 4/5 agree
- [ ] Default rounds changed from 1 to 2

### Quality Gates
- [ ] Manual test: Run council on 3 different questions
- [ ] Verify models actually reference each other by name
- [ ] Verify early exit triggers when consensus reached

## Implementation Order

1. **Phase 1: Engagement Prompts**
   - Update `council_system` prompt with AGREE/DISAGREE requirement
   - Add first speaker prompt variant
   - Test with single question

2. **Phase 2: Convergence Detection**
   - Add `detect_consensus()` function
   - Integrate into deliberation loop
   - Test early exit behavior

3. **Phase 3: CLI & Docs**
   - Change default rounds to 2
   - Update SKILL.md

## Files Summary

| File | Changes |
|------|---------|
| `council.py` | Add ~25 lines: updated prompts, detect_consensus function |
| `SKILL.md` | Update docs: new default rounds, how convergence works |

## Edge Cases

| Case | Handling |
|------|----------|
| Immediate consensus (Round 1) | Exit early, proceed to judge |
| No consensus after all rounds | Judge synthesizes with "no consensus reached" note |
| Model fails | Skip, continue with remaining, note in output |
| All agree but one | 4/5 threshold still triggers consensus |

## References

- Current implementation: `/Users/terry/skills/llm-council/council.py`
- ReConcile paper (ACL 2024): Confidence-weighted voting, sycophancy mitigation via explicit disagreement prompts
- CONSENSAGENT: Conversation-level consensus detection triggers
- AutoGen SelectorGroupChat: Dynamic speaker selection patterns (not needed for this simpler implementation)
