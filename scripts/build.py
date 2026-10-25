#!/usr/bin/env python3
"""Build the book and reject broken local links. Run from any directory."""

from html import escape, unescape
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit, urlunsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
REQUIRED = ["book.md", "chapters/01-why-metadata.md",
            "chapters/02-reading-a-database.md", "chapters/03-following-lineage.md"]


def destination(source):
    return Path("index.html") if source == Path("book.md") else source.with_suffix(".html")


def relative(target, page):
    return Path(os.path.relpath(target, page.parent)).as_posix()


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


def build():
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing required source: {name}")
    sources = [Path("book.md"), *sorted(p.relative_to(ROOT) for p in (ROOT / "chapters").glob("*.md"))]
    if (ROOT / "examples").exists():
        sources.extend(sorted(p.relative_to(ROOT) for p in (ROOT / "examples").rglob("*.md")))
    content = {source: read_source(source) for source in sources}
    book_title = content[Path("book.md")][0]
    chapters = [p for p in sources if p.parent == Path("chapters")]
    reading_order = [Path("book.md"), *chapters]
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    shutil.copy2(ROOT / "assets/book.css", OUT / "assets/book.css")
    if (ROOT / "examples").exists():
        shutil.copytree(ROOT / "examples", OUT / "examples")
    for source, (title, text) in content.items():
        page = destination(source)
        converter = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "sane_lists"],
                                      extension_configs={"toc": {"toc_depth": "2-3"}})
        body = converter.convert(text)
        body = re.sub(r'\b(href|src)="([^"]*)"', rewrite_link, body)
        body = body.replace("<pre>", '<pre tabindex="0" role="region" aria-label="Code example">')
        body = body.replace("<table>", '<div class="table-scroll" role="region" aria-label="Data table" tabindex="0"><table>')
        body = body.replace("</table>", "</table></div>")
        nav = []
        for item in reading_order:
            active = ' aria-current="page"' if item == source else ""
            label = "Introduction" if item == Path("book.md") else content[item][0]
            nav.append(f'<li><a href="{escape(relative(destination(item), page))}"{active}>{escape(label)}</a></li>')
        pagination = []
        if source in reading_order:
            index = reading_order.index(source)
            for offset, label in [(-1, "Previous"), (1, "Next")]:
                if 0 <= index + offset < len(reading_order):
                    item = reading_order[index + offset]
                    pagination.append(f'<a rel="{label.lower()}" href="{relative(destination(item), page)}"><span>{label}</span>{escape(content[item][0])}</a>')
        description = f"{title}. Read {book_title}, a practical guide to understanding data through its metadata."
        toc = f'<details class="page-contents" open><summary>On this page</summary>{converter.toc}</details>' if converter.toc_tokens else ""
        html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="color-scheme" content="light dark">
  <title>{escape(title)} · {escape(book_title)}</title>
  <link rel="stylesheet" href="{relative(Path('assets/book.css'), page)}">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a href="{relative(Path('index.html'), page)}">{escape(book_title)}</a><span>A practical book about data</span></header>
<div class="book-layout">
  <aside class="book-sidebar"><details class="chapter-menu" open><summary>Contents</summary><nav aria-label="Book chapters"><ol>{''.join(nav)}</ol></nav></details></aside>
  <main id="main" tabindex="-1">
    <article><header class="chapter-header"><p class="eyebrow">{'Introduction' if source == Path('book.md') else 'The book'}</p><h1>{escape(title)}</h1></header>
    {toc}
    <div class="prose">{body}</div>
    </article>
    <nav class="pagination" aria-label="Continue reading">{''.join(pagination)}</nav>
    <footer class="page-footer"><a href="https://github.com/snowch/metadata-book">Source on GitHub</a></footer>
  </main>
</div>
</body>
</html>
'''
        (OUT / page).parent.mkdir(parents=True, exist_ok=True)
        (OUT / page).write_text(html, encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Built {check_links()} pages in {OUT}; all local links and anchors resolve.")


if __name__ == "__main__":
    try:
        build()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
