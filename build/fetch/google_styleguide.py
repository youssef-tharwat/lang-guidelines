#!/usr/bin/env python3
# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Convert a Google style guide HTML page into the Markdown source the compiler parses.

    curl -sfL https://google.github.io/styleguide/tsguide.html -o tsguide.html
    python3 build/fetch/google_styleguide.py tsguide.html > sources/typescript/google-typescript-style-guide.md

Each heading is preceded by ``<a id="..."></a>`` with the page's own anchor, and each example
is labelled ``✅ Good:`` or ``❌ Bad:`` from the page's good/bad markers (``language-ts good``
classes, or kramdown ``goodcode``/``badcode`` divs). Navigation, scripts and the table of
contents are dropped; everything else is kept.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

VOID_TAGS = frozenset({"meta", "link", "br", "img", "hr", "input"})
SKIPPED_TAGS = frozenset({"script", "style", "head", "nav"})
HEADING_TAGS = {f"h{level}": level for level in range(1, 7)}
LABELS = {"good": "✅ Good:", "goodcode": "✅ Good:", "bad": "❌ Bad:", "badcode": "❌ Bad:"}
LANGUAGE_RE = re.compile(r"language-\.?(?P<language>[\w-]+)")
WHITESPACE_RE = re.compile(r"\s+")
BLANK_RUN_RE = re.compile(r"\n{3,}")


@dataclass
class Node:
    """An element and its children (elements or text)."""

    tag: str
    attrs: dict[str, str]
    children: list[Node | str] = field(default_factory=list)

    def classes(self) -> set[str]:
        """Return the element's CSS classes."""
        return set(self.attrs.get("class", "").split())


class TreeBuilder(HTMLParser):
    """Build a ``Node`` tree, tolerating unclosed and stray end tags."""

    def __init__(self) -> None:
        """Start with an empty root."""
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Open an element (void elements close at once)."""
        node = Node(tag, {key: value or "" for key, value in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        """Close the innermost open element with this tag, if any."""
        for depth in range(len(self.stack) - 1, 0, -1):
            if self.stack[depth].tag == tag:
                del self.stack[depth:]
                return

    def handle_data(self, data: str) -> None:
        """Keep text as a child of the current element."""
        self.stack[-1].children.append(data)


def find(node: Node, tag: str, *, node_id: str = "", css_class: str = "") -> Node | None:
    """Depth-first search for the first element matching the tag, id and class given."""
    matches = node.tag == tag and (not node_id or node.attrs.get("id") == node_id)
    if matches and (not css_class or css_class in node.classes()):
        return node
    for child in node.children:
        if isinstance(child, Node):
            hit = find(child, tag, node_id=node_id, css_class=css_class)
            if hit:
                return hit
    return None


def raw_text(node: Node | str) -> str:
    """All text under ``node``, as written."""
    if isinstance(node, str):
        return node
    return "".join(raw_text(child) for child in node.children)


def inline(node: Node | str) -> str:
    """Render inline content as Markdown, collapsing whitespace."""
    if isinstance(node, str):
        return WHITESPACE_RE.sub(" ", node)
    inner = "".join(inline(child) for child in node.children)
    rendered = {
        "code": lambda: f"`{WHITESPACE_RE.sub(' ', raw_text(node)).strip()}`",
        "strong": lambda: f"**{inner.strip()}**" if inner.strip() else "",
        "b": lambda: f"**{inner.strip()}**" if inner.strip() else "",
        "em": lambda: f"_{inner.strip()}_" if inner.strip() else "",
        "i": lambda: f"_{inner.strip()}_" if inner.strip() else "",
        "del": lambda: f"~~{inner.strip()}~~" if inner.strip() else "",
        "a": lambda: _link(node, inner),
    }
    return rendered.get(node.tag, lambda: inner)()


def _link(node: Node, text: str) -> str:
    href = node.attrs.get("href", "")
    if not text.strip() or text.strip() == "↩":
        return ""
    if not href or href.startswith("#"):
        return text
    return f"[{text.strip()}]({href})"


class Renderer:
    """Render block-level nodes to Markdown lines."""

    def __init__(self) -> None:
        """Start with no output and no pending example label."""
        self.out: list[str] = []
        self.label = ""

    def block(self, node: Node | str, indent: str = "") -> None:
        """Render ``node`` and its children as Markdown blocks."""
        if isinstance(node, str):
            if node.strip():
                self.out.append(f"{indent}{inline(node).strip()}\n\n")
            return
        if node.tag in SKIPPED_TAGS:
            return
        marker = LABELS.keys() & node.classes()
        if node.tag == "div" and marker and not node.children:
            self.label = LABELS[next(iter(marker))]
            return
        handler = {
            "pre": self.code_block,
            "p": self.paragraph,
            "ul": self.bullets,
            "ol": self.numbered,
            "table": self.table,
            "blockquote": self.quote,
            "dl": self.definitions,
        }.get(node.tag)
        if node.tag in HEADING_TAGS:
            self.heading(node)
        elif handler:
            handler(node, indent)
        else:
            for child in node.children:
                self.block(child, indent)

    def heading(self, node: Node) -> None:
        """Emit the page anchor, then the heading."""
        anchor = node.attrs.get("id")
        if anchor:
            self.out.append(f'<a id="{anchor}"></a>\n')
        self.out.append(f"{'#' * HEADING_TAGS[node.tag]} {inline(node).strip()}\n\n")

    def paragraph(self, node: Node, indent: str) -> None:
        """Emit a paragraph; a lone "Why?" becomes a bold lead-in."""
        text = inline(node).strip()
        if text == "Why?":
            text = "**Why?**"
        if text:
            self.out.append(f"{indent}{text}\n\n")

    def code_block(self, node: Node, indent: str) -> None:
        """Emit a fenced block, labelled when the page marks it good or bad."""
        code = find(node, "code") or node
        classes = code.classes() | node.classes()
        label = next((LABELS[name] for name in ("good", "bad") if name in classes), self.label)
        self.label = ""
        language_match = next((m for m in map(LANGUAGE_RE.match, sorted(classes)) if m), None)
        language = language_match.group("language") if language_match else ""
        if label:
            self.out.append(f"{indent}{label}\n\n")
        body = "\n".join(f"{indent}{line}" if line else "" for line in raw_text(code).rstrip("\n").split("\n"))
        self.out.append(f"{indent}```{language}\n{body}\n{indent}```\n\n")

    def bullets(self, node: Node, indent: str) -> None:
        """Emit an unordered list."""
        self.items(node, indent, ordered=False)

    def numbered(self, node: Node, indent: str) -> None:
        """Emit an ordered list."""
        self.items(node, indent, ordered=True)

    def items(self, node: Node, indent: str, *, ordered: bool) -> None:
        """Emit list items, rendering nested blocks under each."""
        number = 0
        for child in node.children:
            if not isinstance(child, Node) or child.tag != "li":
                continue
            number += 1
            marker = f"{number}. " if ordered else "*   "
            inline_parts = [part for part in child.children if not _is_block(part)]
            blocks = [part for part in child.children if _is_block(part)]
            head = "".join(inline(part) for part in inline_parts).strip()
            if not head and blocks and isinstance(blocks[0], Node) and blocks[0].tag == "p":
                head = inline(blocks.pop(0)).strip()
            self.out.append(f"{indent}{marker}{head}\n\n")
            for block in blocks:
                self.block(block, indent + " " * len(marker))
        self.out.append("\n")

    def table(self, node: Node, indent: str) -> None:
        """Emit a Markdown table; cell content is flattened to one line."""
        rows = [
            [inline(cell).strip().replace("|", "\\|") for cell in row.children if isinstance(cell, Node)]
            for row in _all(node, "tr")
        ]
        rows = [row for row in rows if row]
        if not rows:
            return
        lines = [f"| {' | '.join(rows[0])} |", f"| {' | '.join('---' for _ in rows[0])} |"]
        lines += [f"| {' | '.join(row)} |" for row in rows[1:]]
        self.out.append(indent + f"\n{indent}".join(lines) + "\n\n")

    def quote(self, node: Node, indent: str) -> None:
        """Emit a blockquote by rendering its content and prefixing each line."""
        inner = Renderer()
        for child in node.children:
            inner.block(child)
        text = "".join(inner.out).strip("\n")
        self.out.append("\n".join(f"{indent}> {line}".rstrip() for line in text.split("\n")) + "\n\n")

    def definitions(self, node: Node, indent: str) -> None:
        """Emit a definition list as bold terms followed by their text."""
        for child in node.children:
            if isinstance(child, Node) and child.tag == "dt":
                self.out.append(f"{indent}**{inline(child).strip()}**\n\n")
            elif isinstance(child, Node) and child.tag == "dd":
                for grandchild in child.children:
                    self.block(grandchild, indent)


def _is_block(part: Node | str) -> bool:
    return isinstance(part, Node) and part.tag in {"p", "ul", "ol", "pre", "table", "blockquote", "div"}


def _all(node: Node, tag: str) -> list[Node]:
    found = [node] if node.tag == tag else []
    for child in node.children:
        if isinstance(child, Node):
            found.extend(_all(child, tag))
    return found


class MissingContentError(Exception):
    """The page has no recognizable content container."""

    def __init__(self, path: Path) -> None:
        """Name the file that could not be converted."""
        super().__init__(f"{path}: no div#content or div.markdown-body found")


def convert(path: Path) -> str:
    """Return the Markdown rendering of the style guide page at ``path``."""
    builder = TreeBuilder()
    builder.feed(path.read_text(encoding="utf-8"))
    content = find(builder.root, "div", node_id="content") or find(builder.root, "div", css_class="markdown-body")
    if content is None:
        raise MissingContentError(path)
    toc = find(content, "ul", node_id="markdown-toc")
    if toc:
        content.children = [child for child in content.children if child is not toc]
    renderer = Renderer()
    renderer.block(content)
    markdown = html.unescape("".join(renderer.out))
    return BLANK_RUN_RE.sub("\n\n", markdown).strip() + "\n"


def main() -> int:
    """Convert the HTML file named on the command line and print the Markdown."""
    sys.stdout.write(convert(Path(sys.argv[1])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
