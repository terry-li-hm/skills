#!/usr/bin/env python3
"""
YouTube Transcript Extractor

A utility script to extract transcripts from YouTube videos.
Uses the youtube-transcript-api library.

Usage:
    python extract_transcript.py <video_id_or_url> [options]

Examples:
    python extract_transcript.py dQw4w9WgXcQ
    python extract_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    python extract_transcript.py dQw4w9WgXcQ --language de
    python extract_transcript.py dQw4w9WgXcQ --format json
    python extract_transcript.py dQw4w9WgXcQ --timestamps
"""

import argparse
import html
import json
import re
import sys
from typing import Optional

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import (
        JSONFormatter,
        TextFormatter,
        SRTFormatter,
        WebVTTFormatter,
    )
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    )
except ImportError:
    print("Error: youtube-transcript-api is not installed.")
    print("Install it with: pip install youtube-transcript-api")
    sys.exit(1)


def extract_video_id(url_or_id: str) -> str:
    """
    Extract the video ID from a YouTube URL or return the ID if already provided.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    - Just the VIDEO_ID itself
    """
    # Pattern for various YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'  # Just the video ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    # If no pattern matches, assume it's the video ID
    return url_or_id.strip()


def clean_transcript_text(text: str, remove_annotations: bool = True) -> str:
    """
    Clean up transcript text by removing artifacts and normalizing formatting.

    Args:
        text: The raw transcript text
        remove_annotations: Remove [Music], [Applause], etc. annotations

    Returns:
        Cleaned transcript text
    """
    # Decode HTML entities (e.g., &amp; -> &, &#39; -> ')
    text = html.unescape(text)

    if remove_annotations:
        # Remove bracketed annotations like [Music], [Applause], [Laughter], etc.
        text = re.sub(r'\[[^\]]*\]', '', text)

    # Remove speaker labels (e.g., ">> JOHN:", "SPEAKER 1:", "- Speaker:")
    text = re.sub(r'(?:^|\s)>>?\s*[A-Z][A-Z\s]*:', '', text)
    text = re.sub(r'(?:^|\s)SPEAKER\s*\d*:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(?:^|\s)-\s*[A-Za-z]+:', '', text)

    # Remove multiple spaces and normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def get_transcript(
    video_id: str,
    languages: list[str] = None,
    preserve_formatting: bool = False
) -> tuple[list, dict]:
    """
    Fetch the transcript for a YouTube video.

    Args:
        video_id: The YouTube video ID
        languages: List of language codes in priority order (default: ['en'])
        preserve_formatting: Whether to preserve HTML formatting tags

    Returns:
        Tuple of (transcript_data, metadata)
    """
    if languages is None:
        languages = ['en']

    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(
        video_id,
        languages=languages,
        preserve_formatting=preserve_formatting
    )

    metadata = {
        'video_id': transcript.video_id,
        'language': transcript.language,
        'language_code': transcript.language_code,
        'is_generated': transcript.is_generated,
    }

    return transcript, metadata


def list_available_transcripts(video_id: str) -> list[dict]:
    """
    List all available transcripts for a video.

    Args:
        video_id: The YouTube video ID

    Returns:
        List of transcript info dictionaries
    """
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)

    available = []
    for t in transcript_list:
        available.append({
            'language': t.language,
            'language_code': t.language_code,
            'is_generated': t.is_generated,
            'is_translatable': t.is_translatable,
        })

    return available


def format_transcript(
    transcript,
    output_format: str = 'text',
    include_timestamps: bool = False,
    clean: bool = False
) -> str:
    """
    Format the transcript in the specified format.

    Args:
        transcript: The FetchedTranscript object
        output_format: One of 'text', 'json', 'srt', 'vtt'
        include_timestamps: Include timestamps in text output
        clean: Apply text cleanup to remove annotations and normalize text

    Returns:
        Formatted transcript string
    """
    if output_format == 'json':
        formatter = JSONFormatter()
        output = formatter.format_transcript(transcript, indent=2)
        if clean:
            # For JSON, we need to parse, clean each text field, and re-serialize
            data = json.loads(output)
            for item in data:
                if 'text' in item:
                    item['text'] = clean_transcript_text(item['text'])
            output = json.dumps(data, indent=2)
        return output

    elif output_format == 'srt':
        formatter = SRTFormatter()
        output = formatter.format_transcript(transcript)
        if clean:
            # Clean each subtitle block while preserving SRT structure
            lines = output.split('\n')
            cleaned_lines = []
            for line in lines:
                # Don't clean index numbers or timestamps
                if line.strip().isdigit() or '-->' in line or line.strip() == '':
                    cleaned_lines.append(line)
                else:
                    cleaned_lines.append(clean_transcript_text(line))
            output = '\n'.join(cleaned_lines)
        return output

    elif output_format == 'vtt':
        formatter = WebVTTFormatter()
        output = formatter.format_transcript(transcript)
        if clean:
            # Clean each subtitle block while preserving VTT structure
            lines = output.split('\n')
            cleaned_lines = []
            for line in lines:
                # Don't clean header, timestamps, or empty lines
                if line.startswith('WEBVTT') or '-->' in line or line.strip() == '':
                    cleaned_lines.append(line)
                else:
                    cleaned_lines.append(clean_transcript_text(line))
            output = '\n'.join(cleaned_lines)
        return output

    else:  # text format
        if include_timestamps:
            lines = []
            for snippet in transcript:
                minutes = int(snippet.start // 60)
                seconds = int(snippet.start % 60)
                text = clean_transcript_text(snippet.text) if clean else snippet.text
                lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")
            return "\n".join(lines)
        else:
            text = " ".join([snippet.text for snippet in transcript])
            if clean:
                text = clean_transcript_text(text)
            return text


def main():
    parser = argparse.ArgumentParser(
        description='Extract transcripts from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'video',
        help='YouTube video ID or URL'
    )

    parser.add_argument(
        '-l', '--language',
        nargs='+',
        default=['en'],
        help='Language code(s) in priority order (default: en)'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json', 'srt', 'vtt'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '-t', '--timestamps',
        action='store_true',
        help='Include timestamps in text output'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available transcripts instead of fetching'
    )

    parser.add_argument(
        '--preserve-formatting',
        action='store_true',
        help='Preserve HTML formatting tags in transcript'
    )

    parser.add_argument(
        '-c', '--clean',
        action='store_true',
        help='Clean transcript text (remove [Music], [Applause], speaker labels, etc.)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )

    args = parser.parse_args()

    # Extract video ID
    video_id = extract_video_id(args.video)

    try:
        if args.list:
            # List available transcripts
            available = list_available_transcripts(video_id)
            print(f"Available transcripts for video {video_id}:\n")
            for t in available:
                gen_status = "auto-generated" if t['is_generated'] else "manual"
                trans_status = "translatable" if t['is_translatable'] else "not translatable"
                print(f"  - {t['language']} ({t['language_code']}): {gen_status}, {trans_status}")
        else:
            # Fetch transcript
            transcript, metadata = get_transcript(
                video_id,
                languages=args.language,
                preserve_formatting=args.preserve_formatting
            )

            # Format output
            output = format_transcript(
                transcript,
                output_format=args.format,
                include_timestamps=args.timestamps,
                clean=args.clean
            )

            # Write output
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Transcript saved to {args.output}")
            else:
                print(output)

            # Print metadata to stderr
            print(f"\n--- Metadata ---", file=sys.stderr)
            print(f"Video ID: {metadata['video_id']}", file=sys.stderr)
            print(f"Language: {metadata['language']} ({metadata['language_code']})", file=sys.stderr)
            print(f"Auto-generated: {metadata['is_generated']}", file=sys.stderr)

    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video {video_id}", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print(f"Error: No transcript found for video {video_id} in languages: {args.language}", file=sys.stderr)
        print("Use --list to see available transcripts", file=sys.stderr)
        sys.exit(1)
    except VideoUnavailable:
        print(f"Error: Video {video_id} is unavailable (private, deleted, or region-blocked)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
