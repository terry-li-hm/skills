---
name: choregos
description: "DEPRECATED — folded into strategos (swarm mode). Use /strategos instead."
---

# choregos — DEPRECATED

**Folded into `/strategos` as swarm mode (Step 3).** All parallel pipeline functionality — auto-routing, validation, summary, merge+escalate — is now in strategos.

Use `/strategos` for all coding tasks, including parallel execution.

## When to Use

- 2+ independent tasks (different files, no shared state)
- Tasks have clear validation commands (or can be inferred)
- Terry doesn't need to make routing decisions per task
- Terry is OK being AFK while delegates run

**NOT for:** tasks that touch the same files, need live Terry decisions, or involve external sends (WhatsApp, email, live APIs during testing).

## Step 1 — Decompose (if needed)

If given a feature description instead of a task list, decompose first:
- Break into independent sub-tasks (different files/modules)
- Each task must be fully self-contained (no shared state)
- If tasks can't be made independent, use sequential strategos instead

For each task, capture:
```
name:        short-kebab-name
spec:        full self-contained prompt (include file paths, constraints, verification cmd)
lang:        rust | python | typescript | other
validation:  cargo build && cargo test | uv run pytest | pnpm test | <custom>
```

## Step 2 — Pre-flight

```bash
# Ensure clean base for worktrees
git status  # if uncommitted changes, stash or commit first
git stash   # if needed

# Verify lucus available
lucus list
```

If `lucus` unavailable, stop and fall back to sequential strategos — don't attempt pipeline without worktree isolation.

## Step 3 — Auto-Route (no asking)

Route each task without asking Terry:

| Signal | Tool | Command |
|--------|------|---------|
| Rust (any) | Codex | `codex exec --sandbox danger-full-access --full-auto "<spec>"` |
| Multi-file, repo nav | Codex | `codex exec --full-auto "<spec>"` |
| New project, algorithmic | Gemini | `cd <worktree> && gemini -p "<spec>" --yolo` |
| Boilerplate, bulk | OpenCode | `OPENCODE_HOME=~/.opencode-lean opencode run -m zhipuai-coding-plan/glm-5 --title "<name>" "<spec>"` |

Report routing decisions inline: "→ feature-a: Codex (Rust), feature-b: Gemini (new logic), feature-c: OpenCode (boilerplate)"

## Step 4 — Create Worktrees

One per task, before launching any delegates:
```bash
lucus new <task-name-a>
lucus new <task-name-b>
lucus new <task-name-c>
```

Note each worktree path returned by lucus.

## Step 5 — Launch All in Parallel

Launch all delegates simultaneously using Bash `run_in_background: true` for each. Never use shell `&` — use the tool parameter.

```bash
# Example: Rust task in worktree
cd <worktree-a> && codex exec --sandbox danger-full-access --skip-git-repo-check --full-auto "<spec-a>"

# Example: Gemini task
cd <worktree-b> && gemini -p "<spec-b>" --yolo

# Example: OpenCode task
cd <worktree-c> && OPENCODE_HOME=~/.opencode-lean opencode run --title "<name-c>" "<spec-c>"
```

All launched in the same response. Print: "Launched N delegates. Waiting for completion..."

## Step 6 — Validate Each on Completion

As each background task completes (notification fires), immediately validate in that worktree:

```bash
cd <worktree-X> && <validation_cmd>
```

Record result:
- **Pass (exit 0):** ✓, run `git diff --stat` to capture scope
- **Fail (exit ≠ 0):** ✗, capture last 20 lines of error

Don't wait for all tasks before validating — validate as each completes.

## Step 7 — Summary

Once all tasks complete and validated, send summary:

```
Pipeline complete: N/M tasks passed

✓ feature-a   Codex    3 files   cargo test passed    2m14s
✓ feature-b   Gemini   1 file    cargo test passed    1m48s
✗ feature-c   Codex    —         cargo build failed   3m02s
✓ feature-d   OpenCode 2 files   (no test cmd)        0m55s
```

**If Terry is on Blink/iOS:** send via `deltos "<summary>"`.
**If Terry is on desktop (Ghostty):** output inline in chat.

## Step 8 — Merge Passing, Escalate Failures

**For each ✓ task:**
```bash
lucus merge <passing-branch>
```

**For each ✗ task:**
- Show full error
- Propose: retry with different delegate / fix in-session / skip
- Wait for Terry's call per failed task

Don't merge failing branches. Don't auto-fix without Terry's input.

## Step 9 — Final commit

After all merges:
```bash
git add -A && git commit -m "pipeline: <summary of what shipped>"
git push
```

## Routing Overrides

Terry can override auto-routing inline:
- "use Gemini for all" → override tool for all tasks
- "skip validation" → skip Step 6
- "notify on done" → always send deltos even on desktop

## Anti-Patterns

- **Don't share a worktree** between two tasks — conflicts guaranteed
- **Don't launch sequentially** — defeats the purpose
- **Don't merge without validation** — even if delegate exits 0
- **Don't auto-fix failures** — escalate to Terry
- **Don't use `&` with run_in_background: true** — double-backgrounding breaks output

## Calls

- `lucus` — worktree management
- `deltos` — mobile notification
- `strategos` — fallback for sequential tasks or unclear routing
