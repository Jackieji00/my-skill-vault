# Skill Explanation: Instruction Librarian

## Purpose
Transforms unorganized PDF manuals in a `_Pending/` folder into structured, tagged, and summarized knowledge assets within the `说明书/` directory.

## Detailed Implementation

### 1. Hierarchical Rule Check
- **Method**: `Pre-check Logic`.
- **Input**: `/requirements.md` (Global) and `/说明书/_Guide.md` (Local).
- **Logic**: Prioritizes "taboos" and global sync rules from the root first, then applies local classification and naming rules from the sub-folder guide.

### 2. Multi-modal PDF Analysis
- **Method**: `AI Extraction`.
- **Input**: PDF files in `_Pending/`.
- **Logic**: Uses AI vision/text extraction to identify **Brand**, **Model**, and **Category**. Generates a functional summary (Reset, Maintenance, Features).

### 3. Organized Archiving
- **Method**: `Move & Rename`.
- **Logic**: 
    1. Renames PDF to `[Brand]-[Model]-Manual.pdf`.
    2. Moves PDF to its respective folder (e.g., `说明书/Digital/Apple/`).
    3. Generates a matching `.md` file containing an embedded PDF link and the AI summary.

### 4. Status Tracking
- **Output**: Entries in `HomePage.md` reporting which manuals were processed today.
