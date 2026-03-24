---
name: translation
description: Turn a design into a self-contained implementation plan with TDD steps, exact paths, and complete code. Use after /transcription or when the shape is already clear.
user_invocable: true
context: fork
---

# /translation — Implementation Plan

Turn a validated design into a plan that an executing agent (or future you) can follow with zero additional context. The plan is the complete instruction set.

## When to Use

- After `/transcription` when the design is approved
- When requirements are already clear and no design exploration is needed
- When the user says "plan this", "how do we build this", "break this down"
- **Not needed for:** single-file changes, obvious bug fixes, config tweaks

## Inputs

Accept any of:
- A requirements doc path (from `/transcription`)
- A verbal feature description
- A GitHub issue or bug report

If a requirements doc exists in `~/docs/brainstorms/` matching the topic, read it and use it as the origin. Reference it with `origin:` in frontmatter. Don't re-ask questions the transcription already answered.

If inputs are too vague to plan, say so. Either ask targeted questions (one at a time) or suggest `/transcription` first.

## Context Scan

Before planning, scan what exists. Match depth to scope:

- **Light:** Search for relevant files, check for prior art. 30 seconds.
- **Standard/Deep:** Read relevant source files, check `~/docs/solutions/` for learnings, note patterns to follow. Check for system-wide impacts: what callbacks, middleware, or observers fire when this code runs? What breaks if this fails halfway?

If local context is sufficient, skip external research. If the domain is unfamiliar or high-risk (security, payments, external APIs), do targeted web research before planning.

## The Plan

### Structure

Scale the plan to the work. A 3-step task gets a compact plan. A cross-cutting feature gets full treatment.

**Every plan starts with:**

```markdown
---
date: YYYY-MM-DD
topic: <kebab-case>
origin: ~/docs/brainstorms/YYYY-MM-DD-<topic>.md  # if one exists
---

# <Feature Name>

**Goal:** [One sentence — what this builds and why]

**Approach:** [2-3 sentences — how, and key technical choices]
```

### File Map

Before defining tasks, map every file that will be created or modified:

```markdown
## Files

- Create: `exact/path/to/new_file.py` — [what it does]
- Modify: `exact/path/to/existing.py` — [what changes]
- Test: `tests/exact/path/to/test_file.py` — [what it covers]
```

This is where decomposition decisions get locked in. Each file should have one clear job. Files that change together should live together.

### Tasks

Each task is a self-contained unit that produces a working, testable increment. A task that leaves things broken is too big or wrongly scoped.

````markdown
### Task N: [Component Name]

**Files:** `path/to/file.py`, `tests/path/to/test.py`

- [ ] Write failing test

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] Verify it fails — `pytest tests/path/test.py::test_name -v` → FAIL

- [ ] Implement

```python
def function(input):
    return expected
```

- [ ] Verify it passes — `pytest tests/path/test.py::test_name -v` → PASS

- [ ] Commit — `git commit -m "feat: add specific behavior"`
````

**The standard is TDD.** Write the test first, watch it fail, implement minimally, watch it pass, commit. Every task follows this rhythm unless testing genuinely doesn't apply (pure config, documentation, CI changes).

### Task Granularity

Each step is one action, 2-5 minutes:
- "Write the failing test" — one step
- "Run it to verify failure" — one step
- "Implement minimal code" — one step
- "Verify pass" — one step
- "Commit" — one step

If a step takes more than 5 minutes to describe or execute, it's multiple steps.

### What Goes in the Plan

- **Exact file paths.** Always.
- **Complete code.** Not "add validation" — the actual code.
- **Exact commands with expected output.** Not "run the tests" — the specific command and what success looks like.
- **Why, not just what.** When a choice isn't obvious, explain the reasoning in a sentence.

### What Stays Out

- Alternative approaches already rejected in transcription (link to origin doc)
- Future considerations and extensibility (YAGNI)
- Resource estimates and timelines
- Issue tracker integration

## Save

Write the plan to `~/docs/plans/YYYY-MM-DD-<topic>-plan.md`. Confirm the path.

## Handoff

State the plan path and recommend `/folding` for execution. Don't start implementing — the user decides when.

If the plan is small enough that full delegation is overkill (2-3 tasks, all straightforward), say so: "This is small enough to just execute directly."

## Principles

- **Zero-context execution.** An agent reading only this plan should be able to execute it without asking questions. If they'd need to ask, the plan is incomplete.
- **TDD by default.** Tests first. Exceptions must be justified.
- **Complete code, not descriptions.** "Add error handling for X" is not a plan step. The actual error handling code is.
- **One working increment per task.** Never leave the system broken between tasks.
- **Scale ceremony to scope.** Don't write a 50-step plan for a 3-step job.
