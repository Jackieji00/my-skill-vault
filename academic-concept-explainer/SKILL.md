---
name: academic-concept-explainer
description: Online academic concept explainer for Obsidian. Use when the user selects a term or asks a technical/research question and wants a sourced Markdown concept note generated from public academic sources such as open textbooks, arXiv papers, and university lecture notes, with Obsidian frontmatter, wikilinks, tags, MOC updates, caching, and no dependency on a local paper library or external LLM API.
---

# Academic Concept Explainer

## Purpose

Generate a sourced Obsidian concept note for a selected term or question using public academic sources only. The skill is designed for users who read papers and want quick, citation-backed explanations inserted into their knowledge graph.

## Primary workflow

1. Read the user's `query` from their request.
2. Resolve output paths:
   - Default concept directory: user-provided `existing_notes_dir`, otherwise `Concepts/`.
   - Optional MOC file: user-provided `moc_file`.
3. Run `scripts/academic_concept_explainer.py`.
4. Return the JSON result from the script, especially `success`, `note_path`, and `message`.
5. If the script reports no reliable sources, do not invent an explanation; tell the user to refine the query.
6. When answering the user in chat, include the corresponding English technical term and at least one source link whenever a concept explanation is given.
7. Prefer university/course/textbook sources over arXiv. Use arXiv only when textbook and university lecture sources do not provide enough relevant passages.

## Script

Use the bundled script:

```bash
python academic-concept-explainer/scripts/academic_concept_explainer.py \
  --query "自注意力机制" \
  --existing-notes-dir "/path/to/ObsidianVault/Concepts" \
  --moc-file "/path/to/ObsidianVault/术语表.md"
```

JSON input is also supported:

```bash
echo '{"query":"Transformer 的位置编码是如何工作的？","existing_notes_dir":"./Concepts","moc_file":"./术语表.md"}' \
  | python academic-concept-explainer/scripts/academic_concept_explainer.py --stdin-json
```

## What the script does

- Searches online sources in this order:
  1. Open textbooks and high-quality educational pages.
  2. `.edu` university lecture notes.
  3. arXiv papers only if the first two source types provide fewer than 3 relevant passages.
  4. Google Scholar only if explicitly enabled with `--use-scholar`.
- Extracts short relevant passages and ranks them with BM25 when available.
- Selects a definition-like sentence preferentially from textbook sources.
- Builds a Markdown note with:
  - YAML frontmatter.
  - A `## 术语 / English Terms` section containing Chinese term, English technical term, and aliases.
  - `> [!info]` definition block.
  - Background, mathematical form, variants, applications, and limitations sections when evidence exists.
  - Obsidian footnote-style source markers after source-backed passages.
  - A reference list with clickable Markdown links for every cited source.
- Converts known existing concept names into Obsidian wikilinks when matching files exist in `existing_notes_dir`.
- Appends the new concept to `moc_file` when provided.
- Caches query results for 7 days under `cache/`.

## Output note conventions

Each generated note should contain frontmatter like:

```yaml
---
title: 自注意力机制
created: 2026-06-12
source_count: 8
tags:
  - 概念解释
  - 大模型
---
```

Do not create unsourced explanatory prose outside the script's extracted and lightly organized source passages. If summarization is needed, keep it conservative and explicitly source-backed.

## Citation and terminology requirements

Every generated note must make citation and terminology visible:

- Use bilingual section headings, such as `## 定义 / Definition` and `## 背景 / Background`.
- Include the likely English technical term near the top of the note.
- Preserve the original user query as the Chinese/display term.
- Put a citation marker such as `^[ref1]` after every extracted explanatory passage.
- In `## 参考文献`, use clickable links: `[Source Title](https://...)`.
- For every source passage, keep the original excerpt and add a short Chinese reading cue when possible. The reading cue must stay conservative and must not introduce claims beyond the cited passage.
- If the agent gives a short explanation directly in chat instead of only returning the note path, the chat answer must include:
  - Chinese term.
  - English term.
  - 1-3 sentence explanation.
  - At least one source link.

## Dependencies

Install:

```bash
pip install arxiv requests beautifulsoup4 trafilatura rank-bm25
```

Optional:

```bash
pip install scholarly
```

## Safety and source rules

- Use only publicly reachable sources.
- Respect polite request intervals and `robots.txt` checks where possible.
- Use a clear User-Agent.
- Keep quoted passages short; do not reproduce entire articles, chapters, or papers.
- If Google Scholar is enabled, warn that it is rate-limit prone and may fail.
- Never require an external LLM API.
