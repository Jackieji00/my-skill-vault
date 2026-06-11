# Skill Explanation: LeetCode Sync

## Purpose
Synchronizes LeetCode solution files (Python, Java, C++, etc.) into a structured Obsidian vault, maintaining consistent templates and linking.

## Detailed Implementation

### 1. Dynamic Path Resolution
- **Logic**: Implements a priority-based path resolution (Args -> Env -> Memory -> Default) to ensure that sensitive local paths are not hardcoded in the shared `SKILL.md`.

### 2. File Parsing
- **Method**: Regex Extraction.
- **Input**: Filename (e.g., `1.two-sum.py`).
- **Logic**: Extracts the problem ID, title, and file extension. Reads the file content to extract metadata (difficulty, tags) from comments.

### 3. Incremental Update
- **Method**: Markdown Merging.
- **Logic**: If the target `.md` file exists, it appends the new solution as a code block while preserving existing notes or older solutions.
