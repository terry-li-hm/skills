---
name: waking-up
description: Waking Up meditation transcripts — catalog, transcribe, search, rename. "waking up", "wu", "transcribe meditation"
user_invocable: true
---

# Waking Up Transcripts

Manage the Waking Up meditation transcript pipeline via the `wu` CLI (`~/repos/wu/`).

## Trigger

Use when:
- User says "waking up", "wu", "transcribe", "meditation transcripts"
- Any question about the Waking Up catalog, audio IDs, or transcript status

## Quick Commands

```bash
wu catalog                    # show catalog stats (courses, types)
wu catalog <file.json>        # import new courses dump from browser extraction
wu search "Alan Watts"        # search by title/slug
wu search "zen" --type talk   # filter by content type
wu info <audio_id>            # show metadata + vault status for a UUID
wu transcribe <id> "Title" --teacher "Name" --pack "Pack"   # single session
wu batch batch_all_titled.json                                # batch run
wu rename --dry-run           # preview placeholder renames
wu rename                     # apply renames
```

## Common Workflows

### Check what's in the catalog
```bash
wu catalog          # 1831 courses, breakdown by type
wu search "Tao"     # find specific content
```

### Transcribe a single session
```bash
wu info <audio_id>                        # check if already transcribed
wu transcribe <id> "Title" --teacher "Sam Harris" --pack "Fundamentals"
```

### Batch transcribe
```bash
wu batch batch_all_titled.json            # Batch 1: Alan Watts (115 sessions) — DONE
wu batch batch_phase2.json               # Phase 2: Theory series (167 sessions) — READY, needs Deepgram credits
wu batch batch_all_titled.json --force    # re-transcribe everything
```

### Rename placeholders after batch
```bash
wu rename --dry-run    # see what would change
wu rename              # apply renames
```

### Refresh catalog (browser extraction required)
1. Go to https://app.wakingup.com, open DevTools Console
2. Paste `extract_audio_ids.js` from the repo
3. Navigate packs to capture GraphQL responses
4. Run `copyWakingUpSessions()` or `getWakingUpSessions()`
5. Save JSON to file, then: `wu catalog <file.json>`

### Get pack course listings via browser (for batch building)
```bash
# Auth works via stored browser-auth-state.json
# agent-browser --session wu-session can log in with:
TOKEN=$(python3 -c "import json; d=json.load(open('~/repos/wu/browser-auth-state.json')); print(next(c['value'] for c in d['cookies'] if c['name']=='STYXKEY-token'))")
agent-browser --session wu-session open "https://app.wakingup.com"
agent-browser --session wu-session eval "document.cookie='STYXKEY-token=$TOKEN; path=/; domain=.wakingup.com; secure'"
agent-browser --session wu-session open "https://app.wakingup.com/packs/<HASH>"
# Then snapshot → extract course titles → match against all_courses.json by title+type+duration
```

## Key Paths

- **Repo:** `~/repos/wu/`
- **Vault transcripts:** `~/notes/Waking Up/`
- **Audio cache:** `~/.cache/waking-up-audio/`
- **Catalog data:** `all_courses.json`, `audio_id_mapping.json` (in repo root)
- **Batch files:** `batch_all_titled.json` (Batch 1, done), `batch_phase2.json` (167 sessions, ready)

## Error Handling

- **DEEPGRAM_API_KEY not set**: Should be in `~/.zshenv`. Required for transcription.
- **No segments found**: Audio ID may be invalid or content removed from CDN.
- **ffmpeg failed**: Ensure ffmpeg is installed (`brew install ffmpeg`).
- **No cached catalog**: Run `wu catalog` with a JSON file first, or use existing repo data.

## Notes

- Deepgram Nova-3 is the default transcription model — **$0.0056/min all-in** ($0.0043 base + $0.0013 keyterm add-on), ~5.3% WER
- Already-processed sessions are skipped automatically (check vault for existing `.md`)
- The `--force` flag re-downloads and re-transcribes even if output exists
- Audio is cached in `~/.cache/waking-up-audio/` — safe to clear for disk space

## STT Provider Comparison (Feb 2026)

For future phases, **Speechmatics Pro** is the strongest alternative:
- $0.004/min all-in (cheaper than Deepgram all-in)
- `sounds_like` phonetic guidance for Sanskrit/Pali terms (IPA mapping)
- 1,000 words/job limit (vs Deepgram's 100 terms)
- 480 min/month free tier (recurring) — enough to test a full pack

Before committing to Phase 3 on Speechmatics: run one ~30-min pack through both providers with term list and compare Sanskrit accuracy manually.

**Avoid:** Groq/OpenAI Whisper (no vocab injection, hallucination issues on quiet audio), Google/AWS (6× more expensive), self-hosted Whisper (infra overhead + hallucination risk).
