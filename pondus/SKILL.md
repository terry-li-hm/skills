---
name: pondus
description: "AI model benchmark aggregator CLI. Use when comparing models, checking benchmark scores, or looking up leaderboard rankings."
user_invocable: false
---

# Pondus

Opinionated AI model benchmark aggregator. Rust CLI, open-source.

- **Repo:** `~/code/pondus` | [GitHub](https://github.com/terry-li-hm/pondus) | [crates.io](https://crates.io/crates/pondus)
- **Version:** 0.6.0 (Mar 2026)
- **Install:** `cargo install pondus`

## Architecture

```
src/
├── main.rs          # CLI (clap derive): sources, compare, list subcommands
├── models.rs        # Core types: ModelScore, SourceResult, MetricValue, SourceStatus
├── alias.rs         # Model name → canonical alias resolution (exact + prefix matching)
├── cache.rs         # JSON file cache in dirs::cache_dir()/pondus/ (macOS: ~/Library/Caches/pondus/)
├── config.rs        # Config from ~/.config/pondus/config.toml
├── output.rs        # Table/JSON/YAML output formatting
└── sources/
    ├── mod.rs       # Source trait + registry
    ├── aa.rs        # Artificial Analysis (REST API primary, scrape fallback)
    ├── arena.rs     # LMSYS Arena (agent-browser scrape, JSON fallback)
    ├── seal.rs      # Scale SEAL (agent-browser scrape)
    ├── swebench.rs  # SWE-bench (GitHub JSON API)
    ├── swebench_r.rs # SWE-rebench (agent-browser scrape)
    ├── aider.rs     # Aider polyglot (raw YAML from GitHub)
    ├── livebench.rs # LiveBench (HuggingFace datasets-server API)
    ├── tbench.rs    # Terminal-Bench (agent-browser scrape)
    └── mock.rs      # Test mock source
```

## Source Trait Pattern

Every source implements `Source`:
```rust
pub trait Source {
    fn name(&self) -> &str;
    fn fetch(&self, config: &Config, cache: &Cache) -> Result<SourceResult>;
}
```

`SourceResult` contains `Vec<ModelScore>` where each score has:
- `model`: normalized lowercase name (for alias matching)
- `source_model_name`: original name from source
- `metrics`: `HashMap<String, MetricValue>` (source-specific keys)
- `rank`: optional ordering

## Key Patterns

### AA uses REST API (v0.5.0+)
Primary: `GET https://artificialanalysis.ai/api/v2/data/llms/models` with `x-api-key` header.
Returns 394 models (vs 76 from scrape) including older/superseded models.
API key: `[artificial-analysis] api_key` in config.toml, or `AA_API_KEY` env var.
Falls back to agent-browser scrape if no key configured.
Response parsed via typed structs (`AaApiResponse` → `AaApiModel` → `AaApiEvaluations`).
Free tier: 1000 req/day.

### Scrape sources use agent-browser accessibility snapshots
Four sources scrape via `agent-browser snapshot` which returns an accessibility tree, not HTML.
Parse structured elements (`- row "..."`, `- cell "..."`, `- link "..."`) not flat text.

**Cell parser pattern** (used in Arena, SWE-rebench):
```rust
// Collect cells from row, extract values by position
if trimmed.starts_with("- cell \"") {
    if let Some(val) = extract_cell_value(cell_line) {
        cells.push(val);
    }
}
```

**Forward parser pattern** (used in SEAL):
Finds ±score anchors first, then walks backwards to find rank + model name.

### Alias resolution
`alias.rs` maps source model names → canonical names in two phases:
1. **Exact match** from `aliases.toml` lookup table
2. **Prefix match** fallback: `source_name.starts_with(alias)` with longest-match-wins, matching at `-`, `(`, or space boundaries (not `.` to avoid gpt-5 matching gpt-5.2). Space added in v0.5.0 for AA API names like `"Claude Opus 4.5 (Reasoning)"`.

### Cache
JSON files in `~/Library/Caches/pondus/` (macOS). TTL-based. Each source caches its parsed data.
**Clear a source cache:** `rm ~/Library/Caches/pondus/<source>.json`

## Source-Specific Gotchas

| Source | Gotcha |
|---|---|
| **AA** | API primary (394 models), scrape fallback (76 models). API key in config or `AA_API_KEY` env. API model names have parenthesized suffixes like `"(Reasoning)"` — prefix match resolves them. Scrape: intelligence index is cell[3]. |
| **Arena** | Multiple leaderboard tables (Text, Vision, Image Gen, Video Gen). Image/video models filtered by keyword. First table detected by `- row "1 "`. Claude Sonnet 4.6 outranks Opus on Arena (creative writing bias). |
| **SEAL** | Benchmark cards use `±` in score values. Model names may have trailing `*` (footnotes) — stripped. Scores averaged across benchmarks per model. |
| **SWE-bench** | Tests agent+model scaffolds, not raw models. Deduplicates by keeping highest `resolved_rate` per `source_model_name`. 367→301 after dedup. |
| **SWE-rebench** | Tests raw model performance. Same model scores 20-30pts lower than SWE-bench (no agent scaffold). |
| **LiveBench** | HuggingFace datasets-server API, batch limit 100 (not 1000). Dataset frozen since April 2025 — effectively dead. |
| **Aider** | Raw YAML from GitHub. Cost metric has legitimate zeros (free models) and extreme max (o1 at $186). |
| **Terminal-Bench** | `AGENT / Model` format breaks alias matching. Only 8 entries. |

## Build Gotchas

- **Stale binary:** `cargo build`/`cargo run` may say "Finished" without recompiling. Fix: `cargo clean -p pondus` then build.
- **Cargo.lock:** Must be committed before `cargo publish` (rejects dirty working dir).
- **Cache location:** `dirs::cache_dir()` on macOS = `~/Library/Caches`, not `~/.cache`.
- **PyPI publish:** `uv run --with build python3 -m build && uvx twine upload dist/*` (uv doesn't read ~/.pypirc).

## Publishing Checklist

1. Bump version in both `Cargo.toml` and `pyproject.toml`
2. `git add Cargo.toml pyproject.toml Cargo.lock && git commit`
3. `cargo publish`
4. `rm -rf dist/ && uv run --with build python3 -m build && uvx twine upload dist/*`
5. `git push`

## Data Quality

Audit script at `/tmp/pondus_audit.py` (not committed). Checks:
1. Score sanity (zeros, negatives, extreme outliers)
2. Arena ELO range
3. Source freshness (which models present)
4. Cross-source consistency (SWE-bench vs SWE-rebench deltas)
5. LiveBench value assessment

Analysis note: `~/notes/Pondus - Benchmark Analysis Feb 2026.md`

## Delegation Pattern

AA API integration was delegated to Codex (GPT-5.3-codex) — good fit for agentic repo-navigation tasks.
Codex wrote the typed structs, config wiring, and fetch logic. Claude fixed the prefix match boundary char (space) that Codex couldn't test without the live API.
Lesson: delegate the implementation, review the integration points.

## Aggregate Reliability Notes (Mar 2026)

Audited via `pondus check <model> --show-matches`. Findings:
- **TOML keys with dots** (`[kimi-k2.5]`) are parsed as nested keys by TOML. Must quote: `["kimi-k2.5"]`.
- **`cargo build --release` ≠ `cargo install --path .`** — build updates `target/release/` but not the installed binary in `~/.cargo/bin/`. Always install after build to avoid stale binary confusion.
- **Kimi K2.5** only has 1 reasoning source (AA). Mainly a coding model (swebench, swe-rebench). Using it in a reasoning-focused council (consilium) is thinly validated — preference over DeepSeek R1 is on lab diversity grounds, not reasoning benchmark depth.
- **GLM-5** has 2 reasoning sources (AA + Arena) and 4 total — best-validated Chinese model in the aggregate as of Mar 2026.
- **`--tag reasoning` sources**: AA, Arena, LiveBench, Seal. LiveBench frozen since Apr 2025 — effectively stale.

## Council Composition Rationale (consilium, Mar 2026)

Swapped DeepSeek R1 → Kimi K2.5 based on:
- R1 (Jan 2025) unranked on AA, weakest on Aider vs Kimi
- `pondus rank --aggregate --tag reasoning` confirms: GLM-5 rank 3 (0.818, 2 sources), Kimi K2.5 rank 1 on AA (0.972) but only 1 reasoning source
- Lab diversity: Moonshot (Kimi) + Zhipu (GLM) + xAI (Grok) + Anthropic (judge) = 4 distinct orgs
- Current council: GPT-5.2-pro, Gemini-3.1-pro-preview, Grok-4, Kimi-K2.5, GLM-5

## Future Work (low priority)

- Terminal-Bench: strip `AGENT /` prefix for alias matching
- LiveBench: deprecate or flag as stale
- `--time-decay` weighting for older benchmark results
