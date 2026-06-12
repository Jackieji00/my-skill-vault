# Project Work Log

[2026-06-12 20:32] | academic-concept-explainer/ | Updated source priority to prefer textbooks and university lecture notes before arXiv, and changed generated concept notes to use bilingual section headings, English technical terms, citations, and clickable source links.
[2026-06-12 20:20] | academic-concept-explainer/ | Added explicit English technical term output and clickable citation-link requirements to the skill and note generator.
[2026-06-12 20:12] | academic-concept-explainer/scripts/academic_concept_explainer.py | Improved bilingual query expansion for mixed Chinese/English terms such as actor-critic 多智能体 and strengthened definition passage ranking.
[2026-06-12 20:05] | academic-concept-explainer/scripts/academic_concept_explainer.py | Fixed Windows console Unicode output by forcing stdout/stderr to UTF-8 before printing JSON results.
[2026-06-12 19:55] | academic-concept-explainer/ / .resource-index | Added the academic concept explainer skill with an executable Python runner, dependency list, OpenAI skill metadata, and resource index entries.
[2026-06-11 19:45] | Root | Standardized test outputs. Created `test-outputs/` folder and updated `.gitignore` and `requirements.md` to prevent local test files from being committed.
[2026-06-11 19:35] | universal-video-note-taker/ | Successfully installed Python dependencies (ffmpeg-python, future, etc.) for the video processing engine.
[2026-06-11 19:10] | universal-video-note-taker/ | Performed a test run on a Xiaohongshu video URL. Verified the Cornell-style template and AI extraction logic. Note generated for user review.
[2026-06-11 19:00] | universal-video-note-taker/ | Created a new universal video note-taking skill. Supports multi-platform, AI-driven keyframe extraction, and Cornell notes. Integrated it into morning-routine.
[2026-06-11 18:40] | leetcode-sync/ | Refactored skill to use dynamic variables for paths, protecting local privacy. Added WORK_LOG.md and EXPLANATIONS.md for the skill.
[2026-06-11 18:35] | .gitignore | Added .gemini/ and other temporary directories to untrack local configurations and skill packages.
[2026-06-11 18:20] | AGENTS.md | Created AGENTS.md to define core behavioral rules, logging standards, and the Plan-Confirm-Execute workflow.
[2026-06-11 18:05] | morning-routine/SKILL.md | Optimized video transcription logic by introducing readable pseudocode and logic flows.
[2026-06-11 17:55] | skills/obsidian-pdf-organizer/ | Refactored skill into "Instruction Librarian" with a hierarchical rule system (Global Requirements vs. Folder Guide).
[2026-06-11 17:20] | skills/obsidian-pdf-organizer/ | Initialized obsidian-pdf-organizer skill for automated PDF management in Obsidian.
[2026-06-05] | Project Root | Initial project setup and creation of early skills (morning-routine, leetcode-sync).
