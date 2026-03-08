---
name: consilium
description: Multi-model deliberation — auto-routes by difficulty. Full council (~$0.50), quick parallel (~$0.10), red team (~$0.20), and more.
aliases: [ask-llms, council, ask llms]
github_url: https://github.com/terry-li-hm/consilium
user_invocable: true
cli_version: 0.5.1
cli_verified: 2026-03-03
runtime: rust
---

# Consilium

5 frontier models deliberate on a question, then Gemini judges and Claude critiques. Models see and respond to previous speakers, with a rotating challenger ensuring sustained disagreement. Auto-routes by difficulty.

> Source: `~/code/consilium/`. Site: [consilium.sh](https://consilium.sh). Extended reference: `~/skills/consilium/REFERENCE.md`.

---

## Modes

| Mode | Flag | Cost | Description |
|------|------|------|-------------|
| Auto (default) | *(none)* | varies | Opus classifies difficulty, picks quick or council |
| Quick | `--quick` | ~$0.10 | Parallel queries, no debate/judge |
| Council | `--council` | ~$0.50 | Full multi-round debate + judge |
| Deep | `--deep` | ~$0.90 | Council + auto-decompose + 2 debate rounds |
| Deep + xpol | `--deep --xpol` | ~$1.05 | Deepest — cross-pollination pass after debate |

**Other modes:** `--redteam` (~$0.20), `--premortem` (~$0.20), `--forecast` (~$0.25), `--oxford` (~$0.40), `--discuss` (~$0.30), `--socratic` (~$0.30), `--solo` (~$0.40)

---

## Routing

**Mental model:** `--quick` = breadth (surface perspectives), `--council` = convergence (stress-test a decision).

**Default bias: deep > council > quick.** Career, negotiation, strategy, real consequences → `--deep`. Reserve `--quick` for naming and pure brainstorming.

```
Single correct answer? → Web search or ask Claude directly
Personal preference / physical / visual? → Try it in person
Measurable outcome? → judex (run the experiment)
Need perspectives without debate? → --quick
Binary for/against? → --oxford
Stress-testing a plan? → --redteam
Assume failure, work backward? → --premortem
Probabilistic answer? → --forecast
Exploratory, still forming the question? → --discuss or --socratic
Everything else → --deep (default)
```

---

## When to Use / Not Use

**Use:** Genuine trade-offs, domain-specific decisions, strategy, stress-testing plans, probabilistic forecasting, code/security audit (`--redteam` with code pasted in).

**Skip:** Single correct answer, personal taste/physical (glasses, food), thinking out loud, already converged, speed matters (60-90s for full council).

---

## Prerequisites

```bash
# API key — already in ~/.zshenv, available in all shells including background
export OPENROUTER_API_KEY=$(security find-generic-password -s openrouter-api-key -a terry -w 2>/dev/null)

# Binary: ~/.local/bin/consilium → ~/code/consilium/target/release/consilium
# After code changes: cd ~/code/consilium && cargo build --release
```

---

## Running the Council

### Step 0: Suitability check

**consilium or judex?** If the outcome is measurable (build passes, benchmark faster, quality checkable) → `judex`. Deliberation is for decisions you can't measure.

Check the routing table above. If it falls in "Skip", redirect.

### Step 0.5: Propose mode

Tell the user which mode and why (one line), then confirm. Don't run until confirmed.

> "Strategic question with real consequences — I'd use **--deep --xpol**. Good?"

### Step 1: Gather context (for career/strategic decisions)

```bash
consilium "Should I accept this offer?" \
  --deep \
  --persona "Principal Consultant at Capco, ex-CNCBI Head of DS, HK market" \
  --domain banking \
  --vault
```

### Step 2: Run — always backgrounded, always `--vault`

```bash
# Standard invocation
consilium "question" --deep --vault

# With prompt file (avoids shell quoting issues for long prompts)
consilium --prompt-file /tmp/prompt.txt --deep --vault
```

**`--vault` is mandatory for:** any `--deep`, `--council`, or architecture/review run. Auto-saves to `~/notes/Councils/` with Obsidian Sync backup. Never use `--output /tmp/...` — `/tmp` doesn't survive reboot.

**For `--quick --quiet` batch/agent-test runs:** use `-o ~/docs/solutions/agent-tests/<name>.md` — skips Obsidian sync but survives session end. Pattern: `consilium --quick --quiet --domain banking -o ~/docs/solutions/agent-tests/proposal-architect.md "..."`

**`--quick` vs `--council` in background:** Running 4+ parallel `--council` sessions hits OpenRouter rate limits (20+ concurrent API calls). Use `--quick` for parallel batch runs; `--council` for single focused deliberations.

**Always `run_in_background: true`** on the Bash tool. Watch live: `consilium --watch` or `--tui` in another tmux tab.

**Retrieving output:** TaskOutput times out at 120s — consilium `--quick` takes ~150s, `--council` longer. Always redirect to `~/tmp/` and read with `cat`:
```bash
consilium "..." --quick > ~/tmp/consi-<name>.txt 2>&1
# then after task completes:
cat ~/tmp/consi-<name>.txt
```
Never use TaskOutput alone to retrieve consilium results — it will timeout and the output file in `/private/tmp` will vanish. `~/tmp/` survives the session.

**Don't retry if seemingly stuck.** One background job per query. If TaskOutput times out, just `cat ~/tmp/consi-<name>.txt` — the job is likely still running or already done.

### Step 3: Parse and present

After completion:
1. Read `[DECISION]` line as quick signal
2. Read vault file in `~/notes/Councils/`
3. Synthesize: decision + key reasoning + dissents + cost
4. **Never dump raw transcript into context**

If `--vault` was used but file is missing in `~/notes/Councils/`, treat run as partial.

---

## Common Flags

```bash
--persona "context"     # Personal context injected into prompts
--domain banking        # Regulatory context (banking|healthcare|eu|fintech|bio)
--context "hint"        # Context hint for the judge
--challenger gemini     # Assign contrarian role (council mode only)
--decompose             # Break complex question into sub-questions first
--rounds 3              # Rounds for --discuss or --socratic
--followup              # Interactive drill-down after judge (council only)
--effort high           # Reasoning effort: low|medium|high
--format json           # Machine-parseable output (council + quick only)
--share                 # Upload to secret Gist
--thorough              # Skip consensus early exit + context compression
--no-save               # Don't auto-save to ~/.consilium/sessions/
```

---

## Session Management

```bash
consilium --sessions              # List recent sessions
consilium --stats                 # Cost breakdown
consilium --watch                 # Live tail (rich formatted)
consilium --tui                   # TUI with phase/cost/time
consilium --view "career"         # View session matching term
consilium --search "career"       # Search all session content
consilium --doctor                # Check API keys and connectivity
```

---

## Known Issues

- **`--vault` is mandatory for background/overnight runs.** Never `/tmp` — wiped on reboot. `--vault` → `~/notes/Councils/` with Obsidian Sync.
- **OPENROUTER_API_KEY in background shells** — fixed: key in `~/.zshenv`. No inline fetch needed.
- **Binary can go stale after code changes.** `cd ~/code/consilium && cargo build --release`
- **Model timeouts** (historically DeepSeek/GLM) — partial outputs add noise but council still works.
- **`--format json` only works with council and quick modes.** Other modes output prose only.
- **`--challenger` and `--followup` are council-only.**
- **GPT-5.4-Pro (Responses API) is slow for `--council`.** Takes 67-120s+ per call with structured prompts — times out in blind (90s cap) and debate (120s cap). Council completes with 3/5 models in ~7-9 min. For faster runs: `CONSILIUM_MODEL_M1="google/gemini-2.5-flash" consilium --council "..."`. Full diagnosis: `~/docs/solutions/gpt-5.4-pro-responses-api-latency.md`.
- **402 = OpenRouter out of credits.** Tell Terry to top up at openrouter.ai/credits. Do not retry or proceed.
- **403 on a new model = access restricted (allowlist-gated).** Test before upgrading: `consilium --quick --quiet "test" 2>&1 | grep -i "403\|error"`. Swap to an available model or remove from rotation.

---

## Reference

Extended docs in `~/skills/consilium/REFERENCE.md`:
- Prompting tips (drafts, social, architecture, philosophical, domain-specific)
- Model tendencies table
- Flag compatibility matrix
- Follow-up workflow + vault template
- Cost & ROI
- Key lessons
- Research foundations (Surowiecki, Tetlock, Nemeth, CIA ACH)
- Recent features changelog

---

## See Also

- Repository: https://github.com/terry-li-hm/consilium
- Related: `/judex` (measurable outcomes), `/ask-llms` (alias)
- Lessons: `[[Frontier Council Lessons]]`
- Research: `~/docs/solutions/multi-llm-deliberation-research.md`
