# lacuna

Demo CLI for Meridian regulatory gap analysis. Wraps the Railway API with Rich output.

**Script:** `~/bin/lacuna` (uv run --script, no install needed)
**API:** `https://meridian-production-1bdb.up.railway.app` (no auth)

## Commands

```bash
lacuna docs                                          # list all documents
lacuna gap --circular hkma-cp --baseline demo-baseline           # run gap analysis
lacuna gap --circular hkma-cp --baseline demo-baseline --verbose # with reasoning + citations
lacuna query "What are HKMA's GenAI consumer protection requirements?" --jurisdiction hk
lacuna warmup                                        # pre-warm Railway cache before demo
```

## Doc Aliases

| Alias | Document |
|-------|----------|
| `hkma-cp` | HKMA GenAI Consumer Protection 2024 |
| `hkma-gai` | HKMA GenAI Financial Services 2024 |
| `hkma-sandbox` | HKMA GenAI Sandbox Arrangement 2024 |
| `hkma-spm` | HKMA SPM CA-G-1 Revised 2024 |
| `eu-ai-act` | EU AI Act (Regulation 2024/1689) |
| `fca` | FCA AI Update 2024 |
| `mas-consult` | MAS AI Risk Management Consultation 2025 |
| `mas-mrmf` | MAS AI Model Risk Management 2024 |
| `demo-baseline` | Meridian Demo Baseline (Capco-authored) |
| `nist-rmf` | NIST AI Risk Management Framework 1.0 |

Raw UUIDs also accepted anywhere an alias is used.

## Demo Day Checklist

1. `lacuna warmup` — do this before the meeting (cache resets on Railway restart)
2. Expected result for primary demo pair: **Full: 1 / Partial: 5 / Gap: 2**
3. If warmup takes >60s, Railway cold-started — run it twice

## Gotchas

- **`is_policy_baseline` is always `false`** — all docs are in doc_repo, not policy_repo. The script hardcodes this; don't change it.
- **Gap analysis timeout is 120s** — first run after Railway restart can take 30s+. Always warmup.
- **Cache is in-memory on Railway** — resets on every service restart. Re-run `lacuna warmup` if Railway was redeployed.
- **NIST and demo-baseline show jurisdiction "-"** — hardcoded in BASELINES set; they're not jurisdiction-specific.
- **Override API URL:** `LACUNA_API_URL=http://localhost:8000 lacuna docs` for local dev.

## Second Credibility Baseline

For the "I didn't write this doc" credibility test during demo:
```bash
lacuna gap --circular hkma-cp --baseline nist-rmf
```
NIST AI RMF was uploaded `no_llm=true` so findings will differ from the primary pair.

## Files

- Script: `~/bin/lacuna`
- Plan: `~/code/lacuna/docs/plans/2026-03-02-feat-lacuna-demo-cli-plan.md`
- Meridian project: `~/code/reg-atlas/`
- Meridian CLAUDE.md (doc IDs, deploy): `~/code/reg-atlas/CLAUDE.md`
- Demo script: `~/code/reg-atlas/DEMO_SCRIPT.md`
