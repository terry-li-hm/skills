---
name: delegate
description: "Delegate coding tasks to OpenCode (free) or Codex (paid). Auto-packages context and runs backgrounded."
user_invocable: true
---

# Delegate

One command to delegate coding tasks. Routes to the right tool, packages context, runs backgrounded.

## Triggers

- `/delegate <task>` — route to OpenCode (default)
- `/delegate --codex <task>` — escalate to Codex (paid)
- Also trigger proactively when a coding task doesn't need vault context or judgment

## Routing

| Signal | Route to | Why |
|--------|----------|-----|
| Routine coding, refactoring, bulk ops, tests | **OpenCode** (GLM-5) | Free, unlimited |
| OpenCode failed 2-3x, deep bug, complex feature | **Codex** (GPT-5.2-codex) | Smarter, paid |
| **Code review** of a package/module | **Codex** | Reads broadly, writes structured findings |
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

## Code Review Pattern (Codex)

Codex handles full-package code reviews well. Pattern:
1. Give file paths + line counts + module descriptions (not file contents)
2. List specific focus areas (error handling, duplication, async, bugs, types)
3. Ask it to write findings to a `REVIEW.md` with severity + line references
4. Triage the output — Codex finds real bugs but also suggests over-engineering. Filter.
5. Delete `REVIEW.md` before committing (artifact, not source)

**Parallel review from both tools:** Launch Codex + OpenCode review simultaneously with different output files (`REVIEW-codex.md`, `REVIEW-opencode.md`). They have complementary strengths — Codex finds architectural issues and subtle races; OpenCode catches product/UX concerns and gives concrete fix snippets. Triage by consensus: findings both flag are real bugs; tool-unique findings need judgment. Tested on doumei (Feb 2026): 4 consensus bugs + 1 good unique find each.

**Parallel fixes after review:** Launch one OpenCode per fix in parallel. Keep prompts to "read this range, change X to Y, run tests". OpenCode handles simple substitutions; complex structural transforms (nested try/except wrapping) silently stall — do those directly.

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
| Empty output with `&` | Shell backgrounds before OpenCode starts | Never use `&` — use Bash tool's `run_in_background: true` instead |
| Wrong files modified | Ambiguous paths | Use absolute paths, specify exact method/line |
| Codex "stdin is not a terminal" | Using bare `codex` instead of `codex exec` | Use `codex exec --skip-git-repo-check --full-auto "prompt"` for headless. Bare `codex` is interactive-only |
| OpenCode `run` rejects file reads | Sandboxes to project root, auto-rejects `external_directory` | Bundle target files into `/tmp/` first: `cat files... > /tmp/bundle.md`, then `opencode run "read /tmp/bundle.md"` |

**If OpenCode fails twice on the same task:** Escalate to Codex (`codex --model o4-mini "prompt"`, paid — uses OpenAI credits) or do it directly in Claude. Don't retry with the same prompt.

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
- **Prompt budget:** ~4K chars max for OpenCode, ~8K for Codex. When in doubt, `echo -n "prompt" | wc -c`
- **Output often empty:** OpenCode doesn't reliably capture stdout. Check session JSON instead.
