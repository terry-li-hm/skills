---
name: youtube-transcript
description: Extract transcripts/subtitles from YouTube videos. Use when the user wants to get the transcript, captions, or subtitles from a YouTube video URL or video ID.
---

# YouTube Transcript Extractor

This skill extracts transcripts from YouTube videos using the `youtube-transcript-api` library.

## When to Use

Use this skill when the user:
- Asks to get the transcript of a YouTube video
- Wants to extract subtitles or captions from a YouTube video
- Needs the text content from a YouTube video for analysis, summarization, or other purposes
- Provides a YouTube URL or video ID and asks for its transcript

## Instructions

### Step 1: Extract the Video ID

From a YouTube URL, extract the video ID:
- `https://www.youtube.com/watch?v=VIDEO_ID` → use `VIDEO_ID`
- `https://youtu.be/VIDEO_ID` → use `VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID` → use `VIDEO_ID`
- If the user provides just the ID (e.g., `dQw4w9WgXcQ`), use it directly

### Step 2: Install Dependencies

Ensure the `youtube-transcript-api` package is installed:

```bash
pip install youtube-transcript-api
```

### Step 3: Extract the Transcript

Use the Python script provided in this skill or write inline Python code:

```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id, languages=['en']):
    """
    Extract transcript from a YouTube video.

    Args:
        video_id: The YouTube video ID (not the full URL)
        languages: List of language codes in priority order (default: ['en'])

    Returns:
        A list of transcript snippets with text, start time, and duration
    """
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript = ytt_api.fetch(video_id, languages=languages)
        return transcript
    except Exception as e:
        return f"Error fetching transcript: {e}"

# Example usage
video_id = "VIDEO_ID_HERE"
transcript = get_transcript(video_id)

# Print the full transcript text
for snippet in transcript:
    print(snippet.text)
```

### Step 4: Format the Output

You can format the transcript in different ways:

**Plain text (concatenated):**
```python
full_text = " ".join([snippet.text for snippet in transcript])
print(full_text)
```

**With timestamps:**
```python
for snippet in transcript:
    minutes = int(snippet.start // 60)
    seconds = int(snippet.start % 60)
    print(f"[{minutes:02d}:{seconds:02d}] {snippet.text}")
```

**As JSON:**
```python
from youtube_transcript_api.formatters import JSONFormatter
formatter = JSONFormatter()
json_output = formatter.format_transcript(transcript, indent=2)
print(json_output)
```

**As SRT subtitle format:**
```python
from youtube_transcript_api.formatters import SRTFormatter
formatter = SRTFormatter()
srt_output = formatter.format_transcript(transcript)
print(srt_output)
```

### Step 5: Clean Up the Transcript (Optional)

YouTube transcripts often contain artifacts that you may want to remove:

| Artifact | Example | Description |
|----------|---------|-------------|
| Annotations | `[Music]`, `[Applause]` | Sound/action descriptions |
| Speaker labels | `>> JOHN:`, `SPEAKER 1:` | Speaker identifiers |
| HTML entities | `&amp;`, `&#39;` | Encoded characters |

Use the cleanup function to remove these:

```python
import html
import re

def clean_transcript_text(text, remove_annotations=True):
    """Clean up transcript text by removing artifacts."""
    # Decode HTML entities
    text = html.unescape(text)

    if remove_annotations:
        # Remove [Music], [Applause], etc.
        text = re.sub(r'\[[^\]]*\]', '', text)

    # Remove speaker labels
    text = re.sub(r'(?:^|\s)>>?\s*[A-Z][A-Z\s]*:', '', text)
    text = re.sub(r'(?:^|\s)SPEAKER\s*\d*:', '', text, flags=re.IGNORECASE)

    # Normalize whitespace
    text = ' '.join(text.split())
    return text

# Apply cleanup to transcript
full_text = " ".join([snippet.text for snippet in transcript])
clean_text = clean_transcript_text(full_text)
print(clean_text)
```

Or use the CLI script with the `--clean` flag:

```bash
python extract_transcript.py VIDEO_ID --clean
```

## Available Formatters

- `JSONFormatter` - JSON format
- `TextFormatter` - Plain text
- `WebVTTFormatter` - WebVTT subtitle format
- `SRTFormatter` - SRT subtitle format
- `PrettyPrintFormatter` - Human-readable format

## Language Support

To get transcripts in specific languages:

```python
# Try German first, then English
transcript = ytt_api.fetch(video_id, languages=['de', 'en'])

# List all available transcripts for a video
transcript_list = ytt_api.list(video_id)
for t in transcript_list:
    print(f"{t.language} ({t.language_code}) - Generated: {t.is_generated}")
```

## Translation

If a transcript supports translation:

```python
transcript_list = ytt_api.list(video_id)
transcript = transcript_list.find_transcript(['en'])

if transcript.is_translatable:
    translated = transcript.translate('es')  # Translate to Spanish
    result = translated.fetch()
```

## Error Handling

Common errors to handle:
- **TranscriptsDisabled**: Video has transcripts disabled
- **NoTranscriptFound**: No transcript available in requested languages
- **VideoUnavailable**: Video is private, deleted, or region-blocked

```python
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

try:
    transcript = ytt_api.fetch(video_id)
except TranscriptsDisabled:
    print("Transcripts are disabled for this video")
except NoTranscriptFound:
    print("No transcript found in the requested language")
except VideoUnavailable:
    print("Video is unavailable")
```

## Error Handling

- **If TranscriptsDisabled**: Video has transcripts disabled — inform user, no workaround
- **If NoTranscriptFound**: No transcript in requested language — try other languages or auto-generated
- **If VideoUnavailable**: Video is private, deleted, or region-blocked — inform user
- **If rate limited**: YouTube may throttle; wait and retry
- **If IP blocked**: Cloud server IPs may be blocked; suggest user run locally or use proxy

## Limitations

- Age-restricted videos may not be accessible
- Some videos have transcripts disabled by the uploader
- Cloud server IPs may be blocked by YouTube (use proxies if needed)
- Auto-generated transcripts may contain errors

## Example Workflow

1. User provides: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Extract video ID: `dQw4w9WgXcQ`
3. Run the extraction script
4. Return the transcript text to the user
5. Optionally summarize or analyze the content as requested
