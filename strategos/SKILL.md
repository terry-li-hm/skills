---
name: strategos
description: Structured on-ramp for delegate-first dev work. Use at the start of any coding task. Runs solutions KB check → CE plan → delegate → review.
user_invocable: true
---

# /strategos — Delegate-First Dev Workflow

Structured on-ramp for any coding task. Enforces: orchestrate here, execute elsewhere.

## Triggers

- `/strategos <task description>` — start a coding task the right way
- `/strategos --yolo <task>` — skip plan review (personal tools, low blast radius)
- Proactively when user asks to build, port, fix, refactor, or add a feature
- **After consilium/brainstorm/design discussion when user says "implement", "build", "do it", "go ahead"** — prior discussion is NOT a plan, always start here
- "pipeline these", "run all these in parallel", "do all of these" — auto-enters swarm mode (Step 3)

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

**Naming anything (CLI, skill, or tool)?** → **HARD GATE: name before code.** No `uv init`, `cargo new`, or scaffold until the name is confirmed available on the target registry (PyPI for Python, crates.io for Rust). Burned: built entire scaffold + delegated Chunk 1 as "mnemon", discovered PyPI was taken, had to rename everything. Flow: consilium `--quick` for candidates → check availability → reserve/publish stub → then scaffold. See `artifex` for naming conventions.

### 1. Solutions KB check
```bash
cerno "<topic or tool name>"
```
Read the result. If prior art exists, verify it still applies (check dates, tool versions, repo state) before using. Don't blindly reuse stale KB entries — a bad solution propagates indefinitely.
If `cerno` fails or returns no results, continue and note "No KB prior art found".

### 1.5. Scope checkpoint (lightweight, no blocking)

**If >30 min have passed since the task was stated and no code/delegation has started:** flag it. Say: "We've been exploring for [X] min — the primary deliverable is [Y]. Continue exploring or start building?" One sentence, not a lecture. This catches the byproduct trap (garden posts, research tangents, naming debates pulling focus from the build). Exploring is fine — but make it a conscious choice, not drift. Burned: spent 60+ min on garden posts, research gaps, and career reflection before writing a single line of docima code.

### 2. Choose weight class

**Effort switching (opusplan pattern):** Opus is always the session default — no model switching needed. For multi-file or architectural tasks, bump to max effort for the CE plan + weight-class step, then drop back to medium before delegation. Planning is where Opus's reasoning gap is real; execution goes to external delegates regardless of effort level.
```
/model → max effort   ← CE plan + weight-class decision
/model → medium       ← step 3 delegation (CC default)
```
Skip for trivial tasks (single file, clear spec). *Pattern sourced from Claude Code's `opusplan` alias; updated Mar 2026 when Opus became session default.*

Default to `/workflows:plan`. Use `EnterPlanMode` only as the exception.

**`--yolo` mode (personal tools, low blast radius):**
Skip plan review — go straight from CE plan to delegation. Valid when ALL of:
- Personal tool (not client/production code)
- Blast radius = only Terry (no shared repos, no external sends)
- Spec is clear (from prior brainstorm, consilium, or user description)
- No architecture decisions that need human judgment

CE plan still runs (catches codebase gotchas) — only the review/approval pause is skipped. Terry can invoke explicitly (`/strategos --yolo <task>`) or Claude can auto-detect when all conditions are met and announce: "Auto-yolo: personal tool, clear spec, low blast radius."

| Task size | Use |
|-----------|-----|
| **Trivial:** new skill file, config change, ≤20 lines of code, no existing code touched, zero cascading changes | **Build directly in-session** — skip CE plan and delegation. Hook enforced: Write/Edit to `~/code/` >20 lines is hard-blocked. |
| Single-file, ≤3 commands, no architecture decisions, requires live user decisions mid-plan | `EnterPlanMode` → delegate |
| **New project / fresh codebase** (blank repo, new crate, no existing code to research) | `superpowers:brainstorming` → `superpowers:writing-plans` → `superpowers:subagent-driven-development` — CE research agents find nothing on blank repos; skip them |
| **Spec already written** (brainstorm done, design doc exists, task is clear) | `plan-exec <spec-file> -p ~/code/<project>` — **zero Max20**. Fallback chain: Gemini → Codex → OpenCode. |
| Multi-command CLI, new architecture, existing codebase | **CE research → Superpowers plan → `plan-exec`** (see pipeline below). Max20 = brainstorm + plan only. Execution is free. |
| Same as above but genuinely needs vault context mid-execution | `/slfg <description>` — fully autonomous. Burns Max20 — use only when vault context can't be serialised into a prompt. |
| Unclear requirements | `/workflows:brainstorm` first |

**CE + Superpowers + External Execution (the full free pipeline):**

The integrated pipeline that maximises quality while minimising Max20 spend. CE and Superpowers handle judgment (research, planning, review); free tools handle implementation.

```
┌─ RESEARCH (cheap — Haiku/Sonnet subagents) ──────────────┐
│ CE: learnings-researcher + repo-research-analyst          │
│ → surfaces ~/docs/solutions/ gotchas + codebase patterns  │
│ → run in parallel, ~2min, catches institutional knowledge │
└──────────────────────────────────────────────────────────┘
          ↓ gotchas + patterns feed into plan
┌─ PLANNING (one Opus pass) ───────────────────────────────┐
│ superpowers:writing-plans                                 │
│ → converts research into structured TDD task steps        │
│ → file structure, test-first, exact commands              │
│ → identifies shared artifacts (Phase 1) vs independent    │
│   tasks (Phase 2)                                         │
└──────────────────────────────────────────────────────────┘
          ↓ plan decomposes into tasks
┌─ EXECUTION (FREE — external tools) ─────────────────────┐
│ Phase 1: Build shared artifacts sequentially, commit      │
│ Phase 2: Fan out to lucus worktrees + mixed tools         │
│   → Route by signal: Codex (multi-file/Rust),             │
│     Gemini (algorithmic), OpenCode (boilerplate)           │
│ Phase 3: Validate each on completion (deps, scope, tests) │
│ Phase 4: Merge passing branches                           │
└──────────────────────────────────────────────────────────┘
          ↓ merged code ready for review
┌─ REVIEW (cheap — Sonnet subagents) ─────────────────────┐
│ CE: pattern-recognition-specialist → spec compliance      │
│ CE: kieran-python/rust/ts-reviewer → code quality         │
│ CE: security-sentinel → if handles input/auth/secrets     │
│ CE: code-simplicity-reviewer → YAGNI check last           │
└──────────────────────────────────────────────────────────┘
```

**When to use:** Existing codebase with KB history + multi-task work. This is the **default pipeline for non-trivial builds**. The only Max20 spend is orchestration (reading outputs, routing decisions) + one planning pass.

**When NOT to use:** Fresh codebase (CE finds nothing), trivial single-file change, or tasks requiring live vault context that can't be serialised into a prompt.

**Superpowers writing-plans → external execution bridge:**
The plan from `writing-plans` produces per-task specs with exact file paths, test commands, and code. Each task spec becomes a self-contained delegate prompt:
1. Extract task from plan → write to `/tmp/<project>-task-N.txt`
2. Identify shared artifacts (types, interfaces, helpers) → build those first in Phase 1
3. Independent tasks → fan out as External Agent Teams (see below)

**Routing table for execution step:**
| Signal | Tool | Why |
|--------|------|-----|
| Rust | Codex `--sandbox danger-full-access` | Best dev tool, DNS for cargo |
| Multi-file, cross-imports | Codex | Repo navigation |
| Algorithmic, isolated logic | Gemini | AA index 57, free |
| Boilerplate, routine adapter | OpenCode | Free, unlimited |
| All three down | Sonnet subagent | Last resort, burns Max20 |

Reviews (spec compliance + code quality) always stay as Claude subagents — judgment work belongs on Max20.

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
| **Rust (any)** | **Codex `--sandbox danger-full-access`** | Default for Rust. Lifts DNS block, `cargo build` works, Terminal-Bench #1 for dev tasks. `codex exec --sandbox danger-full-access --full-auto "..."` |
| **Rust — Codex budget exhausted or code is sensitive** | **Gemini CLI** | Fallback. Runs locally, no code leaves machine. `cd ~/code/<project> && gemini -m gemini-3.1-pro-preview -p "..." --yolo` |
| Algorithmic, isolated logic, "write X that does Y" | **Gemini CLI** | AA index 57 (beats Opus 4.6 at 53), free. `gemini -m gemini-3.1-pro-preview -p "..." --yolo` |
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
# Codex — MUST cd into the target repo first (writes scoped to CWD even with --sandbox danger-full-access)
# Default: FOREGROUND (omit run_in_background) — keeps tmux tab active. Background only when doing parallel in-session work.
cd ~/code/<repo> && codex exec --skip-git-repo-check --full-auto "<prompt>"

# Gemini — MUST cd into the project repo first (Gemini locks workspace to CWD)
# Default to gemini-3.1-pro-preview (AA index 57, beats Opus 4.6)
cd ~/code/<project> && gemini -m gemini-3.1-pro-preview -p "<prompt>" --yolo

# OpenCode
OPENCODE_HOME=~/.opencode-lean opencode run \
  -m opencode/glm-5 \
  --title "<title>" \
  "<prompt>"
```
Use Bash tool's `run_in_background: true` — not shell `&`.
If chosen delegate command fails immediately, switch once to a backup tool based on task type; if backup fails, stop and report delegation blocked.

**Swarm mode (2+ independent tasks → parallel execution):**

**Default posture: always look for the parallel split.** When scoping a task, the first question is "what are the independent units?" not "how do I sequence this?" Parallel is free and async; sequential is a bottleneck. Only fall back to sequential when tasks genuinely depend on each other's output.

When the plan decomposes into N independent tasks, launch all at once — free, async, no Max20 cost.

**Parallelise across independence boundaries, not arbitrary splits.** More agents only helps when tasks don't need each other's output. Splitting coupled files across agents causes merge conflicts — one agent per dependency chain. Splitting tiny tasks (10-line config files) costs more to package than to write inline. The right decomposition is: different files + no shared output = different agents.

**Choose parallel execution method:**

| Method | When | Pros | Cons |
|--------|------|------|------|
| **External swarm** (lucus + Codex/Gemini/OpenCode) | Multi-file tasks, Rust, need sandbox/DNS | Free, best dev tools, full isolation | Manual decomposition, merge step |
| **Agent Teams** (TeamCreate) | In-session tasks, need vault/session context | Shares context, no merge, auto-parallel | Burns Max20, Claude-only (no Codex/Gemini) |

**Default: external swarm.** Use Agent Teams when tasks need vault context or cross-file reasoning that can't be captured in a standalone prompt.

#### External swarm pipeline

**Step 1 — Decompose.** For each task, capture:
```
name:        short-kebab-name
spec:        full self-contained prompt (include file paths, constraints, verification cmd)
lang:        rust | python | typescript | other
validation:  cargo build && cargo test | uv run pytest | pnpm test | <custom>
```

**Step 2 — Auto-route (no asking).** Route each task by signal (see tool table above). Report inline: "→ feature-a: Codex (Rust), feature-b: Gemini (new logic), feature-c: OpenCode (boilerplate)"

**Step 3 — Create worktrees + launch all in parallel:**
```bash
# Worktrees
lucus new <task-a-branch>
lucus new <task-b-branch>

# Launch all simultaneously (Bash tool run_in_background: true for each)
cd <worktree-a> && codex exec --sandbox danger-full-access --full-auto "<spec-a>"
cd <worktree-b> && gemini -m gemini-3.1-pro-preview -p "<spec-b>" --yolo
```

**Step 4 — Validate as each completes.** Don't wait for all — validate on notification:
```bash
cd <worktree-X> && <validation_cmd>
# Pass (exit 0): ✓, run git diff --stat
# Fail (exit ≠ 0): ✗, capture last 20 lines of error
```

**Step 5 — Summary + merge:**
```
Pipeline complete: N/M tasks passed
✓ feature-a   Codex    3 files   cargo test passed    2m14s
✗ feature-b   Gemini   —         build failed         3m02s
```
Merge passing branches (`lucus merge <branch>`). For failures: show error, propose retry with different delegate / fix in-session / skip. Wait for Terry's call. Don't auto-fix without input.

#### External Agent Teams (free swarm with coordination)

**The goal: Agent Teams coordination without Max20 cost.** Opus orchestrates in-session (the only cost), free tools execute in parallel worktrees. This is the default for all multi-task work.

**The pattern:**
```
Opus (orchestrator, in-session)
  ├── Phase 1: Build shared artifacts (sequential)
  │   └── Write shared code (embeddings.py, types, interfaces)
  │   └── Commit — worktrees only see committed history
  │
  ├── Phase 2: Fan out independent tasks (parallel)
  │   ├── lucus new task-a → Codex (multi-file)
  │   ├── lucus new task-b → Gemini (algorithmic)
  │   └── lucus new task-c → OpenCode (boilerplate)
  │
  ├── Phase 3: Validate as each completes
  │   ├── Check pyproject.toml for dep pollution
  │   ├── git diff --stat for scope creep
  │   └── Run tests
  │
  └── Phase 4: Merge passing branches, retry failures with different tool
```

**Fallback chain (when a tool fails, switch laterally — don't escalate to Max20):**
```
Gemini 429 (quota) → Codex or OpenCode
Codex sandbox block → Gemini (runs locally) or Sonnet subagent
OpenCode auth fail → Gemini or Codex
All three down → Sonnet subagent (last resort, burns Max20)
```

**Tool diversity rule:** Never launch 3+ delegates to the same provider simultaneously. Gemini free tier quota is shared — parallel Gemini calls burn through it in one burst. Mix tools: Gemini (algorithmic) + Codex (multi-file) + OpenCode (boilerplate).

**Key insight: coordination via files, not shared context.** Agent Teams' advantage is shared conversation context. External swarm replaces that with:
- Shared artifacts committed to repo (Phase 1)
- Self-contained spec files at `/tmp/` per task
- Orchestrator validates and connects outputs

This works for 90% of tasks. Reserve Agent Teams (TeamCreate) for the rare case where workers need live back-and-forth or vault context too large to paste into a prompt.

**Sequential dependent phases? Use Phase Contract pattern** (`~/docs/solutions/phase-contract-pattern.md`):
- Each phase runs as a fresh-context subagent → produces a file artifact + JSON summary
- Orchestrator validates JSON contract before launching next phase
- On `"status": "failed"` → stop and restart from that phase, not the beginning
- Complements swarm: use swarm for parallel independent tasks, phase contracts for sequential dependent tasks

**Max20 conservation principle:** Opus token spend should be brainstorm and judgment, not orchestration or implementation. Once a plan exists, hand off to `plan-exec` — zero Max20 from that point.

**`plan-exec` — zero-Max20 execution:**
```bash
# Single task with spec file (fallback: gemini → codex → opencode)
plan-exec /tmp/task-spec.txt -p ~/code/project

# Force a specific backend
plan-exec spec.txt -p ~/code/project -b codex

# Dry run
plan-exec spec.txt --dry-run

# For multi-task plans: write per-task specs, launch parallel
plan-exec /tmp/task-a.txt -p ~/code/project &
plan-exec /tmp/task-b.txt -p ~/code/project &
wait
```
Results: `~/.cache/plan-exec/<timestamp>/`. If all backends fail, escalate to Opus.

**The ideal Max20 budget for a build session:**
- Brainstorm/discuss with user → Max20 (irreplaceable)
- Write plan → Max20 (one Opus pass, or use Gemini for simple plans)
- Execute plan → `plan-exec` (FREE)
- Validate results → quick in-session check (minimal Max20)
- Review → CE agents as Sonnet subagents (cheap Max20)

**Everything between "plan written" and "review needed" should cost zero Max20.**

**Rules for all parallel execution:**
- **Commit the plan before `lucus new`** — worktrees only see committed history. Uncommitted plan files are invisible to delegates.
- Decompose the plan first — tasks must be truly independent (different files)
- One `lucus` worktree per delegate — never share a worktree
- Mix tools by task type: Codex for multi-file/repo nav, Gemini for algorithmic, OpenCode for boilerplate
- Review `git diff --stat` per branch before merging — Gemini touches extra files. **Specific pattern:** Gemini promotes optional dependencies to main `dependencies` in pyproject.toml/Cargo.toml when it sees imports in the file it's implementing. Always check dependency changes after Gemini delegates.
- **Gemini executes live mutations during testing** — if the CLI wraps a live service (calendar, WhatsApp, DB), expect real side effects during Gemini's verification pass. Brief with a test fixture or accept live side effects and clean up after.
- Merge conflicts = tasks weren't independent enough; phase them next time
- If any delegate branch fails, do not merge partial branches blindly; finish successful branches first, then re-scope failed task as a new single delegation.
- **Don't launch sequentially** — defeats the purpose of swarm mode
- **Rate limit fallback:** If a delegate returns 429 (Gemini capacity exhausted), switch tool laterally immediately (don't wait). Gemini → Codex or OpenCode. Don't launch all delegates simultaneously to the same provider — split across providers.
- **Codex can't write to lucus worktree paths** if `apply_patch` resolves to the main repo path. Workaround: use Sonnet subagent or Gemini (both respect CWD). See `delegation-reference.md`.
- **Post-delegate checklist (enforced by hook next session):** (1) `head -12 pyproject.toml` — dep pollution, (2) `git diff --stat` — scope creep, (3) run tests.

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

**CLI binary changes — always smoke test before closing.** After any `cargo build --release` or equivalent: run `<binary> --version` or a minimal real invocation to confirm the new binary works. Don't wait to be asked. Burned: swapped consilium council model, shipped and committed without testing until user prompted.

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

## Language Selection

**Default: Python for new tools.** Use Rust only when there's a specific reason (CPU-bound, startup speed, extending existing Rust tool). Capco/client work is always Python. Full heuristic: `~/docs/solutions/rust-vs-python-heuristic.md`.

## Defaults by Language

| Language | Default tool | Caveats |
|----------|-------------|---------|
| Rust | **Codex `--sandbox danger-full-access`** (default) / Gemini (fallback if budget low or code sensitive) | `--full-auto` alone keeps `workspace-write` sandbox which blocks DNS/cargo. `--sandbox danger-full-access` lifts all restrictions. Rust regex: no lookahead. |
| Python | Gemini or OpenCode | Use `uv` not pip. Single-file scripts: `uv run --script` shebang. |
| TypeScript | Codex or Gemini | pnpm, not npm. |
| Shell scripts | OpenCode | New `~/bin/` scripts must be Python (bash-guard). |

## Hard Rules

- **Prior discussion ≠ plan.** Consilium output, brainstorm notes, and design reviews are inputs to planning — not a substitute for it. Always run cerno + CE plan first.
- **Never write non-trivial code in-session** without proposing delegation first.
- **One task per delegation.** If there are 3 independent tasks, launch 3 separate delegates.
- **Don't inline full files.** Give paths, let delegates read.
- **Write tests for any non-trivial fix or feature.** At minimum: a test that would have caught the bug just fixed, plus any critical invariants (caps, bounds, parse contracts). Delegates don't write tests by default — add a dedicated test task in the delegation prompt or as a separate delegate. Don't ship without it.
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
- Codex write blocked ("Operation not permitted") → launched from wrong CWD; always `cd ~/code/<repo> && codex exec ...`
- Gemini no file changes → missing `--yolo`
- Double-backgrounded → never use `&` with `run_in_background: true`
- After Codex → always `git add && git commit` manually (sandbox blocks `.git`)

## Calls
- `cerno` — solutions KB check (step 1)
- `lucus` — for parallel worktree isolation
- `scrutor` — for post-implementation review
- `artifex` — for naming conventions
