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

- **Read relevant files** mentioned in the task (full content, not snippets)
- **Include file paths** as absolute paths
- **Include error output** if debugging
- **Include constraints** ("don't modify X", "keep existing patterns")
- **Include verification** ("run `pytest tests/` to verify")

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

```
[Goal]: <what to achieve>
[Files]: <absolute paths to read/modify>
[Context]: <relevant code, errors, constraints>
[Verify]: <command to confirm success>
[Constraints]: <what NOT to do>
```

## Proactive Delegation

When a coding task arrives that's clearly routine (refactoring, file moves, test writing, boilerplate), propose delegation before executing:

> "This looks like a good candidate for OpenCode — want me to delegate it?"

This saves Claude tokens for work that actually needs orchestration and judgment.

## Notes

- **OpenCode model:** Always `zhipuai-coding-plan/glm-4.7` (NOT `opencode/glm-4.7` which depletes credits)
- **Lean config:** `OPENCODE_HOME=~/.opencode-lean` skips MCPs, cuts startup from 60s to 15s
- **PII:** If prompt contains personal info, mask first: `cd ~/skills/pii-mask && uv run mask.py "<prompt>"`
- **Output often empty:** OpenCode doesn't reliably capture stdout. Check session JSON instead.
