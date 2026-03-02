# lacuna

Demo CLI for Lacuna regulatory gap analysis. Wraps the Railway API with Rich output.

**Script:** `~/bin/lacuna` (uv run --script, no install needed)
**API:** `https://meridian-production-1bdb.up.railway.app` (no auth)

## Commands

```bash
lacuna docs                                          # list all documents (12 docs)
lacuna preflight                                     # health check: API + docs + cache (use before demo)
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
| `demo-baseline` | Codex Argentum v1.0 (Capco-authored illustrative baseline) |
| `nist-rmf` | NIST AI Risk Management Framework 1.0 |
| `nist-iso42001` | NIST AI RMF → ISO 42001 Crosswalk |
| `sg-genai` | Singapore GenAI Governance Framework 2024 |

Raw UUIDs also accepted anywhere an alias is used.

## Demo Day Checklist

**Night before:**
1. `lacuna preflight` — full health check (API + all 12 docs + cache warmup in one command)
2. Expected: `PASS — demo ready.` with Full:1 Partial:5 Gap:2 (hkma-cp vs Codex Argentum v1.0)
3. Start a QuickTime screen recording as backup before the meeting

**Day of (before Tobin arrives):**
1. `lacuna preflight` again — cache resets on Railway restart
2. Have these queries ready to paste:
   - `What are HKMA's requirements for GenAI consumer protection?`
   - `What are the high-risk AI system requirements under the EU AI Act?`
3. Bring a 5G mobile hotspot — office wifi may block Railway/Railway egress

**If preflight shows FAIL:**
- API unreachable → check network, try `LACUNA_API_URL=http://localhost:8000 lacuna docs` for local fallback
- Missing docs → Railway restarted and volume still mounting; wait 60s and retry
- Cache warm failed → run `lacuna warmup` manually; first run can take 30s+

## Gotchas

- **`is_policy_baseline` is always `false`** — all docs are in doc_repo, not policy_repo. The script hardcodes this; don't change it.
- **Gap analysis timeout is 45s** — if Railway cold-started, first run can exceed this. Always warmup.
- **Cache is in-memory on Railway** — resets on every service restart. Re-run `lacuna warmup` (or `lacuna preflight`) if Railway was redeployed.
- **NIST, NIST crosswalk, and demo-baseline show jurisdiction "-"** — hardcoded in BASELINES set; they're not jurisdiction-specific.
- **sg-genai and nist-iso42001 uploaded no_llm** — chunks exist for RAG queries, but extracted requirements field is sparse. Don't demo gap analysis against these as baseline.
- **Override API URL:** `LACUNA_API_URL=http://localhost:8000 lacuna docs` for local dev.
- **uv resolves deps on first run** — if demo machine has never run it, first invocation hits PyPI (needs internet). Pre-warm by running any lacuna command once the day before.

## Second Credibility Baseline

For the "I didn't write this doc" credibility test during demo:
```bash
lacuna gap --circular hkma-cp --baseline nist-rmf
```
NIST AI RMF was uploaded `no_llm=true` so findings will differ from the primary pair.

## Files

- Script: `~/bin/lacuna`
- Plan: `~/code/lacuna/docs/plans/2026-03-02-feat-lacuna-demo-cli-plan.md`
- Lacuna project: `~/code/lacuna/`
- Lacuna CLAUDE.md (doc IDs, deploy): `~/code/lacuna/CLAUDE.md`
- Demo script: `~/code/lacuna/DEMO_SCRIPT.md`
- Vault: `~/notes/Capco/Lacuna/` (symlinks to CLAUDE.md, DEMO_SCRIPT.md, Codex Argentum)
