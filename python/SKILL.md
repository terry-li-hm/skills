---
name: python
description: "Python development — new script/package scaffold, uv workflow, PyPI publish checklist. Use when starting or publishing Python work."
user_invocable: true
---

# Python

Three modes: **new** (scaffold), **dev** (daily workflow), **publish** (PyPI checklist). Pick the one that matches where you are.

## Triggers

- `/python new <name>` — scaffold a new script or package
- `/python dev` — daily workflow reminders
- `/python publish` — PyPI publish checklist
- `/python` with no args — ask which mode

---

## Mode: New

### What are you building?

| Type | Use when |
|------|----------|
| **Single-file script** | Personal automation, LaunchAgent, one-off CLI |
| **Package** | Publishing to PyPI, multi-file, reusable library |

---

### Single-file script

Shebang for all standalone scripts:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx",
#   "rich",
# ]
# ///
```

- **`.zshenv` not `.zshrc`** for env vars (sourced in non-interactive shells)
- **LaunchAgent scripts must use `uv run --script`** — never `.venv/bin/python` (breaks on uv upgrades). Must include `--python 3.13`.
- **`PYTHONUNBUFFERED=1`** in plist environment for log visibility under `nohup`
- **Symlinked scripts:** use `Path(__file__).resolve().parent` to get real directory, not symlink location

---

### Package (PyPI / multi-file)

```bash
uv init <name>          # creates pyproject.toml, src layout
cd <name>
uv add httpx rich       # add deps
```

**pyproject.toml essentials:**

```toml
[project]
name = "<name>"
version = "0.1.0"
description = "<one line>"
requires-python = ">=3.13"
license = { text = "MIT" }

[project.scripts]
<name> = "<name>:main"   # CLI entry point

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Name via consilium (mandatory):**

```bash
consilium "Name a new Python CLI tool that does X. Latin or Greek preferred. Check PyPI availability." --quick
```

Check PyPI availability: `pip index versions <name>` or search pypi.org. Name collision = full rename cost.

---

## Mode: Dev

### Commands

```bash
uv run <script.py>            # run with inline deps resolved
uv add <package>              # add dep (updates pyproject.toml + lockfile)
uv remove <package>           # remove dep
uv upgrade                    # upgrade all deps
uv sync                       # sync venv to lockfile
ruff check .                  # lint
ruff check . --fix            # auto-fix
ruff format .                 # format
```

### Testing

```bash
uv run pytest                 # run tests
uv run pytest -x              # stop on first failure
uv run pytest --tb=short      # concise tracebacks (prefer over default)
```

### Tool install

```bash
uv tool install <name>               # install CLI tool globally
uv tool install --reinstall <name>   # update (--reinstall enforced by hook)
```

**`uv tool install --force` is hook-blocked** — must use `--reinstall`.

### Agent-native design

If the script will be called by agents (not just humans):

```python
import sys

is_tty = sys.stdout.isatty()

if is_tty:
    # Pretty output: colours, progress bars, tables (rich)
else:
    # Plain output: newline-delimited, no ANSI, machine-parseable
```

TTY = human signal. Non-TTY = agent consumer. Design for both.

---

## Mode: Publish (PyPI)

### Pre-publish checklist

```bash
ruff check .                  # zero lint errors
ruff format --check .         # formatting clean
uv run pytest                 # tests pass
uv build                      # builds dist/ — check for errors
```

### Publish

```bash
uvx twine upload dist/*       # NOT uv publish — it doesn't read ~/.pypirc
```

**`uv publish` doesn't read `~/.pypirc`** — always use `uvx twine upload dist/*`.

### After publish

```bash
pip install <name>            # verify clean install from PyPI
uv tool install <name>        # verify CLI entry point works
```

Bump version in `pyproject.toml` before publishing. `uv` doesn't have a `cargo-release` equivalent — bump manually or use `bump2version`.

---

## Gotchas

- **`uv publish` ignores `~/.pypirc`** — use `uvx twine upload dist/*`
- **`uv tool install --force` hook-blocked** — use `--reinstall`
- **LaunchAgent + uv** — use `uv run --script` with `--python 3.13`; never `.venv/bin/python`
- **`.zshenv` not `.zshrc`** — env vars for non-interactive shells (cron, LaunchAgent, agent shells)
- **`PYTHONUNBUFFERED=1`** — required for `nohup` log visibility
- **Symlinked scripts** — `Path(__file__).resolve().parent` for actual directory
- **Package manager** — always `uv`, never `pip install` directly into global env. pnpm for Node.
- **Credential access in agent shells** — keychain locked in separate security session. Use `_keychain("service-name")` helper; `security` commands don't inherit unlocks from tmux

## Rust vs Python: when to use which

- **Rust:** CLI tools others install, performance-critical, single binary distribution, crates.io
- **Python:** Prototyping, AI/ML (PyTorch/numpy), glue code, LaunchAgents, anything uv-heavy
- **Key insight:** "Python is faster to write" is irrelevant when Claude writes it. Optimise for the end product.
