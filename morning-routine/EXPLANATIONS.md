# Skill Explanation: Morning Routine

## Purpose
Automates the start of the workday by synchronizing research papers, processing pending video notes, and managing the Obsidian `HomePage.md`.

## Detailed Implementation

### 1. Bilingual Paper Recommendation
- **Method**: `start-my-day` integration.
- **Logic**: Reads today's paper notes, detects language, and uses AI to ensure a bilingual (CN/EN) format for titles and abstracts.

### 2. Pending Video Processing
- **Method**: `bilibili-auto-transcript` orchestration.
- **Input**: Frontmatter `url` from notes tagged with `#pending/video`.
- **Logic**:
    1. Extract URL.
    2. Invoke transcription skill to get summaries.
    3. Match content against `_tags_index.md` for standardized tagging.
    4. Move the finalized note to `VideoNotes/`.
- **Output**: Updated Markdown note with transcript, tags, and status changed to `#completed/video`.

### 3. HomePage & Archive Management
- **Method**: Date-based routing.
- **Logic**: Checks if the date in `HomePage.md` is current. If not, it calculates the week folder and archives old content before initializing a new daily summary.
