---
name: oghma
description: oghma memory tool — search memories, check status, manage daemon. Use when user mentions oghma, memory search, or session memory.
---

# oghma

Rust CLI that watches AI coding session transcripts, extracts technical gotchas via LLM, stores in SQLite with FTS5 + vector search, and provides hybrid search. Replaces Python oghma (v0.6.3) with single binary, local fastembed-rs embeddings.

## Quick Reference

```bash
oghma search "rust cargo workspace"   # FTS5 keyword search (default)
oghma search "query" --mode vector    # vector search (requires embeddings)
oghma search "query" -n 5 -c gotcha   # limit + category filter
oghma add "content" -c gotcha         # manual memory insert
oghma status                          # DB path, memory count, daemon state
oghma stats                           # category + tool counts
oghma start                           # start daemon (background)
oghma start -f                        # start daemon (foreground, for debug)
oghma stop                            # stop daemon
oghma migrate-embeddings --dry-run    # check pending embeddings
oghma migrate-embeddings              # backfill embeddings for all memories
oghma init                            # create ~/.oghma/config.toml
```

## Key Paths

- **Binary:** `~/bin/oghma` (built from `~/code/oghma-rs/`)
- **Config:** `~/.oghma/config.toml` (TOML, backward-compat with Python oghma TOML)
- **DB:** `~/.oghma/oghma.db` (SQLite with FTS5 + sqlite-vec)
- **PID file:** `~/.oghma/oghma.pid`
- **Log:** `~/.oghma/oghma.log`
- **fastembed model cache:** `~/code/oghma-rs/.fastembed_cache/` (gitignored)
- **Repo:** `~/code/oghma-rs/`

## Architecture

```
file watcher → JSONL parsers → LLM extractor → fastembed embeddings → sqlite-vec dedup → SQLite store
```

- **Parsers:** Claude Code (`~/.claude/projects/-Users-*/*.jsonl`), Codex (`rollout-*.jsonl`), OpenCode (`ses_*`), OpenClaw
- **LLM routing:** `google/`, `anthropic/`, `meta-llama/`, `deepseek/`, `moonshotai/` → OpenRouter (`OPENROUTER_API_KEY`); else → OpenAI (`OPENAI_API_KEY`)
- **Embeddings:** fastembed-rs BGESmallENV15, 384-dim, local ONNX (no API key)
- **Dedup:** cosine similarity via sqlite-vec, threshold 0.92

## Config Fields (all have defaults — existing Python TOML works as-is)

```toml
[extraction]
model = "google/gemini-3-flash-preview"   # model for LLM extraction
skip_content_patterns = ["MEMORY.md", "write_memory", "edit_memory"]

[embedding]
batch_size = 100
rate_limit_delay = 0.1
max_retries = 3

[tools]
# All tools default to enabled with standard paths; cursor disabled by default
```

## Gotchas

- **`oghma search` returns nothing at startup** — binary may be old. Check `oghma --version`.
- **Config parse error `missing field`** — old Python TOML missing new Rust fields. Fields now have `#[serde(default)]` — re-init with `oghma init` only if still failing.
- **Daemon shows "running" but PID stale** — PID file exists from crashed session. `rm ~/.oghma/oghma.pid` then `oghma start`.
- **fastembed model download on first `migrate-embeddings`** — ~24MB, one-time download to `.fastembed_cache/`. Normal.
- **Cargo workspace binary path** — `~/code/target/release/oghma` (workspace root), NOT `~/code/oghma-rs/target/release/oghma`. But the oghma-rs crate is NOT part of the workspace (separate Cargo.toml at root), so it builds to `~/code/oghma-rs/target/release/oghma`.
- **Hook injection** — `~/.claude/hooks/oghma-session-inject.py` calls `oghma search` as subprocess, debounced 30min per cwd. Also injects `~/code/<project>/CONTEXT.md` if present.
- **Search is keyword-only until embeddings backfilled** — run `oghma migrate-embeddings` after daemon has run a while.

## Build / Deploy

```bash
cd ~/code/oghma-rs
cargo build --release
cp target/release/oghma ~/bin/oghma
```

## Phase Status

- **Phase 1** ✅ — search MVP (FTS5, status, stats, add, init)
- **Phase 2** ✅ — daemon + ingestion (parsers, extractor, embedder, watcher, start/stop, migrate-embeddings)
- **Phase 3** 🔜 — hybrid RRF search, MCP server (rmcp), migration tool from Python 1536-dim DB, crates.io publish
