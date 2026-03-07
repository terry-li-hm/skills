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

### −1. Should we build at all?

Before scoping, ask: **is this a one-off or a recurring need?**

| Signal | Action |
|--------|--------|
| Will run this logic >1 time | Build a proper CLI or skill — not a script |
| Ad-hoc data wrangling, truly once | Inline Python/bash is fine |
| Unsure | Default to building — purge cost is `deleo <path>`, rewrite cost is an hour |

Build cost is low (delegated to Codex/OpenCode). Purge cost is near-zero. Rewriting ad-hoc scripts repeatedly costs more than a tool that might get deleted.

### 0. Pre-flight (before anything else)

**Data governance gate — before any delegation:**
Can this code leave the machine? Check:
- No `.env`, secrets, credentials, or production data in scope
- No proprietary client code that can't go to external CLIs (Codex/Gemini run on third-party infra)
- If unsure → local-only tools (Opus in-session) or redact before delegating

**Break-glass (hotfix only):**
If a production incident requires skipping this workflow, that's allowed — but not silent. Create a `HOTFIX_BYPASS.md` at repo root documenting: what was skipped, why, and a post-hoc review task. Without this artifact, "it was urgent" becomes the universal excuse to skip planning.

**Parallel agent sessions on the same repo?** → `lucus new <branch>` first. One worktree per session prevents `git add -A` conflicts between delegates. See `~/skills/lucus/SKILL.md`.
- If `lucus` is unavailable, continue in current worktree and explicitly warn about merge/conflict risk.

**Naming anything (CLI, skill, or tool)?** → Follow `artifex` naming convention: consilium first, crates.io check for every candidate, reserve before planning.

### 1. Solutions KB check
```bash
cerno "<topic or tool name>"
```
Read the result. If prior art exists, verify it still applies (check dates, tool versions, repo state) before using. Don't blindly reuse stale KB entries — a bad solution propagates indefinitely.
If `cerno` fails or returns no results, continue and note "No KB prior art found".

### 2. Choose weight class

Default to `/workflows:plan`. Use `EnterPlanMode` only as the exception.

| Task size | Use |
|-----------|-----|
| **Trivial:** new skill file, single script <50 lines, clear spec, no existing code touched, zero cascading changes | **Build directly in-session** — skip CE plan and delegation |
| Single-file, ≤3 commands, no architecture decisions, requires live user decisions mid-plan | `EnterPlanMode` → delegate |
| **New project / fresh codebase** (blank repo, new crate, no existing code to research) | `superpowers:brainstorming` → `superpowers:writing-plans` → `superpowers:subagent-driven-development` — CE research agents find nothing on blank repos; skip them |
| Multi-command CLI, new architecture, requires vault context or cross-file reasoning | `/slfg <description>` — fully autonomous (plan → deepen → CE swarm → review). Burns Max20 — use only when vault context is essential. |
| Same as above but Max20 is low, or tasks map cleanly to independent files | `/ce:plan` → `/deepen-plan` → **external swarm** (lucus + parallel delegates) → `/ce:review` |
| Unclear requirements | `/workflows:brainstorm` first |

**CE + superpowers hybrid (existing codebase, in-session execution):**
CE research first → superpowers execution loop. Best of both: CE's `learnings-researcher` + `repo-research-analyst` surface institutional gotchas; superpowers' two-stage per-task review (spec compliance → code quality) catches over-building.
```
CE: learnings-researcher + repo-research-analyst   ← surface codebase gotchas
superpowers:writing-plans                           ← convert to TDD task steps
superpowers:subagent-driven-development             ← execute with per-task review
CE: security-sentinel + kieran-*-reviewer           ← thorough final review
```
Skip CE plan (redundant with writing-plans). Use hybrid when: existing codebase with KB history + want tight per-task review loops in-session.

**External tool override inside subagent-driven-development:**
When dispatching the implementer subagent, route by task signal instead of always using `general-purpose`:
| Signal | Implementer |
|--------|-------------|
| Rust + needs `cargo build`/`cargo test` | Gemini CLI (`gemini -p "..." --yolo`, `run_in_background: true`) |
| Multi-file, repo navigation | Codex (`codex exec --full-auto "..."`) |
| Boilerplate / bulk | OpenCode |
| Default / everything else | `general-purpose` subagent (current default) |
Reviews (spec compliance + code quality) always stay as Claude subagents regardless of implementer choice.

**`/slfg` vs external swarm:**
- `/slfg` = Claude Task agents, burns Max20, fully automated, no manual decomposition
- External swarm = Codex/Gemini/OpenCode in parallel worktrees, free, requires manual decomposition + merge
- **Default to external swarm.** Use `/slfg` only when the task requires vault context or cross-file reasoning that can't be captured in a task spec. "It's easier" is not a reason to burn Max20.

**Rule of thumb:** If you'd build more than one file, touch existing architecture, or need research agents to surface best practices → `/workflows:plan`. `EnterPlanMode` is for trivial tasks where the user needs to make live decisions as the plan unfolds.

**HARD GATE — EnterPlanMode is ONLY valid when ALL of these are true:**
- Single file touched (or two files with trivially obvious changes)
- No new types/enums/structs being added
- No function signature changes propagating to other files
- User must make live decisions mid-plan that you can't anticipate

**Anti-pattern (do NOT rationalize past this):** "User already knows what they want, requirements are clear, so EnterPlanMode is fine." → WRONG. Clear requirements are exactly when CE plan adds most value — it surfaces codebase gotchas and KB learnings the user doesn't know about, not requirements. In one real case: a "simple" CLI flag + enum change had 25 cascading signature changes, a missing provider branch, a dedup bug in quick_models(), and an Anthropic max_tokens constraint — none visible from the feature description. CE plan caught all of them. EnterPlanMode caught none.

**Approved plan ≠ skip CE plan:** Even if you have an approved plan (from EnterPlanMode or brainstorm), run CE plan anyway before delegating — unless the plan already came from `/ce:plan` against the current repo HEAD. CE plan deepens with codebase-specific gotchas. It's additive, not duplicative.

**Why CE plan beats built-in plan:** `/workflows:plan` runs `learnings-researcher` + `repo-research-analyst` in parallel — surfacing `~/docs/solutions/` gotchas and exact patterns from reference projects. Built-in plan is a single-model think-through that misses institutional knowledge entirely. In practice, CE plan catches things like wrong crate versions, agent-first output requirements, implementation ordering, and Codex delegation gotchas that built-in plan never surfaces. The cost is ~2 min of research time; the benefit compounds with every prior solution captured in the KB.

### 3. Delegate execution

**Pick the right tool:**

| Signal | Tool | Why |
|--------|------|-----|
| Needs repo navigation, test loops, multi-file | **Codex** | Best developer (Terminal-Bench #1) |
| **Rust feature requiring `cargo build` validation** | **Gemini CLI** | Runs on your machine — discovers compile errors. Codex sandbox blocks DNS/cargo. |
| Algorithmic, isolated logic, "write X that does Y" | **Gemini CLI** | Best programmer (LiveCodeBench #1), free |
| Bulk ops, boilerplate, routine refactoring | **OpenCode** | Free, unlimited |
| Task failed 3+ times from **reasoning difficulty** | **→ Opus in-session** | Escalation only, switch back after |
| Task failed from **sandbox constraint** (DNS, build, write access) | **→ Switch tool laterally** | Codex DNS failure → Gemini; OpenCode write block → Codex. Not a reasoning problem. |
| **Rust complex bug (diagnosis only)** | **Codex → Gemini handoff** | Codex navigates + diagnoses; Gemini builds/verifies locally. Pass Codex output as context to Gemini. |
| Routing uncertain despite benchmarks | **Run `judex` experiment** | Parallel Codex+Gemini → real evidence → update routing |

**Context packaging checklist** (delegates need to be self-sufficient):
- [ ] Absolute file paths (let delegate read, don't inline full files)
- [ ] Error output if debugging (trim to relevant lines)
- [ ] Constraints ("don't modify X", "keep existing patterns")
- [ ] Verification command ("run `cargo test` to verify")
- [ ] Anti-placeholder: "Implement fully. No stubs, no TODOs, no simplified versions."
- [ ] Prompt length: OpenCode hard limit ~4K chars, Codex ~8K chars safe
- [ ] **Patch receipt request:** "End your response with: Files touched: [...], Commands run: [...], Tests added: [...], Risks: [...]"

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
If chosen delegate command fails immediately, switch once to a backup tool based on task type; if backup fails, stop and report delegation blocked.

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

**Sequential dependent phases? Use Phase Contract pattern** (`~/docs/solutions/phase-contract-pattern.md`):
- Each phase runs as a fresh-context subagent → produces a file artifact + JSON summary
- Orchestrator validates JSON contract before launching next phase
- On `"status": "failed"` → stop and restart from that phase, not the beginning
- Complements swarm: use swarm for parallel independent tasks, phase contracts for sequential dependent tasks

**Rules for external swarm:**
- **Commit the plan before `lucus new`** — worktrees only see committed history. Uncommitted plan files are invisible to delegates.
- Decompose the plan first — tasks must be truly independent (different files)
- One `lucus` worktree per delegate — never share a worktree
- Mix tools by task type: Codex for multi-file/repo nav, Gemini for algorithmic, OpenCode for boilerplate
- Review `git diff --stat` per branch before merging — Gemini touches extra files
- **Gemini executes live mutations during testing** — if the CLI wraps a live service (calendar, WhatsApp, DB), expect real side effects during Gemini's verification pass. Brief with a test fixture or accept live side effects and clean up after.
- Merge conflicts = tasks weren't independent enough; phase them next time
- If any delegate branch fails, do not merge partial branches blindly; finish successful branches first, then re-scope failed task as a new single delegation.

### 4. Review (for significant changes)

**New feature / significant PR → `/workflows:review`** (runs all agents with worktrees, most thorough)

For targeted/quick review, run agents directly in order:
1. `pattern-recognition-specialist` — spec compliance first
2. `kieran-rust-reviewer` / `kieran-python-reviewer` / `kieran-typescript-reviewer`
3. `security-sentinel` — if handles input, auth, or secrets
4. `code-simplicity-reviewer` — YAGNI check last

**Optional static security gate (production code / published packages):**
Run after `security-sentinel` when code handles external input, auth, or is published:
- `/diff-review` — security-focused diff review (Trail of Bits `differential-review` plugin)
- `semgrep` skill — pattern-based vulnerability detection (`static-analysis` plugin)
- `codeql` skill — deep static analysis (`static-analysis` plugin)
- `insecure-defaults` skill — hardcoded credentials, fail-open patterns

Skip for: personal scripts, internal tools, leaf-node changes with no external surface.

**Before marking any task done — System-Wide Test Check** (stolen from CE `/ce:work`):

| Question | What to check |
|----------|---------------|
| What fires when this runs? | Callbacks, middleware, hooks — trace two levels out. Read actual code, not docs. |
| Do my tests exercise the real chain? | If every dep is mocked, the test proves isolation only. Write ≥1 integration test through the real chain. |
| Can failure leave orphaned state? | If state is persisted before a risky call — does retry create duplicates? Test the failure path. |
| What other interfaces expose this? | Grep for the method in related classes. If parity needed, add it now. |
| Do error strategies align across layers? | Retry middleware + app fallback + framework handler — do they conflict or double-execute? |

Skip when: leaf-node change, purely additive, no callbacks or state persistence.
If review agents are unavailable, run a manual `git diff` + smoke test and mark review as "manual fallback".

### 5. Companion skill + GitHub repo + crates.io (for any installed CLI or published tool)

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
If commit/push fails, keep the skill file and report "Companion skill not committed" with the failing command.

**GitHub backup — do this every session for any CLI built or modified:**
```bash
# If repo doesn't exist yet:
cd ~/code/<name> && git init && git add -A && git commit -m "init: <name>"
gh repo create terry-li-hm/<name> --private --source . --push
# If repo exists, just push:
git push
```
All personal CLIs are **private** by default. Flip to public only if genuinely general-purpose.

**crates.io — reserve name and/or publish if ALL of these are true:**
- [ ] General-purpose (useful to strangers, not just Terry's setup)
- [ ] Uses registered API credentials (not shared/Desktop creds like Telegram's 2040)
- [ ] No hardcoded personal paths, macOS-only assumptions, or Terry-specific keychain keys
- [ ] Willing to field issues

**Reserve name only (publish stub):** if you want the name but the tool isn't ready — do immediately after `cargo new`, names go fast.

**Skip crates.io:** personal tooling, hardcoded assumptions, credentials only Terry has.

Good candidates from existing CLIs: `exauro`, `caelum`, `poros`, `deleo` (general-purpose). Not ready: `graphis`, `auspex`, `amicus` (too personal as-is).

### 6. Compound (if non-obvious solve)
```
/workflows:compound
```
Captures the learnings in `~/docs/solutions/`.
If compound workflow is unavailable, add a short manual note in `~/docs/solutions/` instead.

## Defaults by Language

| Language | Default tool | Caveats |
|----------|-------------|---------|
| Rust | **Gemini** (if build validation needed) / Codex (repo nav) | Codex sandbox blocks DNS → can't run `cargo build` → can't discover compile errors. Use Gemini for Rust features where the verification requires building. Codex for complex multi-file repo navigation where compilation isn't the blocker. Rust regex: no lookahead. |
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

## Example

> `cerno "rust mcp auth"` returned 2 prior solutions, so plan reused existing auth pattern.
> Delegated implementation to Codex in a `lucus` worktree, then ran `/ce:review`.
> Smoke tests passed; companion skill file added and committed in `~/skills`.

## Boundaries

- Do NOT execute substantial implementation directly in-session except when delegation is blocked.
- Do NOT skip planning because prior discussion exists; this skill always enforces planning gate.
- Stop after orchestration, delegation, review routing, and companion-skill capture.

## Troubleshooting Delegation

When a delegate fails or behaves unexpectedly, check `~/docs/solutions/delegation-reference.md`.
Key quick-reference:
- OpenCode silent fail → prompt >4K chars
- Codex hangs → bundle files into `/tmp/` first
- Gemini no file changes → missing `--yolo`
- Double-backgrounded → never use `&` with `run_in_background: true`
- After Codex → always `git add && git commit` manually (sandbox blocks `.git`)

## Calls
- `cerno` — solutions KB check (step 1)
- `lucus` — for parallel worktree isolation
- `scrutor` — for post-implementation review
- `artifex` — for naming conventions
