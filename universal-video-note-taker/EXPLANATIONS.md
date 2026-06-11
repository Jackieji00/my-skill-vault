# Skill Explanation: Universal Video Note-taker

## Detailed Implementation

### 1. `clean_url(url)`
- **Input**: Raw Video URL.
- **Logic**: Strips tracking and session parameters (like XHS Android share tags) to present a clean URL to `yt-dlp`, reducing the chance of 403 errors.
- **Output**: Cleaned URL string.

### 2. `get_subtitles(url)`
- **Logic**: Implements the **Tiered Transcription** pattern:
    - **Step 1**: Try `yt-dlp --write-subs`.
    - **Step 2**: Try `yt-dlp --write-auto-subs`.
    - **Step 3**: Extract audio via `ffmpeg`, then process via `openai-whisper` (Small/Medium model based on GPU VRAM).

### 3. `capture_keyframes(video_path, timestamps, output_dir)`
- **Input**: Video source, AI-determined timestamps, and `_attachments/video-notes/`.
- **Logic**: Executes `ffmpeg -ss` to capture frames at specific moments identified as "meaningful transitions" by the AI.
- **Output**: JPG files saved in the standardized attachments folder.

### 4. `generate_cornell_note(...)`
- **Logic**: Combines all extracted data into a Cornell-structured Markdown template. Uses Obsidian callouts for visual hierarchy.
