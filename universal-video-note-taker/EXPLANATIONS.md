# Skill Explanation: Universal Video Note-taker

## Purpose
A versatile agentic tool to process any video URL and create a highly readable, image-supported learning note based on the Cornell Note-taking system.

## Detailed Implementation

### 1. Universal Acquisition
- **Method**: `yt-dlp` integration.
- **Logic**: Extracts metadata and subtitles from any supported URL. If CC is unavailable, it extracts the audio stream for transcription.

### 2. Multi-tier Transcription
- **Logic**:
    - **Tier 1 (Native)**: Extract existing SRT/VTT subtitles.
    - **Tier 2 (AI-Generated)**: Extract audio via `ffmpeg`, then process via Whisper or similar AI models to generate text timestamps.

### 3. AI-Judged Keyframe Extraction
- **Method**: `ffmpeg` surgical capture.
- **Logic**: The AI scans the transcript for "pivot points" (e.g., transitions, summaries). It calculates the exact timestamp and uses `ffmpeg` to capture a JPG frame to provide visual context in the note.

### 4. Human-Easy-to-Read (Cornell) Layout
- **Logic**: Uses Obsidian-specific Callouts for summaries and keywords (Cues) to keep the core insights visible at a glance while preserving detailed chronological notes.
