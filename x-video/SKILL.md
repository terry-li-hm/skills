---
name: x-video
description: Transcribe X/Twitter video tweets and broadcasts. Use when user shares an X URL containing video or broadcast content and wants transcription.
user_invocable: false
---

# X Video Transcription

Transcribe video tweets and broadcasts from X/Twitter. Routes through `video-digest` pipeline with X-specific handling.

## URL Detection

| URL pattern | Type | Route |
|-------------|------|-------|
| `x.com/i/broadcasts/` | Broadcast | Step 1 (broadcast) |
| `x.com/*/status/*` with video | Video tweet | Step 2 (tweet) |
| `twitter.com/i/broadcasts/` | Broadcast | Step 1 (broadcast) |
| `twitter.com/*/status/*` with video | Video tweet | Step 2 (tweet) |

**Always use `bird read <url>` first** to check what the tweet contains (link, video, broadcast).

## Step 0: Check Tweet Content

```bash
bird read <URL>
```

If tweet links to a broadcast URL (`x.com/i/broadcasts/`), use Step 1.
If tweet has embedded video, use Step 2.
If tweet is text-only or links to an article, this skill doesn't apply — route to `summarize` or `video-digest`.

## Step 1: Broadcasts (Live Streams / Spaces Replays)

**CRITICAL GOTCHA:** Audio-only download (`-f "ba"`) from X broadcasts grabs a padded music/silence track — NOT the actual speech. Gemini will hallucinate entire fake conversations from music-only audio. This is a dangerous, confident failure mode.

```bash
# List formats to confirm broadcast
yt-dlp --cookies-from-browser chrome -F "BROADCAST_URL"

# Download VIDEO format (speech is in the video's audio track)
yt-dlp --cookies-from-browser chrome -f "replay-600" \
  -o "/tmp/media_broadcast.mp4" "BROADCAST_URL"

# Extract audio from video
ffmpeg -y -i /tmp/media_broadcast.mp4 -vn -acodec libmp3lame -q:a 3 /tmp/media_audio.mp3
```

Format selection:
- `replay-600` (528x336): good balance of speed vs quality — **default**
- `replay-300` (368x232): faster download, adequate audio
- `replay-2750` (1184x768): only if audio quality is poor at lower formats

**Verify audio has speech before uploading to Gemini:**
```bash
# Check duration (broadcast video is often shorter than audio-only download)
ffprobe /tmp/media_audio.mp3 2>&1 | grep Duration

# Quick volume check
cd /tmp && ffmpeg -i media_audio.mp3 -af "volumedetect" -f null /dev/null 2>&1 | grep mean_volume
# mean_volume > -30 dB = has content. If ~-60 dB = silence.
```

Then: upload to Gemini per `video-digest` Step 2.

## Step 2: Video Tweets

Standard yt-dlp audio extraction works fine for regular video tweets.

```bash
yt-dlp --cookies-from-browser chrome -f "ba[ext=m4a]/ba/b" \
  --extract-audio --audio-format mp3 --audio-quality 5 \
  -o "/tmp/media_audio.%(ext)s" "TWEET_URL"
```

Then: upload to Gemini per `video-digest` Step 2.

## Gemini Transcription

Chain to `video-digest` Step 2. Key settings:

```bash
GEMINI_API_KEY=$(security find-generic-password -s "gemini-api-key" -w 2>/dev/null)
```

Model: `gemini-2.5-flash`

For broadcasts >45 min, warn user before proceeding (large upload + cost).

## Validation

After transcription, sanity-check the first few lines:
- Does the content match the tweet topic?
- Are there real speaker names or topic references?
- If output is `[Music]`, `[No speakers]`, or <50 chars — wrong audio track. Re-download with video format.

## Error Handling

| Problem | Fix |
|---------|-----|
| Broadcast audio = music only | **Wrong track.** Download video format, extract audio from video |
| Gemini returns hallucinated dialogue | Music-only audio. Gemini fabricates speech confidently. Re-download via video |
| yt-dlp can't find broadcast | Add `--cookies-from-browser chrome`. X broadcasts need auth |
| Video tweet has no audio | Some video tweets are silent/music. Tell user |
| Download very slow (broadcasts) | `replay-300` is faster. Broadcasts download segment-by-segment via m3u8 |
