#!/usr/bin/env python3
"""Generate sourced academic concept notes for Obsidian."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.robotparser
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

try:
    import arxiv
except Exception:
    arxiv = None

try:
    import trafilatura
except Exception:
    trafilatura = None

try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None


USER_AGENT = "ObsidianAcademicConceptSkill/1.0 (+https://obsidian.md; academic note-taking)"
CACHE_DAYS = 7
REQUEST_INTERVAL_SECONDS = 3
MAX_PARAGRAPH_CHARS = 1200
MAX_QUOTE_CHARS = 900

TEXTBOOK_SEARCH_QUERIES = [
    "{query} site:deeplearningbook.org",
    "{query} site:d2l.ai",
    "{query} site:probml.github.io",
    "{query} site:stanford.edu textbook",
    "{query} site:mit.edu lecture notes",
]


@dataclass
class SourceParagraph:
    """A short source passage extracted from an academic source."""

    source_type: str
    title: str
    url: str
    text: str
    score: float = 0.0


@dataclass
class SearchResult:
    """Cached search result for a query."""

    query: str
    created_at: str
    paragraphs: List[SourceParagraph]


def now_date() -> str:
    """Return the current local date as YYYY-MM-DD."""

    return datetime.now().strftime("%Y-%m-%d")


def slugify_filename(name: str) -> str:
    """Convert a query into a safe Markdown filename stem."""

    safe = re.sub(r"[\\/:*?\"<>|]", " ", name).strip()
    safe = re.sub(r"\s+", " ", safe)
    return safe[:90] or "未命名概念"


def cache_key(query: str) -> str:
    """Return a stable short cache key for a query."""

    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()[:16]


def ensure_dir(path: Path) -> None:
    """Create a directory and all parents if missing."""

    path.mkdir(parents=True, exist_ok=True)


def tokenize(text: str) -> List[str]:
    """Tokenize English words, numbers, and CJK characters for ranking."""

    return re.findall(r"[a-zA-Z0-9_\-]+|[\u4e00-\u9fff]", text.lower())


def can_fetch(url: str) -> bool:
    """Best-effort robots.txt check."""

    try:
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        parser = urllib.robotparser.RobotFileParser()
        parser.set_url(robots_url)
        parser.read()
        return parser.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def polite_get(url: str, timeout: int = 20) -> Optional[str]:
    """Fetch a URL with a User-Agent, polite delay, and robots best effort."""

    if not can_fetch(url):
        return None
    try:
        time.sleep(REQUEST_INTERVAL_SECONDS)
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        if response.status_code >= 400:
            return None
        return response.text
    except Exception:
        return None


def ddg_search(query: str, max_results: int = 8) -> List[Tuple[str, str]]:
    """Search DuckDuckGo HTML and return (title, url) pairs."""

    try:
        time.sleep(REQUEST_INTERVAL_SECONDS)
        response = requests.post(
            "https://duckduckgo.com/html/",
            data={"q": query},
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        if response.status_code >= 400:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        results: List[Tuple[str, str]] = []
        for link in soup.select("a.result__a"):
            title = link.get_text(" ", strip=True)
            href = link.get("href") or ""
            if "uddg=" in href:
                parsed = urllib.parse.urlparse(href)
                href = urllib.parse.parse_qs(parsed.query).get("uddg", [href])[0]
            if title and href:
                results.append((title, href))
            if len(results) >= max_results:
                break
        return results
    except Exception:
        return []


def extract_text_from_url(url: str) -> str:
    """Extract readable text from a webpage."""

    html = polite_get(url)
    if not html:
        return ""
    if trafilatura is not None:
        try:
            extracted = trafilatura.extract(html, include_comments=False, include_tables=True)
            if extracted:
                return extracted
        except Exception:
            pass
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text("\n", strip=True)


def split_paragraphs(text: str) -> List[str]:
    """Split extracted text into useful medium-length paragraphs."""

    raw_parts = re.split(r"\n{2,}|(?<=[。！？.!?])\s+", text)
    paragraphs: List[str] = []
    for part in raw_parts:
        cleaned = re.sub(r"\s+", " ", part).strip()
        if 80 <= len(cleaned) <= MAX_PARAGRAPH_CHARS:
            paragraphs.append(cleaned)
    return paragraphs


def rank_paragraphs(query: str, paragraphs: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    """Rank paragraphs by relevance to the query."""

    if not paragraphs:
        return []
    if BM25Okapi is not None:
        corpus = [tokenize(paragraph) for paragraph in paragraphs]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(tokenize(query))
        ranked = sorted(zip(paragraphs, scores), key=lambda item: item[1], reverse=True)
        return [(paragraph, float(score)) for paragraph, score in ranked[:top_k]]
    query_tokens = set(tokenize(query))
    ranked_fallback: List[Tuple[str, float]] = []
    for paragraph in paragraphs:
        paragraph_tokens = set(tokenize(paragraph))
        score = len(query_tokens & paragraph_tokens) / max(1, len(query_tokens))
        ranked_fallback.append((paragraph, float(score)))
    return sorted(ranked_fallback, key=lambda item: item[1], reverse=True)[:top_k]


def search_textbook_sources(query: str) -> List[SourceParagraph]:
    """Search open textbook and educational pages."""

    passages: List[SourceParagraph] = []
    seen_urls: set[str] = set()
    for template in TEXTBOOK_SEARCH_QUERIES:
        for title, url in ddg_search(template.format(query=query), max_results=4):
            if url in seen_urls:
                continue
            seen_urls.add(url)
            page_text = extract_text_from_url(url)
            for paragraph, score in rank_paragraphs(query, split_paragraphs(page_text), top_k=3):
                passages.append(SourceParagraph("textbook", title, url, paragraph[:MAX_QUOTE_CHARS], score))
    return sorted(passages, key=lambda item: item.score, reverse=True)[:9]


def search_arxiv_sources(query: str) -> List[SourceParagraph]:
    """Search arXiv and return abstracts as source passages."""

    if arxiv is None:
        return []
    passages: List[SourceParagraph] = []
    try:
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=6, sort_by=arxiv.SortCriterion.Relevance)
        for paper in client.results(search):
            summary = re.sub(r"\s+", " ", paper.summary).strip()
            if summary:
                passages.append(SourceParagraph("arxiv", paper.title, paper.entry_id, summary[:MAX_QUOTE_CHARS], 1.0))
    except Exception:
        return []
    return passages


def search_edu_lectures(query: str) -> List[SourceParagraph]:
    """Search university lecture notes on .edu domains."""

    passages: List[SourceParagraph] = []
    for title, url in ddg_search(f"{query} lecture notes site:.edu", max_results=8):
        page_text = extract_text_from_url(url)
        for paragraph, score in rank_paragraphs(query, split_paragraphs(page_text), top_k=3):
            passages.append(SourceParagraph("lecture", title, url, paragraph[:MAX_QUOTE_CHARS], score))
    return sorted(passages, key=lambda item: item.score, reverse=True)[:9]


def search_google_scholar_optional(query: str, enabled: bool) -> List[SourceParagraph]:
    """Optionally search Google Scholar via scholarly; disabled by default."""

    if not enabled:
        return []
    try:
        from scholarly import scholarly  # type: ignore
    except Exception:
        return []
    passages: List[SourceParagraph] = []
    try:
        iterator = scholarly.search_pubs(query)
        for _ in range(3):
            publication = next(iterator)
            bib = publication.get("bib", {})
            title = bib.get("title", "Google Scholar result")
            abstract = bib.get("abstract", "")
            url = publication.get("pub_url", "")
            if abstract:
                passages.append(SourceParagraph("scholar", title, url, abstract[:MAX_QUOTE_CHARS], 1.0))
            time.sleep(REQUEST_INTERVAL_SECONDS)
    except Exception:
        pass
    return passages


def search_sources(query: str, use_scholar: bool = False) -> List[SourceParagraph]:
    """Search all configured source types and deduplicate passages."""

    all_passages: List[SourceParagraph] = []
    all_passages.extend(search_textbook_sources(query))
    all_passages.extend(search_arxiv_sources(query))
    all_passages.extend(search_edu_lectures(query))
    all_passages.extend(search_google_scholar_optional(query, use_scholar))
    seen: set[str] = set()
    deduped: List[SourceParagraph] = []
    for passage in all_passages:
        digest = hashlib.md5((passage.url + passage.text[:160]).encode("utf-8")).hexdigest()
        if digest not in seen:
            seen.add(digest)
            deduped.append(passage)
    return deduped


def load_or_search(query: str, cache_dir: Path, use_scholar: bool) -> SearchResult:
    """Load cached results when fresh, otherwise search online."""

    ensure_dir(cache_dir)
    cache_path = cache_dir / f"{cache_key(query)}.json"
    if cache_path.exists():
        try:
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            created_at = datetime.fromisoformat(data["created_at"])
            if datetime.now() - created_at < timedelta(days=CACHE_DAYS):
                return SearchResult(
                    query=data["query"],
                    created_at=data["created_at"],
                    paragraphs=[SourceParagraph(**item) for item in data["paragraphs"]],
                )
        except Exception:
            pass
    result = SearchResult(query=query, created_at=datetime.now().isoformat(), paragraphs=search_sources(query, use_scholar))
    cache_path.write_text(
        json.dumps(
            {
                "query": result.query,
                "created_at": result.created_at,
                "paragraphs": [asdict(paragraph) for paragraph in result.paragraphs],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return result


def extract_definition(query: str, paragraphs: List[SourceParagraph]) -> Optional[SourceParagraph]:
    """Select a definition-like passage, preferring textbook sources."""

    definition_patterns = [r"\bis defined as\b", r"\brefers to\b", r"\bis\b", r"定义", r"是指", r"指的是"]
    candidates = sorted(paragraphs, key=lambda item: (0 if item.source_type == "textbook" else 1, -item.score))
    for paragraph in candidates:
        sentences = re.split(r"(?<=[。！？.!?])\s+", paragraph.text)
        for sentence in sentences:
            if query.lower() in sentence.lower() or any(re.search(pattern, sentence, re.I) for pattern in definition_patterns):
                if 40 <= len(sentence) <= MAX_QUOTE_CHARS:
                    return SourceParagraph(paragraph.source_type, paragraph.title, paragraph.url, sentence.strip(), paragraph.score)
    return candidates[0] if candidates else None


def group_paragraphs(paragraphs: Iterable[SourceParagraph]) -> Dict[str, List[SourceParagraph]]:
    """Group passages into concept-note sections."""

    groups: Dict[str, List[SourceParagraph]] = {"背景": [], "数学形式": [], "变体与相关概念": [], "应用": [], "对比与限制": []}
    for paragraph in paragraphs:
        text = paragraph.text.lower()
        if any(keyword in text for keyword in ["equation", "formula", "matrix", "probability", "公式", "矩阵"]):
            groups["数学形式"].append(paragraph)
        elif any(keyword in text for keyword in ["application", "used in", "applied", "应用", "用于"]):
            groups["应用"].append(paragraph)
        elif any(keyword in text for keyword in ["variant", "extension", "related", "变体", "相关"]):
            groups["变体与相关概念"].append(paragraph)
        elif any(keyword in text for keyword in ["however", "limitation", "compared", "contrast", "限制", "相比"]):
            groups["对比与限制"].append(paragraph)
        else:
            groups["背景"].append(paragraph)
    return groups


def infer_tags(query: str, paragraphs: List[SourceParagraph]) -> List[str]:
    """Infer a small set of Obsidian tags from query and source text."""

    merged = (query + " " + " ".join(paragraph.text for paragraph in paragraphs[:10])).lower()
    tags = ["概念解释"]
    mapping = {
        "大模型": ["transformer", "attention", "llm", "language model", "self-attention"],
        "机器学习": ["machine learning", "classification", "regression", "supervised"],
        "深度学习": ["neural", "deep learning", "gradient", "backpropagation"],
        "统计学习": ["statistical", "bayesian", "probability", "estimator"],
        "计算机视觉": ["vision", "image", "cnn", "segmentation"],
        "自然语言处理": ["nlp", "language", "token", "embedding"],
    }
    for tag, keywords in mapping.items():
        if any(keyword in merged for keyword in keywords):
            tags.append(tag)
    return list(dict.fromkeys(tags))


def collect_existing_concepts(existing_notes_dir: Path) -> Dict[str, str]:
    """Collect existing Markdown note stems for wikilinking."""

    concepts: Dict[str, str] = {}
    if not existing_notes_dir.exists():
        return concepts
    for note_path in existing_notes_dir.rglob("*.md"):
        concepts[note_path.stem.lower()] = note_path.stem
    return concepts


def wikilink_known_concepts(markdown: str, existing_notes_dir: Path, current_title: str) -> str:
    """Convert known concept mentions into Obsidian wikilinks."""

    concepts = collect_existing_concepts(existing_notes_dir)
    for _, title in sorted(concepts.items(), key=lambda item: len(item[0]), reverse=True):
        if title == current_title:
            continue
        pattern = re.compile(rf"(?<!\[\[)({re.escape(title)})(?!\]\])", re.I)
        markdown = pattern.sub(r"[[\1]]", markdown)
    return markdown


def unique_note_path(base_dir: Path, title: str) -> Path:
    """Return a non-conflicting note path, adding _vN when needed."""

    ensure_dir(base_dir)
    candidate = base_dir / f"{slugify_filename(title)}.md"
    if not candidate.exists():
        return candidate
    version = 2
    while True:
        candidate = base_dir / f"{slugify_filename(title)}_v{version}.md"
        if not candidate.exists():
            return candidate
        version += 1


def build_note(query: str, result: SearchResult, existing_notes_dir: Path) -> Tuple[str, str]:
    """Build the Markdown concept note body."""

    title = slugify_filename(query)
    paragraphs = result.paragraphs
    definition = extract_definition(query, paragraphs)
    groups = group_paragraphs(paragraphs)
    tags = infer_tags(query, paragraphs)
    ref_by_key: Dict[str, str] = {}
    for index, paragraph in enumerate(paragraphs, start=1):
        ref_by_key[paragraph.url + paragraph.text[:40]] = f"ref{index}"
    lines: List[str] = ["---", f"title: {title}", f"created: {now_date()}", f"source_count: {len(paragraphs)}", "tags:"]
    lines.extend([f"  - {tag}" for tag in tags])
    lines.extend(["---", "", f"# {title}", "", "## 定义", "", "> [!info] 定义"])
    if definition:
        ref = ref_by_key.get(definition.url + definition.text[:40], "ref1")
        lines.append(f"> {definition.text} ^[{ref}]")
    else:
        lines.append("> 未能从公开来源中可靠提取定义句。")
    lines.append("")
    for section, section_paragraphs in groups.items():
        if not section_paragraphs:
            continue
        lines.extend([f"## {section}", ""])
        for paragraph in section_paragraphs[:5]:
            ref = ref_by_key.get(paragraph.url + paragraph.text[:40], "")
            lines.append(f"- {paragraph.text} ^[{ref}]")
        lines.append("")
    lines.extend(["## 参考文献", ""])
    for index, paragraph in enumerate(paragraphs, start=1):
        lines.append(f"- ^ref{index} **{paragraph.title}** ({paragraph.source_type})：{paragraph.url}")
    markdown = "\n".join(lines)
    return title, wikilink_known_concepts(markdown, existing_notes_dir, title)


def update_moc(moc_file: Path, note_title: str) -> None:
    """Append a note link to a MOC file, keeping link entries sorted."""

    ensure_dir(moc_file.parent)
    link_line = f"- [[{note_title}]]"
    if moc_file.exists():
        lines = moc_file.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["# 术语表", ""]
    if any(link_line == line.strip() for line in lines):
        return
    entries = [line.strip() for line in lines if line.strip().startswith("- [[")]
    body = [line for line in lines if not line.strip().startswith("- [[")]
    entries.append(link_line)
    entries = sorted(set(entries), key=lambda line: line.lower())
    moc_file.write_text("\n".join(body).rstrip() + "\n\n" + "\n".join(entries) + "\n", encoding="utf-8")


def update_related_papers(existing_notes_dir: Path, concept_title: str, source_titles: List[str]) -> int:
    """Append a related concept link to likely matching paper notes."""

    candidate_dirs = [existing_notes_dir / "Papers", existing_notes_dir.parent / "Papers", existing_notes_dir.parent / "20_Research" / "Papers"]
    paper_notes: List[Path] = []
    for directory in candidate_dirs:
        if directory.exists():
            paper_notes.extend(directory.rglob("*.md"))
    keywords: set[str] = set()
    for source_title in source_titles:
        keywords.update(token for token in tokenize(source_title) if len(token) >= 5)
    updated = 0
    link = f"[[{concept_title}]]"
    for note_path in paper_notes:
        text = note_path.read_text(encoding="utf-8", errors="ignore")
        haystack = (note_path.stem + " " + text[:2000]).lower()
        if link in text or not any(keyword in haystack for keyword in keywords):
            continue
        note_path.write_text(text.rstrip() + f"\n\n## 相关概念\n\n- {link}\n", encoding="utf-8")
        updated += 1
    return updated


def run(query: str, existing_notes_dir: str, moc_file: Optional[str], cache_dir: Optional[str], use_scholar: bool) -> Dict[str, object]:
    """Run the full note-generation workflow and return JSON-serializable output."""

    if not query or not query.strip():
        return {"success": False, "note_path": "", "message": "query 不能为空。"}
    notes_dir = Path(existing_notes_dir).expanduser().resolve()
    cache_path = Path(cache_dir).expanduser().resolve() if cache_dir else notes_dir / "cache"
    result = load_or_search(query.strip(), cache_path, use_scholar)
    if not result.paragraphs:
        return {"success": False, "note_path": "", "message": "未检索到足够可信的公开学术来源，请更换关键词或稍后重试。"}
    title, markdown = build_note(query.strip(), result, notes_dir)
    note_path = unique_note_path(notes_dir, title)
    note_path.write_text(markdown, encoding="utf-8")
    if moc_file:
        update_moc(Path(moc_file).expanduser().resolve(), note_path.stem)
    related_count = update_related_papers(notes_dir, note_path.stem, [paragraph.title for paragraph in result.paragraphs])
    return {"success": True, "note_path": str(note_path), "message": f"已生成概念笔记；更新相关论文笔记 {related_count} 篇。"}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Generate sourced academic concept notes for Obsidian.")
    parser.add_argument("--query", type=str, default="")
    parser.add_argument("--existing-notes-dir", type=str, default="./Concepts")
    parser.add_argument("--moc-file", type=str, default="")
    parser.add_argument("--cache-dir", type=str, default="")
    parser.add_argument("--use-scholar", action="store_true")
    parser.add_argument("--stdin-json", action="store_true")
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""

    args = parse_args()
    if args.stdin_json:
        payload = json.load(sys.stdin)
        query = str(payload.get("query", ""))
        existing_notes_dir = str(payload.get("existing_notes_dir", "./Concepts"))
        moc_file = str(payload.get("moc_file", ""))
        cache_dir = str(payload.get("cache_dir", ""))
        use_scholar = bool(payload.get("use_scholar", False))
    else:
        query = args.query
        existing_notes_dir = args.existing_notes_dir
        moc_file = args.moc_file
        cache_dir = args.cache_dir
        use_scholar = args.use_scholar
    output = run(query=query, existing_notes_dir=existing_notes_dir, moc_file=moc_file or None, cache_dir=cache_dir or None, use_scholar=use_scholar)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
