---
name: quaero
description: Exa search API CLI — neural/semantic web search, find-similar, content extraction, AI answers. Use when WebSearch is too shallow or noesis is overkill. quaero search "topic", quaero answer "question", quaero similar <url>.
---

# quaero

Rust CLI wrapper for the [Exa search API](https://exa.ai). Neural/semantic search that understands meaning, not just keywords.

## When to Use

| Signal | Use |
|--------|-----|
| Keyword search sufficient | WebSearch (free) |
| Need cited, quality sources | `noesis search` (~$0.006) |
| **Need semantic/neural search** | `quaero search --search-type neural` |
| **Find pages like this URL** | `quaero similar <url>` |
| **Quick AI answer with citations** | `quaero answer "question"` |
| **Extract full content of a page** | `quaero contents <url>` |

## Commands

```bash
# Search (default: neural)
quaero search "AI governance frameworks Hong Kong" --n 10
quaero search "rust async tokio" --search-type fast
quaero search "topic" --json  # raw API response

# Find similar pages
quaero similar https://example.com/article

# Extract full content of a URL
quaero contents https://example.com/article

# AI answer with citations
quaero answer "What is the HKMA's stance on AI in banking?"
```

## Setup

API key: `EXA_API_KEY` — stored in 1Password vault `Agents`, item `Agent Environment`.
Injected automatically via `~/.zshenv.tpl` → no manual setup needed.

## Source

- Binary: `~/bin/quaero`
- Source: `~/code/quaero/`
- Search type default: `neural` (semantic embedding-based)

## Gotchas

- `quaero` is a workspace member of `~/code/Cargo.toml` — build with `--target-dir target` to avoid sandbox issues
- `reqwest` uses blocking client — not async, but fine for CLI use
- `search_type` enum values: `auto`, `neural`, `fast`, `deep`
