---
name: dev
description: Structured on-ramp for delegate-first dev work. Use at the start of any coding task. Runs solutions KB check → CE plan → delegate → review.
user_invocable: true
---

# /dev — Delegate-First Dev Workflow

Structured on-ramp for any coding task. Enforces: orchestrate here, execute elsewhere.

## Triggers

- `/dev <task description>` — start a coding task the right way
- Proactively when user asks to build, port, fix, refactor, or add a feature

## Steps

### 1. Solutions KB check
```bash
cerno "<topic or tool name>"
```
Read the result. If prior art exists, use it. Don't duplicate captured learnings.

### 2. Choose weight class

| Task size | Use |
|-----------|-----|
| < 3 files, self-contained fix | Plan mode (`EnterPlanMode`) → delegate |
| Multi-file feature, needs paper trail | `/workflows:plan` → delegate |
| Unclear requirements | `/workflows:brainstorm` first |
| Plan exists, ready to execute | Skip to delegation |

### 3. Delegate execution

**Pick the right tool:**

| Signal | Tool | Why |
|--------|------|-----|
| Needs repo navigation, test loops, multi-file | **Codex** | Best developer (Terminal-Bench #1) |
| Algorithmic, isolated logic, "write X that does Y" | **Gemini CLI** | Best programmer (LiveCodeBench #1), free |
| Bulk ops, boilerplate, routine refactoring | **OpenCode** | Free, unlimited |
| Hard task that failed 3+ times | **→ Opus in-session** | Escalation only, switch back after |

**Context packaging checklist** (delegates need to be self-sufficient):
- [ ] Absolute file paths (let delegate read, don't inline full files)
- [ ] Error output if debugging (trim to relevant lines)
- [ ] Constraints ("don't modify X", "keep existing patterns")
- [ ] Verification command ("run `cargo test` to verify")
- [ ] Anti-placeholder: "Implement fully. No stubs, no TODOs, no simplified versions."
- [ ] Prompt length: OpenCode hard limit ~4K chars, Codex ~8K chars safe

**Launch backgrounded:**
```bash
# Codex
codex exec --skip-git-repo-check --full-auto "<prompt>"

# Gemini
gemini -p "<prompt>" --yolo

# OpenCode
OPENCODE_HOME=~/.opencode-lean opencode run \
  -m zhipuai-coding-plan/glm-5 \
  --title "<title>" \
  "<prompt>"
```
Use Bash tool's `run_in_background: true` — not shell `&`.

### 4. Review (for significant changes)

Run review agents in order:
1. `pattern-recognition-specialist` — spec compliance first
2. `kieran-rust-reviewer` / `kieran-python-reviewer` / `kieran-typescript-reviewer`
3. `security-sentinel` — if handles input, auth, or secrets
4. `code-simplicity-reviewer` — YAGNI check last

### 5. Compound (if non-obvious solve)
```
/workflows:compound
```
Captures the learnings in `~/docs/solutions/`.

## Defaults by Language

| Language | Default tool | Caveats |
|----------|-------------|---------|
| Rust | Codex | Check Rust regex crate: no lookahead. `cargo clean -p <crate>` if stale build. |
| Python | Gemini or OpenCode | Use `uv` not pip. Single-file scripts: `uv run --script` shebang. |
| TypeScript | Codex or Gemini | pnpm, not npm. |
| Shell scripts | OpenCode | New `~/bin/` scripts must be Python (bash-guard). |

## Hard Rules

- **Never write non-trivial code in-session** without proposing delegation first.
- **One task per delegation.** If there are 3 independent tasks, launch 3 separate delegates.
- **Don't inline full files.** Give paths, let delegates read.
- **Delegates don't write tests by default.** Add a separate test task if needed.
- **Review `git diff --stat` scope** after Gemini delegates — it touches extra files.
