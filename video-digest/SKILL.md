---
name: video-digest
description: Video/podcast URL to full transcript + structured digest. Bilibili, YouTube, Xiaoyuzhou, Apple Podcasts, X, direct audio.
user_invocable: false
source: Adapted from github.com/runesleo/x-reader (Feb 2026)
---

# Video & Podcast Digest

Full transcription pipeline for video and podcast URLs. Called by `summarize` and `analyze` skills when media URLs are detected — not invoked directly.

## When to Use

Route here when the URL matches a media platform and the user wants content extraction (not just metadata). For YouTube transcripts with available subtitles, `summarize` can handle directly via `youtube-transcript-api`. This skill is for the full pipeline: no subtitles, non-YouTube platforms, or audio-only content.

## Supported Platforms

| Platform | Subtitles | Whisper | Notes |
|----------|-----------|---------|-------|
| YouTube | Yes (yt-dlp) | Yes | Prefer `youtube-transcript-api` in `summarize` first |
| Bilibili | Yes (yt-dlp) | Yes | yt-dlp gets 412 — use Bilibili API for audio (Step 1d) |
| X/Twitter | No | Yes | Video tweets only |
| Xiaoyuzhou | No | Yes | `__NEXT_DATA__` extraction |
| Apple Podcasts | No | Yes | Via yt-dlp |
| Direct links (.mp3/.mp4/.m4a/.webm/.m3u8) | No | Yes | |

## Prerequisites

```bash
brew install yt-dlp    # video download + subtitle extraction
# ffmpeg already installed — audio conversion + segmentation
```

**Groq API key** (free at https://console.groq.com/keys):
```bash
security add-generic-password -s "groq-api" -a "$(whoami)" -w "YOUR_KEY"
```

Retrieve in scripts:
```bash
GROQ_API_KEY=$(security find-generic-password -s "groq-api" -w 2>/dev/null)
```

## Pipeline

### Step 0: Detect Media Type

| URL Pattern | Type | Route |
|-------------|------|-------|
| `xiaoyuzhoufm.com/episode/` | Podcast | Step 1b |
| `podcasts.apple.com` | Podcast | Step 1c |
| `bilibili.com`, `b23.tv` | Video | Step 1d (Bilibili API) |
| `.mp3`, `.m4a` direct link | Audio | Step 2b |
| Other video URL | Video | Step 1a (subtitle extraction) |

### Step 1a: Extract Subtitles (YouTube, generic)

```bash
rm -f /tmp/media_sub*.vtt /tmp/media_audio.mp3 /tmp/media_transcript*.json /tmp/media_segment_*.mp3 2>/dev/null || true

# YouTube (prefer English, fallback Chinese)
yt-dlp --skip-download --write-auto-sub --sub-lang "en,zh-Hans" -o "/tmp/media_sub" "VIDEO_URL"
```

Check: `ls /tmp/media_sub*.vtt 2>/dev/null`
- Has subtitles: read VTT, skip to Step 3
- No subtitles: Step 2a

### Step 1b: Xiaoyuzhou — Extract Audio URL

```bash
AUDIO_URL=$(curl -sL -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "EPISODE_URL" \
  | grep -oE 'https://media\.xyzcdn\.net/[^"]+\.(m4a|mp3)' \
  | head -1)

curl -L -o /tmp/media_audio.mp3 "$AUDIO_URL"
```

If curl extraction empty: use `agent-browser` to render and extract.
Then: Step 2b.

### Step 1c: Apple Podcasts — via yt-dlp

```bash
yt-dlp -f "ba[ext=m4a]/ba/b" --extract-audio --audio-format mp3 --audio-quality 5 \
  -o "/tmp/media_audio.%(ext)s" "APPLE_PODCAST_URL"
```

Then: Step 2b.

### Step 1d: Bilibili — API Direct Audio

yt-dlp returns 412 for Bilibili. Use Bilibili's public API:

```bash
BV="BV1xxxxx"  # extract from URL

# Get video info
curl -s "https://api.bilibili.com/x/web-interface/view?bvid=$BV" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f\"Title: {d['title']}\nDuration: {d['duration']}s\nCID: {d['cid']}\")"

# Get audio stream URL
CID=<from_above>
AUDIO_URL=$(curl -s "https://api.bilibili.com/x/player/playurl?bvid=$BV&cid=$CID&fnval=16&qn=64" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['dash']['audio'][0]['baseUrl'])")

# Download + convert (Referer required, otherwise 403)
curl -L -o /tmp/media_audio.m4s \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/" "$AUDIO_URL"
ffmpeg -y -i /tmp/media_audio.m4s -acodec libmp3lame -q:a 5 /tmp/media_audio.mp3
```

Then: Step 2b.

### Step 2a: Download Audio (no subtitles)

```bash
# --cookies-from-browser chrome helps bypass YouTube bot detection
yt-dlp --cookies-from-browser chrome -f "ba[ext=m4a]/ba/b" --extract-audio --audio-format mp3 --audio-quality 5 \
  -o "/tmp/media_audio.%(ext)s" "VIDEO_URL"
```

### Step 2b: Check Size & Segment

```bash
FILE_SIZE=$(stat -f%z /tmp/media_audio.* 2>/dev/null)
echo "File size: $FILE_SIZE bytes"
```

- 25MB or under: Step 2c directly
- Over 25MB: segment first

```bash
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/media_audio.* | head -1)
SEGMENT_SEC=600
SEGMENTS=$(python3 -c "import math; print(math.ceil(float('$DURATION')/$SEGMENT_SEC))")

for i in $(seq 0 $((SEGMENTS-1))); do
  START=$((i * SEGMENT_SEC))
  ffmpeg -y -i /tmp/media_audio.* -ss $START -t $SEGMENT_SEC -acodec libmp3lame -q:a 5 \
    "/tmp/media_segment_${i}.mp3" 2>/dev/null
done
```

Transcribe each segment **sequentially** (parallel triggers Groq 524 timeout). Concatenate results.

### Step 2c: Whisper Transcription

```bash
GROQ_API_KEY=$(security find-generic-password -s "groq-api" -w 2>/dev/null)
if [ -z "$GROQ_API_KEY" ]; then
  echo "No Groq API key in keychain. Add: security add-generic-password -s groq-api -a \$(whoami) -w YOUR_KEY"
  exit 1
fi

curl -s -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@AUDIO_FILE" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json" \
  -F "language=zh" \
  > /tmp/media_transcript.json

python3 -c "import json; print(json.load(open('/tmp/media_transcript.json'))['text'])"
```

| Model | Speed | Use |
|-------|-------|-----|
| `whisper-large-v3-turbo` | 10x realtime | Default |
| `whisper-large-v3` | 5x realtime | Noisy/professional content |

Language: `zh` (Chinese), `en` (English), or omit for auto-detect.

### Step 3: Structured Digest

**Short content (under 20 min):**
- Overview (1-2 sentences)
- Key Points (3-5 bullets)
- Notable Quotes (if any)
- Action Items (if applicable)

**Long content (20+ min):**
- Overview (2-3 sentences: who discussed what)
- Chapter Summary (segmented by topic shift, 2-3 sentences each)
- Key Points (5-8 bullets)
- Notable Quotes
- Action Items (if applicable)

## Error Handling

| Problem | Fix |
|---------|-----|
| No subtitles + no Groq key | Prompt user to add key to keychain |
| Audio over 25MB | ffmpeg segment at 10min intervals, transcribe sequentially |
| Podcast over 2 hours | Warn + confirm before proceeding |
| Groq 524 timeout | Never parallelize — sequential only, 5-8s sleep between segments |
| Groq 429 rate limit | 7200s/hour rolling window. Wait for `retry-after` header |
| yt-dlp Bilibili 412 | Use Bilibili API (Step 1d) |
| yt-dlp YouTube bot detection | Add `--cookies-from-browser chrome` |
| Spotify | Not supported (DRM). Tell user |

## Groq Whisper Limits

- Max 25MB per request
- Free tier: 7200 seconds of audio/hour (~2 hours), ~20 hours/day
- Formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
