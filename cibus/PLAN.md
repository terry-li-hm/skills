# Cibus Implementation Plan

## Phase 0: WAF Reconnaissance (prerequisite, ~30 min)

Empirical tests to determine the cheapest reliable fetch path before writing any code.

### 0a. Test `porta run` on OpenRice

```bash
porta run --domain openrice.com --selector main \
  "https://www.openrice.com/en/hongkong/r-dan-ryans-chicago-grill-cityplaza-american-r12345"
```

**Expected outcomes:**
- **Works** → porta becomes primary fetch path (free, no Firecrawl credits). Skip phase 2.
- **Returns challenge page** → PoW token is per-session, not cookie-based. Proceed to 0b.

### 0b. Probe OpenRice hidden APIs

```bash
# Fetch the SPA shell (curl gets through to the HTML, just not past the JS challenge)
curl -sL "https://www.openrice.com/en/hongkong" -o /tmp/openrice-shell.html

# Find JS bundle URLs
grep -oP 'src="[^"]*\.js[^"]*"' /tmp/openrice-shell.html

# For each JS bundle, grep for API endpoints
curl -s "<bundle-url>" | grep -oP '"(/api/[^"]+)"'
curl -s "<bundle-url>" | grep -oP 'fetch\([^)]+\)'

# Test any discovered endpoints
curl -s "https://www.openrice.com/api/<discovered-route>?district=..." | head -50
```

**Expected outcomes:**
- **JSON API found & unprotected** → build cibus around direct API calls. Cheapest path.
- **API found but auth-gated** → try porta cookie injection on the API endpoint.
- **No API / all gated** → peruro remains the only path. Proceed with credit-based approach.

### 0c. Decision gate

| porta works | API found | Strategy |
|-------------|-----------|----------|
| ✓ | — | porta run (free) |
| ✗ | ✓ unprotected | curl API directly (free) |
| ✗ | ✓ auth-gated | porta inject → curl API (free) |
| ✗ | ✗ | peruro (1 credit/page) — current confirmed path |

Record results in `~/officina/docs/solutions/cloudflare-bypass-tools.md` (append
OpenRice porta/API test results).

---

## Phase 1: Skill-Only (no CLI, ~15 min)

The SKILL.md is the implementation. No CLI binary needed for v1 — the skill
orchestrates existing tools (`exauro`, `noesis`, `peruro`, `porta`).

### 1a. Validate the skill works end-to-end

Run `/cibus italian near central, 4 people, corkage friendly` manually in a Claude
Code session and verify:
- Health context pulled from NOW.md
- exauro finds relevant OpenRice URLs
- peruro (or porta, per phase 0 result) fetches listing data
- Output matches the template in SKILL.md

### 1b. Tune the prompt flow

Based on the manual run, adjust:
- Search query construction (OpenRice URL patterns, keyword ordering)
- Data extraction reliability (which fields peruro returns cleanly)
- Ranking heuristics (what to weight: distance, rating, corkage, price)

### 1c. Register in tool-index

Add to `~/officina/claude/tool-index.md` under Misc:

```
| Restaurant finder | `cibus` |
```

---

## Phase 2: Cost Optimisation (if stuck on peruro, ~1 hr)

Only needed if phase 0 yields no free path.

### 2a. Caching layer

Build a simple cache to avoid re-fetching recently-seen listings:

```
~/data/cibus/cache/<openrice-id>.json  # TTL: 7 days
```

Fields: name, address, phone, hours, price, corkage, rating, last_fetched.

### 2b. Two-tier fetch

1. `noesis search` for initial facts (free, ~$0.006/query) — enough to filter
2. `peruro` only for the top 3 candidates that survive filtering

Reduces from 5 credits → 3 credits per invocation.

---

## Phase 3: PoW Solver (stretch, ~4 hr)

Only if all free paths fail and we want to eliminate Firecrawl dependency entirely.

### 3a. Reverse-engineer the challenge

```bash
# Capture the challenge page HTML
peruro "https://www.openrice.com/en/hongkong" > /tmp/openrice-challenge.html

# Or use curl (gets the challenge page directly)
curl -sL "https://www.openrice.com/en/hongkong" > /tmp/openrice-challenge.html

# Extract the challenge JS
grep -oP '<script[^>]*>[^<]*sha256[^<]*</script>' /tmp/openrice-challenge.html
```

Understand: what nonce format, what difficulty target, what cookie/header to submit.

### 3b. Implement solver

Python script (not Rust — this is glue code, not performance-critical):

```python
# sha256_pow.py
# Input: challenge parameters from Cloudflare response
# Output: solved proof + cookie to attach to subsequent requests
```

### 3c. Integrate into fetch chain

```bash
# Solve PoW → get session cookie → curl with cookie
python3 sha256_pow.py --challenge "<params>" | \
  xargs -I{} curl -sH "Cookie: {}" "https://www.openrice.com/api/..."
```

---

## Execution Order

```
Phase 0  →  decision gate  →  Phase 1  →  (Phase 2 if peruro-only)
                                          (Phase 3 deferred to v2)
```

## Success Criteria

- `/cibus` returns a ranked shortlist with structured data for ≥3 restaurants
- Active health context (meds, dietary) integrated into recommendations
- Cost per invocation: ≤5 Firecrawl credits (ideally 0 if porta/API works)
- End-to-end latency: <60s for a 5-restaurant shortlist

## Risks

| Risk | Mitigation |
|------|------------|
| Firecrawl credits exhausted | Phase 2 caching + two-tier fetch |
| OpenRice changes URL structure | exauro search adapts; monitor manually |
| porta cookie injection fails on OpenRice | Expected — peruro is the fallback |
| Cloudflare upgrades PoW | peruro (Firecrawl) handles this upstream |
| Health context stale in vault | Skill reads NOW.md at invocation time |
