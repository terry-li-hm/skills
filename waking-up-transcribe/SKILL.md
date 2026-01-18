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

## Workflow

### 1. Capture Audio IDs (Browser)

User must capture audio IDs from app.wakingup.com:

1. Open https://app.wakingup.com and log in
2. Open DevTools Console (F12)
3. Paste contents of `~/repos/waking-up-transcripts/extract_audio_ids.js`
4. Navigate to a pack and **play each lesson briefly** (just start it)
5. Run `copyWakingUpAudioIds()` to copy IDs to clipboard

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
- `--model tiny|base|small|medium|large` - Whisper model (base recommended)
- `--workers N` - Parallel download threads (default: 10)
- `--force` - Re-process even if exists

**Single lesson:**
```bash
python download_and_transcribe.py <audio_id> "<title>" --teacher "<name>" --pack "<pack>"
```

### 4. Verify Output

Check `~/notes/Waking Up/[Pack]/` for generated Markdown files.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No segments found" | Wrong audio ID - replay lesson and check console |
| Whisper out of memory | Use `--model tiny` |
| Slow transcription | Whisper runs on CPU; use smaller model |

## Dependencies

- Python 3.11+
- ffmpeg (`brew install ffmpeg`)
- openai-whisper (`pip install openai-whisper`)
- requests (`pip install requests`)
