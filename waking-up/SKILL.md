---
name: waking-up
description: Waking Up meditation transcripts — catalog, transcribe, search, rename. "waking up", "wu", "transcribe meditation"
user_invocable: true
---

# Waking Up Transcripts

Manage the Waking Up meditation transcript pipeline via the `wu` CLI (`~/code/wu/`).

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
wu batch batch_all_titled.json                                     # Batch 1 done (Deepgram)
wu batch batch_phase2.json --model gemini-2.5-flash               # Phase 2: 167 sessions (recommended)
wu batch batch_retry_large.json --model or:gemini-3-flash -c 1   # Large files auto-split into 15-min chunks
wu batch-async batch_phase2.json --enrich                         # Speechmatics async only (not Gemini)
wu compare <audio_id>                                              # Compare backends on one session
wu compare <audio_id> --models speechmatics,gemini-2.5-flash      # Custom model set
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
TOKEN=$(python3 -c "import json; d=json.load(open('~/code/wu/browser-auth-state.json')); print(next(c['value'] for c in d['cookies'] if c['name']=='STYXKEY-token'))")
agent-browser --session wu-session open "https://app.wakingup.com"
agent-browser --session wu-session eval "document.cookie='STYXKEY-token=$TOKEN; path=/; domain=.wakingup.com; secure'"
agent-browser --session wu-session open "https://app.wakingup.com/packs/<HASH>"
# Then snapshot → extract course titles → match against all_courses.json by title+type+duration
```

## Key Paths

- **Repo:** `~/code/wu/`
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

- Deepgram Nova-3 is the default model — **$0.0056/min all-in**, used for Batch 1
- Already-processed sessions are skipped automatically (check vault for existing `.md`)
- The `--force` flag re-downloads and re-transcribes even if output exists
- Audio is cached in `~/.cache/waking-up-audio/` — safe to clear for disk space
- `batch-async` is **Speechmatics-specific** (async submit/poll/fetch). Use `batch` for Gemini.
- **Auto split-and-concatenate:** `or:*` models auto-split files >20MB into 15-min ffmpeg chunks, transcribe each, concatenate. No manual splitting needed.

## STT Provider Comparison (tested Feb 2026)

**Recommended for Phase 2: `gemini-2.5-flash`**
- ~$0.0015/min (~$6.75 for 167 sessions vs ~$18 for Speechmatics)
- Matches or beats Speechmatics on Buddhist vocabulary (correctly got "Vipassana" where SM failed)
- No audio duration limit
- Use system prompt with Buddhist glossary instead of `sounds_like`

**Speechmatics Pro** (available, tested):
- $0.004/min, `sounds_like` phoneme hints for Sanskrit/Pali
- `speaker_diarization_config.max_speakers` field removed (breaking change Feb 2026 — already fixed)
- API is async batch (submit → poll → fetch) — different architecture from Gemini

**Avoid:**
- `gemini-3-flash-preview`: output token limit truncates ~38% of 27-min sessions
- `gpt-4o-transcribe`: hard 1400s (~23 min) audio duration limit — rules out most sessions
- Groq/Whisper: hallucination on quiet audio, no vocab injection
- Google Cloud Speech / AWS: 6× more expensive

Full gotchas: `~/docs/solutions/stt-api-gotchas.md`
Full results: `~/notes/Waking Up/STT Comparison Results.md`
