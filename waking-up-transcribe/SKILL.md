# Waking Up Transcribe

Transcribe Waking Up app audio lessons into Obsidian notes.

## Trigger

Use when user says:
- "transcribe waking up"
- "waking up transcript"
- "transcribe [lesson name]"
- "add waking up lessons"

## Paths

- **Repo:** `~/repos/waking-up-transcripts/`
- **Output:** `~/notes/Waking Up/[Pack]/[Title].md`
- **Cache:** `~/.cache/waking-up-audio/`
- **Catalog:** `~/repos/waking-up-transcripts/catalog/`

## Workflow

### 1. Capture Audio IDs (Browser)

User must capture audio IDs from app.wakingup.com:

1. Open https://app.wakingup.com and log in
2. Open DevTools Console (F12)
3. Paste contents of `~/repos/waking-up-transcripts/extract_audio_ids.js`
4. **Just open a pack** - the v2 extractor captures IDs from GraphQL responses automatically!
5. Run `copyWakingUpSessions()` to copy sessions with metadata, or `copyNonMeditations()` to exclude guided meditations

### 2. Create Batch File

Create JSON at `~/repos/waking-up-transcripts/batch.json`:

```json
[
  {
    "audio_id": "f5e2e44b-04c1-4ddc-bba6-9aed02767558",
    "title": "The Logic of Practice",
    "teacher": "Sam Harris",
    "pack": "Fundamentals"
  }
]
```

Required fields: `audio_id`, `title`
Optional fields: `teacher` (default: "Unknown"), `pack` (default: "Uncategorized")

### 3. Run Transcription

```bash
cd ~/repos/waking-up-transcripts
python download_and_transcribe.py --batch batch.json --model base
```

**Options:**
- `--model MODEL` - Transcription model (default: gpt-4o-mini-transcribe at $0.003/min)
- `--workers N` - Parallel download threads (default: 10)
- `--force` - Re-process even if exists

**Models:**
| Model | Cost/min | Notes |
|-------|----------|-------|
| gpt-4o-mini-transcribe | $0.003 | Recommended, 50% cheaper |
| whisper-1 | $0.006 | Legacy |
| gpt-4o-transcribe | $0.006 | Highest accuracy |

**Single lesson:**
```bash
python download_and_transcribe.py <audio_id> "<title>" --teacher "<name>" --pack "<pack>"
```

### 4. Verify Output

Check `~/notes/Waking Up/[Pack]/` for generated Markdown files.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No segments found" | Wrong audio ID - refresh page and check console |
| Rate limit errors | Script has built-in retry; just wait |
| Interrupted batch | Re-run same command - it skips completed files |

## Dependencies

- Python 3.11+
- ffmpeg (`brew install ffmpeg`)
- openai (`pip install openai`)
- requests (`pip install requests`)
