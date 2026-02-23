---
name: delegate
description: "Delegate coding tasks to OpenCode (free), Gemini CLI (free, 1500 RPD), or Codex (paid). Auto-packages context and runs backgrounded."
user_invocable: true
---

# Delegate

One command to delegate coding tasks. Routes to the right tool, packages context, runs backgrounded.

## Triggers

- `/delegate <task>` — route to OpenCode (default)
- `/delegate --gemini <task>` — route to Gemini CLI (free, daily-limited)
- `/delegate --codex <task>` — escalate to Codex (paid)
- Also trigger proactively when a coding task doesn't need vault context or judgment

## Routing

| Signal | Route to | Why |
|--------|----------|-----|
| Routine coding, refactoring, bulk ops, tests | **OpenCode** (GLM-5) | Free, unlimited |
| Needs better reasoning than GLM-5, but not worth Codex credits | **Gemini CLI** (Auto: 3 Pro / 2.5 Flash) | Free, 1500 RPD (AI Pro plan), smarter than GLM-5 |
| OpenCode + Gemini failed, deep bug, complex feature | **Codex** (GPT-5.2-codex) | Smartest, paid |
| **Code audit/review** | **Codex** (GPT-5.2) first | 92% signal. GLM-4.7 needs two-phase prompt (25% signal). See audit section below |
| Needs vault, user decisions, judgment | **Stay in Claude** | Context advantage |

## Workflow

### 1. Package Context

Before building the command, gather what the delegate needs to be self-sufficient:

- **Include file paths** as absolute paths — let the delegate read files itself
- **Include error output** if debugging (trimmed to relevant lines)
- **Include constraints** ("don't modify X", "keep existing patterns")
- **Include verification** ("run `pytest tests/` to verify")

**CRITICAL — Prompt Length Limits:**
- **OpenCode: hard limit ~4K chars.** Prompts >5K chars silently fail (exits 0, writes nothing).
- **Codex: ~8K chars safe**, can handle more context.
- **Never inline full file contents** in the prompt. Instead, give paths and tell the delegate to read them.
- **One focused task per prompt.** If you have 3 independent tasks, launch 3 separate delegations.
- Count your prompt length before sending. If it exceeds the limit, split or trim.

### 2. Build and Run

**OpenCode (default):**
```bash
OPENCODE_HOME=~/.opencode-lean opencode run \
  -m zhipuai-coding-plan/glm-5 \
  --title "<short title>" \
  "<packaged prompt>"
```

**Gemini CLI (mid-tier):**
```bash
gemini -p "<packaged prompt>" --yolo
```

**Codex (escalation):**
```bash
codex exec --skip-git-repo-check --full-auto "<packaged prompt>"
```

Use the Bash tool's `run_in_background: true` to background — not shell `&`.

### 3. Confirm and Monitor

After launching, tell the user:
- What was delegated and to which tool
- How to check progress:
  - OpenCode: `/bin/ls -lt ~/.local/share/opencode/storage/session/` then read session JSON
  - Codex: check output file or `codex resume --last`

## Code Audit Pattern

### Codex (GPT-5.2) — primary auditor

92% signal rate (11/12 real bugs on rai.py). Use for all audits.

```bash
codex exec --skip-git-repo-check --full-auto \
  "Perform a thorough code audit of <file>. Focus on: bugs, data integrity, edge cases, error handling, security, race conditions, logic errors. For each finding: severity (HIGH/MED/LOW), line numbers, the bug, suggested fix."
```

Triage: Codex finds real bugs but also suggests over-engineering. Ask "would I notice this during actual use?" to filter.

### OpenCode (GLM-4.7) — secondary, needs two-phase prompt

**Naive prompt → 0% signal** (25 false positives). GLM pattern-matches vulnerability templates without verifying.

**Two-phase prompt → 25% signal** (1/4 real, found a bug Codex missed):

```bash
opencode run --model opencode/glm-4.7 \
  "Phase 1: Read <file> thoroughly. This is a <context — personal CLI / server / library>. List all potential bugs, but DO NOT report yet.

Phase 2: For EACH potential finding, re-read the specific lines to verify:
- Does the bug actually exist in the current code?
- Is there already a guard/check that handles it?
- Is it relevant for <context>?

Only report findings that survive verification. For each: severity, exact line numbers, the actual buggy code (quote it), why it's real, suggested fix. Drop anything that doesn't survive Phase 2."
```

### Parallel audit (recommended for important code)

Launch Codex + OpenCode two-phase simultaneously. Codex catches most bugs; GLM occasionally finds edge cases Codex misses. Triage by consensus: findings both flag are high confidence; tool-unique findings need judgment.

### After audit: parallel fixes

Launch one OpenCode per fix in parallel. Keep prompts to "read this range, change X to Y, run tests". OpenCode handles simple substitutions; complex structural transforms silently stall — do those directly.

## Prompt Template

Keep under **4K chars for OpenCode**, **8K for Codex**. Never inline file contents — give paths.

```
In <file path>, <what to change>.

<Specific instructions — method names, line numbers, logic to add/modify>

<Constraints — what NOT to touch>

Run <test command> after changes to verify.
```

**Good (380 chars):**
> In src/oghma/cli.py, add a new CLI command 'promote' that takes a memory_id argument. Fetch the memory with storage.get_memory_by_id(), update its category to 'promoted' with a new update_memory_category() method in storage.py. Use rich for output. Run pytest after.

**Bad (5K+ chars):**
> Here is the full content of cli.py: [600 lines]... Here is storage.py: [800 lines]... Now add a promote command...

## Proactive Delegation

When a coding task arrives that's clearly routine (refactoring, file moves, test writing, boilerplate), propose delegation before executing:

> "This looks like a good candidate for OpenCode — want me to delegate it?"

This saves Claude tokens for work that actually needs orchestration and judgment.

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Exits 0, no files changed | Prompt >5K chars | Shorten prompt, remove inline content |
| Timeout after 5min | Task too small (<25 lines) or too vague | Give more specific instructions or do it directly |
| Hangs indefinitely | GLM-5 connection stall | Kill and write directly. Set Bash timeout or use `run_in_background` with periodic checks |
| Gemini "quota exceeded" | Hit 1500 RPD or 120 RPM limit | Wait or switch to OpenCode/Codex. Note: one prompt = many API requests |
| Gemini 429 `MODEL_CAPACITY_EXHAUSTED` | Flash preview has limited server capacity | Auto-retries with backoff. If persistent, force Pro: `gemini -p "prompt" --yolo -m gemini-3-pro` |
| Gemini no file changes | Sandbox mode blocked writes | Ensure `--yolo` flag is set (auto-approves all tool actions) |
| Empty output with `&` | Shell backgrounds before OpenCode starts | Never use `&` — use Bash tool's `run_in_background: true` instead |
| Wrong files modified | Ambiguous paths | Use absolute paths, specify exact method/line |
| Codex "stdin is not a terminal" | Using bare `codex` instead of `codex exec` | Use `codex exec --skip-git-repo-check --full-auto "prompt"` for headless. Bare `codex` is interactive-only |
| OpenCode `run` rejects file reads | Sandboxes to project root, auto-rejects `external_directory` | Bundle target files into `/tmp/` first: `cat files... > /tmp/bundle.md`, then `opencode run "read /tmp/bundle.md"` |
| OpenCode doesn't overwrite output file | Writes to new session, old file persists | Delete target output files before launching review. Or use unique names (e.g. `REVIEW-opencode-$(date +%s).md`) |

**If OpenCode fails twice on the same task:** Escalate to Gemini CLI (`gemini -p "prompt" --yolo`, free but daily-limited) or Codex (`codex exec --full-auto "prompt"`, paid). Don't retry with the same prompt.

## PII Masking

When prompts contain personal info (salary, phone, names), mask before sending to external LLMs:

```bash
cd /Users/terry/skills/pii-mask
masked=$(uv run mask.py "Question with personal details...")
```

Preview what gets masked: `uv run mask.py --dry-run "your text"`
Custom entities only: `uv run mask.py --entities "PHONE_NUMBER,EMAIL_ADDRESS" "text"`

**Detected entities:** Email, phone (+852 format), names, credit cards, IPs, locations, HK IDs, dates, URLs.
Uses Microsoft Presidio with HK-specific custom patterns.

**When NOT to mask:** Prompts to Claude Code directly (same trust boundary), code-only prompts, when PII is essential to the task.

## Notes

- **OpenCode model:** Always `zhipuai-coding-plan/glm-5` (NOT `opencode/glm-5` which depletes credits)
- **Lean config:** `OPENCODE_HOME=~/.opencode-lean` skips MCPs, cuts startup from 60s to 15s
- **Gemini CLI:** Auto-routes to Gemini 3 Pro (complex) or 2.5 Flash (simple) via Google AI Pro plan. 120 RPM, 1500 RPD. One prompt triggers multiple API requests internally — budget ~250-500 actual prompts/day. No prompt length issue (1M context). Force model with `-m gemini-3-pro` if needed.
- **Gemini 3.1 Pro:** Released Feb 19, model ID `gemini-3.1-pro-preview` — CLI v0.29.5 can't access yet (ModelNotFound). Monitor for update.
- **Prompt budget:** ~4K chars max for OpenCode, ~8K for Codex, generous for Gemini. When in doubt, `echo -n "prompt" | wc -c`
- **Output often empty:** OpenCode doesn't reliably capture stdout. Check session JSON instead.
- **GLM-5 broken in OpenCode** (both interactive and headless) — malformed tool call JSON ([#13982](https://github.com/anomalyco/opencode/issues/13982), [#13900](https://github.com/anomalyco/opencode/issues/13900)). Causes silent infinite retry loops. GLM-4.7 still works. Use `glm-4.7` or GPT until fixed upstream.
- **GPT-5.2 Thinking:** Available via OpenAI API ($1.75/$14/Mtok). Best-in-class for reading comprehension, long-context, vision (chart/diagram analysis). xhigh reasoning effort. Route document-heavy analysis here.
- **GPT-4.5:** Deprecated from API Jul 2025. ChatGPT Pro "Legacy" only. Not automatable.
- **Gemini maxOutputTokens gotcha:** Default ~8192 tokens. Set 65536 in generationConfig for long outputs. API silently caps to model's actual max — safe to pass a large value.
- **Delegated AI builds well, never consolidates:** Great for greenfield + targeted bug fixes. But each fix is locally scoped — accumulates structural debt. Plan a human/Claude Code consolidation pass after every 5-10 delegated hardening commits.

## Codex-Specific

- **Headless:** `codex exec --skip-git-repo-check --full-auto "prompt"` (NOT bare `codex` which needs TTY).
- **OpenCode headless:** `opencode run "prompt"` but **sandboxes file reads to project root** — auto-rejects `external_directory`. Workaround: bundle files into `/tmp/` first.
