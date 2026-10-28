#!/usr/bin/env python3
"""Build the book and reject broken local links. Run from any directory."""

from html import escape, unescape
from html.parser import HTMLParser
import os
import json
import hashlib
import math
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit, urlunsplit

import markdown

from metadata_map import render_map

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
REQUIRED = ["book.md", "metadata-map.md", "chapters/01-why-metadata.md",
            "chapters/02-reading-a-database.md", "chapters/03-following-lineage.md",
            "chapters/04-outdated-reports.md", "chapters/05-collecting-metadata.md",
            "chapters/06-unreliable-records.md", "chapters/07-using-metadata.md",
            "chapters/08-choosing-a-platform.md", "chapters/09-sharing-metadata.md",
            "chapters/10-managing-changes.md", "chapters/11-access-and-reuse.md"]
REDIRECTS = {
    "chapters/04-collecting-metadata.html": "chapters/05-collecting-metadata.html",
    "chapters/05-unreliable-records.html": "chapters/06-unreliable-records.html",
    "chapters/06-using-metadata.html": "chapters/07-using-metadata.html",
    "chapters/07-choosing-a-platform.html": "chapters/08-choosing-a-platform.html",
    "examples/lineage/walkthrough.html": "chapters/03-following-lineage.html",
}


def destination(source):
    return Path("index.html") if source == Path("book.md") else source.with_suffix(".html")


def relative(target, page):
    return Path(os.path.relpath(target, page.parent)).as_posix()


def asset_url(path, page):
    """Change asset URLs with their contents so readers receive matching styles/code."""
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    return f"{relative(Path(path), page)}?v={digest}"


def rewrite_link(match):
    value = urlsplit(unescape(match.group(2)))
    path = value.path
    if not value.scheme and not value.netloc and path.endswith(".md"):
        path = str(Path(path).with_suffix(".html"))
        if Path(value.path).name == "book.md":
            path = str(Path(path).with_name("index.html"))
    return f'{match.group(1)}="{escape(urlunsplit(value._replace(path=path)), quote=True)}"'


def read_source(source):
    text = (ROOT / source).read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Empty source: {source}")
    heading = re.search(r"^# (.+)$", text, re.MULTILINE)
    if not heading:
        raise ValueError(f"Source needs a level-one title: {source}")
    return heading.group(1).strip(), text[:heading.start()] + text[heading.end():]


def clean_title(title):
    return re.sub(r"^\d+\.\s+", "", title)


class ReadingText(HTMLParser):
    """Count the core reading text, excluding optional detail and code."""

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.words = 0
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        if tag in ("details", "pre"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("details", "pre"):
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.words += len(re.findall(r"\b[\w’'-]+\b", data))


BOOK_MARK = '''<svg class="brand-mark" width="28" height="32" viewBox="0 0 28 32" fill="none" aria-hidden="true"><path d="M2 5 14 2l12 3v22l-12 3-12-3V5Z" stroke="currentColor" stroke-width="1.5"/><path d="m2 5 12 3 12-3M14 8v22M7 12l4 1m-4 4 4 1m6-5 4-1m-4 6 4-1" stroke="currentColor" stroke-width="1.5"/></svg>'''


LINK_ARROW = '<svg class="external-arrow" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="m3 9 6-6M3 3h6v6" stroke="currentColor" stroke-width="1.2"/></svg>'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


def check_links():
    documents = {p: Document(p.read_text(encoding="utf-8")) for p in OUT.rglob("*.html")}
    errors = []
    for page, document in documents.items():
        for link in document.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(OUT) or not target.is_file():
                errors.append(f"{page.relative_to(OUT)}: missing local target {link}")
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                errors.append(f"{page.relative_to(OUT)}: missing anchor {link}")
    if errors:
        raise ValueError("Broken links:\n" + "\n".join(errors))
    return len(documents)


def write_redirects():
    for old, new in REDIRECTS.items():
        page = Path(old)
        target = escape(relative(Path(new), page), quote=True)
        html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>Page moved · Metadata systems</title>
</head>
<body>
  <main><h1>This page has moved</h1><p><a href="{target}">Continue to the updated page</a>.</p></main>
</body>
</html>
'''
        (OUT / page).parent.mkdir(parents=True, exist_ok=True)
        (OUT / page).write_text(html, encoding="utf-8")


def build():
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing required source: {name}")
    sources = [Path("book.md"), Path("metadata-map.md"), *sorted(p.relative_to(ROOT) for p in (ROOT / "chapters").glob("*.md"))]
    if (ROOT / "examples").exists():
        sources.extend(sorted(p.relative_to(ROOT) for p in (ROOT / "examples").rglob("*.md")))
    content = {source: read_source(source) for source in sources}
    book_title = content[Path("book.md")][0]
    chapters = [p for p in sources if p.parent == Path("chapters")]
    reading_order = [Path("book.md"), *chapters]
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    if (ROOT / "examples").exists():
        shutil.copytree(ROOT / "examples", OUT / "examples",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for source, (title, text) in content.items():
        page = destination(source)
        converter = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "sane_lists", "md_in_html"],
                                      extension_configs={"toc": {"toc_depth": "2-3"}})
        body = converter.convert(text)
        is_map = source == Path("metadata-map.md")
        if is_map:
            map_data = json.loads((ROOT / "assets/metadata-map.json").read_text())
            map_data["layout"] = json.loads((ROOT / "assets/metadata-map-layout.json").read_text())
            body += render_map(map_data)
        body = re.sub(r'\b(href|src)="([^"]*)"', rewrite_link, body)
        reading_time = max(1, math.ceil(ReadingText(body).words / 220))
        body = body.replace("<pre>", '<pre tabindex="0" role="region" aria-label="Code example">')
        body = re.sub(r'(<pre\b[^>]*><code class="language-sql">.*?</code></pre>)',
                      r'<div class="code-example"><div class="code-label" aria-hidden="true">SQL</div>\1</div>',
                      body, flags=re.DOTALL)
        body = body.replace("<table>", '<div class="table-scroll" role="region" aria-label="Data table" tabindex="0"><table>')
        body = body.replace("</table>", "</table></div>")
        nav = []
        for number, item in enumerate(reading_order):
            active = ' aria-current="page"' if item == source else ""
            label = "Introduction" if item == Path("book.md") else clean_title(content[item][0])
            nav_number = f'{number:02}' if number else '—'
            nav.append(f'<li><a href="{escape(relative(destination(item), page))}"{active}><span class="nav-number">{nav_number}</span><span class="nav-title">{escape(label)}</span></a></li>')
        pagination = []
        if source in reading_order:
            index = reading_order.index(source)
            for offset, label in [(-1, "Previous"), (1, "Next")]:
                if 0 <= index + offset < len(reading_order):
                    item = reading_order[index + offset]
                    caption = "START READING" if index == 0 else f"{label.upper()} CHAPTER"
                    if item == Path("book.md"):
                        caption = "INTRODUCTION"
                    arrow = "←" if offset < 0 else "→"
                    pagination.append(f'<a class="pagination-{label.lower()}" rel="{label.lower()}" href="{relative(destination(item), page)}"><span class="pagination-label">{caption}</span><span class="pagination-title">{escape(clean_title(content[item][0]))}<span class="pagination-arrow" aria-hidden="true">{arrow}</span></span></a>')
        description = f"{title}. Read {book_title}, a practical guide to understanding data through its metadata."
        toc = f'<details class="page-contents"><summary>On this page</summary>{converter.toc}</details>' if converter.toc_tokens and not is_map else ""
        page_type = "map" if is_map else "introduction" if source == Path("book.md") else "chapter" if source in chapters else "reference"
        chapter_number = f'{chapters.index(source) + 1:02}' if source in chapters else ""
        chapter_meta = f"CHAPTER {chapter_number}" if chapter_number else "A PRACTICAL GUIDE" if page_type == "introduction" else "REFERENCE"
        decoration = f'<span class="chapter-number" aria-hidden="true">{chapter_number}</span>' if chapter_number else ""
        map_href = relative(Path("metadata-map.html"), page)
        if source in chapters:
            map_href += f"?chapter={chapters.index(source) + 1}"
        if is_map:
            map_href = relative(Path('index.html'), page) + '#contents'
        map_current = ' aria-label="Close metadata map" title="Close metadata map"' if is_map else ''
        map_close = '<span aria-hidden="true"> ×</span>' if is_map else ''
        map_assets = (
            f'<link rel="stylesheet" href="{asset_url("assets/metadata-map.css", page)}">'
            f'<script defer src="{asset_url("assets/metadata-map-arrows.js", page)}"></script>'
            f'<script defer src="{asset_url("assets/metadata-map.js", page)}"></script>'
        ) if is_map else ""
        if is_map:
            chapter_meta = "VISUAL INDEX"
        sidebar = "" if is_map else (
            f'<aside class="book-sidebar"><p class="sidebar-label">THE BOOK</p>'
            f'<p class="sidebar-title">{escape(book_title)}</p>'
            f'<nav aria-label="Book chapters"><ol>{"".join(nav)}</ol></nav></aside>'
        )
        reading_badge = "" if is_map else f'<span class="meta-separator" aria-hidden="true">/</span><span class="reading-time">{reading_time} min read</span>'
        html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="color-scheme" content="light dark">
  <title>{escape(title)} · {escape(book_title)}</title>
  <link rel="icon" type="image/svg+xml" href="{relative(Path('assets/favicon.svg'), page)}">
  <link rel="stylesheet" href="{asset_url('assets/book.css', page)}">
  {map_assets}
</head>
<body class="page-{page_type}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="{relative(Path('index.html'), page)}">{BOOK_MARK}<span class="brand-name">{escape(book_title)}</span></a><span class="header-note">A field guide to data</span><a class="header-map" href="{escape(map_href, quote=True)}"{map_current}>Metadata map{map_close}</a><a class="header-link" href="{relative(Path('index.html'), page)}#contents">Contents {LINK_ARROW}</a></header>
<details class="mobile-contents"><summary>Contents</summary><nav aria-label="Book chapters on mobile"><ol>{''.join(nav)}</ol></nav></details>
<div class="book-layout">
  {sidebar}
  <main id="main" tabindex="-1">
    <article><header class="chapter-header">{decoration}<p class="chapter-meta"><span>{chapter_meta}</span>{reading_badge}</p><h1>{escape(clean_title(title))}</h1></header>
    {toc}
    <div class="prose">{body}</div>
    </article>
    <nav class="pagination" aria-label="Continue reading">{''.join(pagination)}</nav>
    <footer class="page-footer"><span>{escape(book_title)}</span><a href="https://github.com/snowch/metadata-book">Source on GitHub {LINK_ARROW}</a></footer>
  </main>
</div>
</body>
</html>
'''
        (OUT / page).parent.mkdir(parents=True, exist_ok=True)
        (OUT / page).write_text(html, encoding="utf-8")
    write_redirects()
    (OUT / ".nojekyll").touch()
    print(f"Built {check_links()} pages in {OUT}; all local links and anchors resolve.")


if __name__ == "__main__":
    try:
        build()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
