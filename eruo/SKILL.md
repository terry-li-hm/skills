---
name: eruo
description: Context lookup router — finds the right source for any query. "where do I find X?", "search for Y", "do we have notes on Z?"
user_invocable: false
---

# eruo

Single entry point for finding context. Routes to the right source rather than guessing or trying every tool.

## Decision Tree

**Step 1 — Is it about an active project?**
Go to the canonical tracker note directly. Faster and more reliable than any search tool.

| Topic | Check first |
|-------|------------|
| Capco / PILON / Gavin / Bertie / onboarding | `grep -n "." "/Users/terry/notes/Capco/Capco Transition.md"` |
| STR handover | `~/notes/Capco/STR Relabelling Handover.md` |
| Any active project | Tracker note linked from `~/notes/NOW.md` |

**Step 2 — Is it vault knowledge (concepts, decisions, reference)?**
```bash
cerno "<query>"
```
Waterfall: QMD (vault, authoritative) → oghma (conversation memory) fallback.

**Step 3 — Is it from a specific past conversation?**
```bash
anam search "<keyword>" --deep --days 30
```
Use single keywords, not phrases. Escalate to `--days 90` before concluding not found.

**Step 4 — Is it external / web?**
See `indago` skill for tool selection (WebSearch → pplx → grok).

## Common Mistakes

- **Reaching for cerno before checking the tracker note.** Council transcripts score low; the tracker note has the answer clean.
- **Using oghma directly.** Use `cerno` instead — it wraps oghma with the vault as a higher-quality first pass.
- **Concluding "not found" after 7 days on anam.** Default window is 7 days. Always escalate: `--days 30` → `--days 90`.
- **Searching externally for something that's in the vault.** Internal sources first, always.
- **Searching by use-case name when vault files are named by document type.** If cerno/grep misses, the file probably exists under a different name (e.g. "AML monthly meeting slides" → `AML AI Roadmap.md`). Fallback: read the hub note for the topic area and `Glob` the directory — don't conclude "not in vault" after a keyword miss alone.
- **Concept search misses → try a known data point.** If searching by topic fails, search for a specific figure or number the user mentioned (e.g. `142,270`, `48,845`). Numbers are unique and grep reliably to the right note.
- **Treating stakeholder context as co-located with content.** Who Benjamin is lives in `CNCBI Exit.md`; what he's working on lives in `Work/CITIC_AML/`. Cross-folder joins are normal — check both.

## When to Use

Any time the question is "do we have notes on X?", "what did we decide about Y?", "find the draft for Z" — run through this tree in order. Don't skip to step 4.
