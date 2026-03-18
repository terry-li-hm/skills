---
name: probatio
description: "Verification heuristics for deployed systems — the gap between 'function works' and 'system works as deployed.' Reference skill consulted after fixing bugs in cron jobs, CLIs, services, or any code that runs via an automated path. Not user-invocable."
user_invocable: false
disable-model-invocation: true
---

# Probatio — Deployed System Verification

> *Probatio: Latin "proof, testing" — the demonstration that something works in the field, not just in theory.*

Reference heuristics for verifying fixes to systems that run via cron, CLI, services, or any path other than direct function calls. Consult after fixing bugs in deployed pipelines.

## The Core Gap

AI agents (and hurried engineers) fix the function, test the function, and declare victory. But the deployed system calls the function through layers — CLI parser, pipeline orchestrator, environment setup — that can shadow, override, or bypass the fix. **The minimum valid verification runs the exact command production runs.**

## Failure Modes

| # | Mode | What happens | Example |
|---|------|-------------|---------|
| 1 | **Parameter shadowing** | Function default is fixed, but every real caller passes the parameter explicitly | `gather_daily(today=date.today())` overrides the default `-1 day` fix |
| 2 | **Environment divergence** | Fix works in interactive shell; cron has stripped env (no PATH, no .zshenv vars) | LaunchAgent can't find `uv` or API keys |
| 3 | **Stale cache** | Source file is fixed but `.pyc`/wheel/venv caches serve old code | `uv run` uses cached install, not edited source |
| 4 | **Idempotency guard** | Fix works on first run; second run is blocked by "already exists" check | Theoria skips if `Daily/YYYY-MM-DD.md` exists |
| 5 | **Timing-dependent state** | Manual test runs when upstream data is fresh; cron runs before upstream has fired | Theoria at 3am, lustro at 6:30pm |
| 6 | **Error swallowing** | Function fails but CLI catches broadly and exits 0; cron log shows "complete" | `except Exception: sys.exit(0)` |
| 7 | **Path indirection** | Edit source file, but binary resolves through symlink or installed package | Editing `~/code/foo/` but `~/.local/bin/foo` is a stale install |

## The Five-Question Checklist

After fixing any code that runs via an automated path:

1. **What command does production run?** Find the plist / crontab / systemd unit. Copy the exact invocation.
2. **Run that exact command.** Not the function. Not a simplified version. The actual command with the actual flags.
3. **Check the artifact, not the exit code.** Does the output file exist? Non-empty? Contains the expected date's data? Exit code 0 means nothing if the output is wrong.
4. **What ran before this?** If the system depends on upstream data, verify the upstream state matches what the cron would see at its scheduled time.
5. **Run it twice.** Does the idempotency guard block the second run? Is that correct?

## Key Distinction

| What you tested | What you should have tested |
|---|---|
| Function return value | Output file on disk |
| Default parameter path | Explicit parameter path from caller |
| Interactive shell environment | Cron / LaunchAgent environment |
| First run | Second run (idempotency) |
| Current source file | Installed / cached code |
| Exit code | Actual produced artifact |

## When to Consult

- After fixing any bug in code that runs via LaunchAgent, cron, systemd, or CI
- After delegate-built fixes to pipeline code (delegates test functions, not systems)
- Before claiming a cron fix is "done" in `/wrap`

## Epistemics

The checklist is a **Bayesian prior** about what fails (see `topica`). Each time you run it and a mode fires (or doesn't), update your mental weighting. Parameter shadowing and timing-dependent state are the highest-frequency modes — but that's based on N=2. Accumulate evidence.

## Provenance

Extracted Mar 2026 from theoria/lustro pipeline debugging. Parameter shadowing (mode 1) and timing-dependent state (mode 5) both burned us — fix applied to wrong layer, tested via wrong path, failed silently for 4+ days.
