---
name: judex
description: Empirical tool validation by running two AI coding tools in parallel on the same task. Use when benchmark-based routing is uncertain or contradicted by experience. Updates routing heuristics with real evidence.
user_invocable: false
---

# judex — Empirical Tool Validation

Not user-invocable. Internal guidance consulted when routing uncertainty can't be resolved from benchmarks.

**When to invoke:** You would have reached for `AskUserQuestion` to clarify which tool to use, OR the benchmark recommendation feels wrong given the specific task/language/constraints.

## The Pattern

Instead of arguing from benchmarks, run both and compare.

```
1. Create two lucus worktrees (prevents git add -A conflicts)
2. Write an identical prompt to /tmp/<task>-<tool-a>-prompt.txt and /tmp/<task>-<tool-b>-prompt.txt
3. Launch both in parallel (Bash run_in_background: true)
4. Wait for completion
5. Check: build + test + clippy (or equivalent verification)
6. Diff scope: git diff --stat per branch
7. Pick the winner. Document why. Update routing notes below.
```

## Case 1 — Codex vs Gemini: consilium Feature A (2026-03-04)

**Task:** Rust feature across 4 files — JUDGE_MODEL swap, new anthropic branch in query_model_with_fallback(), model-aware query_judge(), main.rs key threading.

**Prompt:** identical spec, same verification requirement (`cargo build && cargo test && cargo clippy`).

**Codex result:** ❌ Build failed. `~/code/Cargo.toml` workspace picked up the `consilium.*` lucus worktree name. Codex cannot run `cargo build` in its sandbox (DNS blocked) so it never discovered the conflict. Also missed threading `anthropic_api_key` from `main.rs` (prompt said "src/modes/*.rs" only). Error detection used `!response.starts_with('[')` instead of spec'd `is_error_response()`.

**Gemini result:** ✅ Build passed (1m08s), 3/3 tests, clippy clean. Fixed workspace conflict itself by adding `[workspace]` to Cargo.toml. Threaded `anthropic_api_key` through `main.rs → all modes`. Used `is_error_response()`. Touched 13 files (Codex: 11) — the 2 extras were `Cargo.toml` + `main.rs`, both required.

**Root causes of Codex failure:**
| Gap | Cause | Fixable with better prompt? |
|-----|-------|-----------------------------|
| Workspace conflict | Codex sandbox blocks `cargo build` (DNS) — can't discover compile errors | ❌ No — structural limitation |
| Missing main.rs threading | Prompt said "src/modes/*.rs" only, didn't mention `src/main.rs` | ✅ Yes |
| Error pattern | Ignored explicit `is_error_response()` instruction | Maybe |

**Winner: Gemini.** Structural advantage: runs on your machine, discovers compile errors, can self-correct.

**Routing update from this case:**
- For Rust tasks where `cargo build` validation is required: prefer Gemini (runs natively, discovers compile errors)
- If using Codex for Rust: explicitly include `src/main.rs` in the caller list, and add `[workspace]` to the package Cargo.toml before launching
- Keep the `is_error_response()` instruction bolded or in a MUST-use section

## Permanent Fixes Discovered

- **`[workspace]` in consilium `Cargo.toml`**: Prevents all future lucus worktree build conflicts. Now merged to main.
- **Prompt gap**: "search all call sites in src/modes/*.rs" misses main.rs. Template fix: "search ALL callers including src/main.rs and src/modes/*.rs"

## Routing Heuristics (Updated)

| Signal | Prefer | Avoid | Reason |
|--------|--------|-------|--------|
| Rust feature requiring `cargo build` | **Gemini** | Codex | Gemini runs on machine, catches compile errors. Codex sandbox blocks cargo. |
| Multi-file repo nav + test loops | **Codex** | Gemini | Codex is Terminal-Bench #1. Gemini touches extra files. |
| Isolated algorithmic logic | **Gemini** | — | LiveCodeBench #1. No compile-time validation needed. |
| Bulk boilerplate, routine edits | **OpenCode** | — | Free, unlimited. |
| Anything that's failed 3+ times | **Opus in-session** | — | Escalation only. |

## When to Run a judex Experiment

- Benchmark says X but recent experience contradicts it
- Task type falls in the gap between tools (e.g., "Rust feature" = Codex benchmark signal vs Gemini build validation signal)
- You've been burned by the routing before on a similar task

## Experiment Template

```bash
# 1. Write prompt to files (avoid shell quoting issues with special chars)
cat > /tmp/<task>-codex-prompt.txt << 'EOF'
<prompt>
EOF

cat > /tmp/<task>-gemini-prompt.txt << 'EOF'
<prompt>
EOF

# 2. Create worktrees
lucus new <task>-codex
lucus new <task>-gemini

# 3. Launch in parallel (run_in_background: true)
cd ~/code/<repo>.<task>-codex && codex exec --skip-git-repo-check --full-auto "$(cat /tmp/<task>-codex-prompt.txt)"
cd ~/code/<repo>.<task>-gemini && gemini -p "$(cat /tmp/<task>-gemini-prompt.txt)" --yolo

# 4. Verify each
cd ~/code/<repo>.<task>-codex && cargo build --release && cargo test && cargo clippy
cd ~/code/<repo>.<task>-gemini && cargo build --release && cargo test && cargo clippy

# 5. Diff scope
cd ~/code/<repo>.<task>-codex && git diff --stat
cd ~/code/<repo>.<task>-gemini && git diff --stat

# 6. Pick winner, commit, merge to main
cd ~/code/<repo>.<task>-gemini && git add -A && git commit -m "feat: ..."
cd ~/code/<repo> && git merge <task>-gemini
```

## Naming

*Judex* — Latin, "judge/arbiter" (from *jus*, law/right + *dicare*, to declare/proclaim). The arbiter between two tool choices based on real evidence, not speculation. Named by consilium quick mode (2026-03-04). Free on crates.io. Crux (Claude's pick) was taken; Judex was the clean alternative.
