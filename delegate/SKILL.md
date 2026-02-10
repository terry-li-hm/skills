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
| Routine coding, refactoring, bulk ops, tests | **OpenCode** (GLM-4.7) | Free, unlimited |
| OpenCode failed 2-3x, deep bug, complex feature | **Codex** (GPT-5.2-codex) | Smarter, paid |
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
  -m zhipuai-coding-plan/glm-4.7 \
  --title "<short title>" \
  "<packaged prompt>" &
```

**Codex (escalation):**
```bash
codex exec --skip-git-repo-check "<packaged prompt>" &
```

Always append `&` to background the task.

### 3. Confirm and Monitor

After launching, tell the user:
- What was delegated and to which tool
- How to check progress:
  - OpenCode: `/bin/ls -lt ~/.local/share/opencode/storage/session/` then read session JSON
  - Codex: check output file or `codex resume --last`

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
| Wrong files modified | Ambiguous paths | Use absolute paths, specify exact method/line |

**If OpenCode fails twice on the same task:** Escalate to Codex or do it directly. Don't retry with the same prompt.

## Notes

- **OpenCode model:** Always `zhipuai-coding-plan/glm-4.7` (NOT `opencode/glm-4.7` which depletes credits)
- **Lean config:** `OPENCODE_HOME=~/.opencode-lean` skips MCPs, cuts startup from 60s to 15s
- **Prompt budget:** ~4K chars max for OpenCode, ~8K for Codex. When in doubt, `echo -n "prompt" | wc -c`
- **PII:** If prompt contains personal info, mask first: `cd ~/skills/pii-mask && uv run mask.py "<prompt>"`
- **Output often empty:** OpenCode doesn't reliably capture stdout. Check session JSON instead.
