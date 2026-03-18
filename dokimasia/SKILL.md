---
name: dokimasia
description: Testing agent-written code — strategies when no human reads the code. Consult from rector (delegation step), opifex, and any agent-built CLI. Not user-invocable.
type: reference
disable-model-invocation: true
---

# Dokimasia — Testing What You Don't Read

> *Dokimasia (δοκιμασία): examination, scrutiny — the Athenian process of vetting candidates before they could serve. Testing agent-written code when no human reads the implementation.*

When agents write the code and humans don't read it, **tests are the specification, not verification.** The test suite IS the product spec. Everything else follows from this inversion.

## The Core Problem

An agent that writes both tests and implementation unconsciously aligns them. Tests verify what the code does, not what it *should* do. They pass on first run — which proves nothing.

## Two-Agent Pattern (Highest Leverage)

The strongest pattern for agent-written code quality:

1. **Test agent** sees only the spec/requirements. No implementation context. Writes failing tests.
2. **Implementation agent** sees only the failing tests + spec. Iterates until green.

Neither contaminates the other. The test agent can't write tests that match the implementation because it hasn't seen it. The implementation agent can't game the tests because it didn't write them.

**In rector's pipeline:** Step 4 delegation becomes two passes — test-first delegation, then implementation delegation.

## Practical QA Floor for CLI Tools

Ranked by value (do all four):

1. **Golden path integration test** — does `tool <primary use case>` produce sane output with real dependencies? Worth more than 50 mocked unit tests.
2. **Smoke test in cron/LaunchAgent** — `tool --no-send && echo OK || echo FAIL`. Runs in the actual environment daily. Catches environment drift that no test suite can.
3. **Shape assertions over exact assertions** — don't test exact output (brittle). Test: contains a date? Has a weather line? Exit code 0? Non-empty? Shape tests survive implementation changes.
4. **Exit code as contract** — for CLIs consumed by scripts/agents, the exit code IS the API. Test it explicitly.

## What Tests Can't Catch

| Failure mode | Why tests miss it | What catches it |
|-------------|-------------------|-----------------|
| **Spec gaps** (Cora label miss) | Tests test the spec as written, not the spec as intended | Integration tests against real environment |
| **Environment drift** (new labels, tool output changes) | Mocked tests freeze assumptions | Periodic live smoke tests |
| **Hallucinated conditions** (`if age == 43`) | Agent inserts to force test green | Two-agent pattern (test writer has no implementation context) |
| **Security bypasses** | Unit tests don't test authorization | Static analysis (SAST), security review |
| **False assumptions propagated across features** | Each test passes in isolation | Integration/E2E tests |

## Key Heuristics

- **If the test passes on first run, it proves nothing.** Watch it fail first (red-green). A test you never saw fail might be testing the wrong thing.
- **Mocks test the mock, not the code.** Agents love mocking because it makes tests green easily. Prefer real dependencies where possible.
- **"First run the tests"** (Willison) — four words at the start of any delegation prompt that force the agent into testing-first mode.
- **Fluency is not competence** (connects to mathesis). Tests passing ≠ code working. Integration test with real dependencies is the actual check.
- **The human's job is diff review, not code review.** Version control + CI provides the audit trail. The human reviews the diff (fast), not the full code (slow).

## When to Apply What

| Situation | Testing approach |
|-----------|-----------------|
| **Personal CLI, daily use** | Golden path + cron smoke test. Eyeballs are the integration test. |
| **Delegated feature in existing codebase** | Two-agent pattern. Test agent first, implementation agent second. |
| **One-off script** | Smoke test only. If it runs once and you see the output, that's sufficient. |
| **Shared tool / production** | Full: two-agent TDD + CI + type checking + security review |

## Sources

- Simon Willison: "Red/Green TDD" + "First Run the Tests" (agentic engineering patterns)
- Addy Osmani: "The 80% Problem in Agentic Coding"
- arxiv:2512.03262: agent-written code is 61% functionally correct but only 10.5% secure
- alexop.dev: isolated subagent TDD raised skill activation from ~20% to ~84%

## Wiring

Consult dokimasia from:
- **rector Step 4** — before delegating implementation, consider two-agent pattern
- **opifex** — when reviewing delegate output, check: did tests exist before implementation?
- **mathesis** — testing yourself (retrieval practice) IS learning; same principle applies to code
- **zetetike** — "does it work?" is an empirical question; experiment (test) trumps research (reading the code)
