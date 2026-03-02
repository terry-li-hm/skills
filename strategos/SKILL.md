---
name: strategos
description: Structured on-ramp for delegate-first dev work. Use at the start of any coding task. Runs solutions KB check → CE plan → delegate → review.
user_invocable: true
---

# /strategos — Delegate-First Dev Workflow

Structured on-ramp for any coding task. Enforces: orchestrate here, execute elsewhere.

## Triggers

- `/strategos <task description>` — start a coding task the right way
- Proactively when user asks to build, port, fix, refactor, or add a feature
- **After consilium/brainstorm/design discussion when user says "implement", "build", "do it", "go ahead"** — prior discussion is NOT a plan, always start here

## Steps

### 0. Pre-flight (before anything else)

**Parallel agent sessions on the same repo?** → `lucus new <branch>` first. One worktree per session prevents `git add -A` conflicts between delegates. See `~/skills/lucus/SKILL.md`.

**Naming anything (CLI, skill, or tool)?** → Follow `design-skill` naming convention: consilium first, crates.io check for every candidate, reserve before planning.

### 1. Solutions KB check
```bash
cerno "<topic or tool name>"
```
Read the result. If prior art exists, use it. Don't duplicate captured learnings.

### 2. Choose weight class

Default to `/workflows:plan`. Use `EnterPlanMode` only as the exception.

| Task size | Use |
|-----------|-----|
| Single-file, ≤3 commands, no architecture decisions, requires live user decisions mid-plan | `EnterPlanMode` → delegate |
| Multi-command CLI, new architecture, Max20 pool healthy | `/slfg <description>` — fully autonomous (plan → deepen → CE swarm → review) |
| Same as above but Max20 is low, or tasks map cleanly to independent files | `/ce:plan` → `/deepen-plan` → **external swarm** (lucus + parallel delegates) → `/ce:review` |
| Unclear requirements | `/workflows:brainstorm` first |
| Approved plan already exists (any source) | Skip to `/ce:work` or external swarm |

**`/slfg` vs external swarm:**
- `/slfg` = Claude Task agents, burns Max20, fully automated, no manual decomposition
- External swarm = Codex/Gemini/OpenCode in parallel worktrees, free, requires manual decomposition + merge
- Default to `/slfg` unless Max20 is constrained or task decomposition is obvious from the plan

**Rule of thumb:** If you'd build more than one file, touch existing architecture, or need research agents to surface best practices → `/workflows:plan`. `EnterPlanMode` is for trivial tasks where the user needs to make live decisions as the plan unfolds.

**Why CE plan beats built-in plan:** `/workflows:plan` runs `learnings-researcher` + `repo-research-analyst` in parallel — surfacing `~/docs/solutions/` gotchas and exact patterns from reference projects. Built-in plan is a single-model think-through that misses institutional knowledge entirely. In practice, CE plan catches things like wrong crate versions, agent-first output requirements, implementation ordering, and Codex delegation gotchas that built-in plan never surfaces. The cost is ~2 min of research time; the benefit compounds with every prior solution captured in the KB.

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

**Launch backgrounded (single delegate):**
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

**Swarm mode (parallel external delegates):**

When the plan decomposes into N independent tasks, launch all at once — free, async, no Max20 cost.

```
# 1. One worktree per task (prevents git add -A conflicts)
lucus new <task-a-branch>
lucus new <task-b-branch>
lucus new <task-c-branch>

# 2. Launch all in parallel (Bash tool run_in_background: true for each)
cd <worktree-a> && codex exec --full-auto "<task A prompt>"
cd <worktree-b> && gemini -p "<task B prompt>" --yolo
cd <worktree-c> && opencode run --title "task-c" "<task C prompt>"

# 3. Wait for all to complete, then merge
lucus merge <task-a-branch>
lucus merge <task-b-branch>
lucus merge <task-c-branch>

# 4. Review merged result
/ce:review
```

**Rules for external swarm:**
- **Commit the plan before `lucus new`** — worktrees only see committed history. Uncommitted plan files are invisible to delegates.
- Decompose the plan first — tasks must be truly independent (different files)
- One `lucus` worktree per delegate — never share a worktree
- Mix tools by task type: Codex for multi-file/repo nav, Gemini for algorithmic, OpenCode for boilerplate
- Review `git diff --stat` per branch before merging — Gemini touches extra files
- Merge conflicts = tasks weren't independent enough; phase them next time

### 4. Review (for significant changes)

**New feature / significant PR → `/workflows:review`** (runs all agents with worktrees, most thorough)

For targeted/quick review, run agents directly in order:
1. `pattern-recognition-specialist` — spec compliance first
2. `kieran-rust-reviewer` / `kieran-python-reviewer` / `kieran-typescript-reviewer`
3. `security-sentinel` — if handles input, auth, or secrets
4. `code-simplicity-reviewer` — YAGNI check last

**Before marking any task done — System-Wide Test Check** (stolen from CE `/ce:work`):

| Question | What to check |
|----------|---------------|
| What fires when this runs? | Callbacks, middleware, hooks — trace two levels out. Read actual code, not docs. |
| Do my tests exercise the real chain? | If every dep is mocked, the test proves isolation only. Write ≥1 integration test through the real chain. |
| Can failure leave orphaned state? | If state is persisted before a risky call — does retry create duplicates? Test the failure path. |
| What other interfaces expose this? | Grep for the method in related classes. If parity needed, add it now. |
| Do error strategies align across layers? | Retry middleware + app fallback + framework handler — do they conflict or double-execute? |

Skip when: leaf-node change, purely additive, no callbacks or state persistence.

### 5. Companion skill (for any installed CLI or published tool)

Create `~/skills/<name>/SKILL.md` in the same session — gotchas are freshest now.

Minimum content:
- Commands with real examples
- File paths / config locations
- When to use it
- Gotchas discovered during build and testing (the stuff `--help` never covers)

```bash
mkdir -p ~/skills/<name>
# write SKILL.md, then:
cd ~/skills && git add <name>/SKILL.md && git commit -m "feat: add <name> skill" && git push
```

### 6. Compound (if non-obvious solve)
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

- **Prior discussion ≠ plan.** Consilium output, brainstorm notes, and design reviews are inputs to planning — not a substitute for it. Always run cerno + CE plan first.
- **Never write non-trivial code in-session** without proposing delegation first.
- **One task per delegation.** If there are 3 independent tasks, launch 3 separate delegates.
- **Don't inline full files.** Give paths, let delegates read.
- **Delegates don't write tests by default.** Add a separate test task if needed.
- **Review `git diff --stat` scope** after Gemini delegates — it touches extra files.

## Calls
- `cerno` — solutions KB check (step 1)
- `delegate` — for tool routing and prompt packaging
- `lucus` — for parallel worktree isolation
- `audit` — for post-implementation review
- `design-skill` — for naming conventions
