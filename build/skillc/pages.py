# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Concatenated web pages: split at ``<!-- source: url -->`` markers, and clean refactoring.guru pages."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .markdown_text import HEADING_RE, clean_body, heading, scan
from .units import Source, Unit

SOURCE_MARKER_RE = re.compile(r"^<!-- source: (?P<url>\S+) -->$")
GOF_URL_RE = re.compile(r"/design-patterns/(?P<slug>[a-z-]+)/[a-z]+/")
GOF_NAV_RE = re.compile(
    r"^(# .+ in \w+ / Design Patterns\s*|\[?# \*\*.*|(\[[^\]]*\]\(https://refactoring\.guru[^)]*\))+\s*)$"
)
GOF_FILE_HEADING_RE = re.compile(r"^#{1,6} \*\*(?P<name>[\w./-]+\.(?P<ext>\w+)):?\*\*.*$")
GOF_OUTPUT_HEADING_RE = re.compile(r"^#{1,6} Output\s*$")
FENCE_LANGUAGE = {"rs": "rust", "toml": "toml", "ts": "typescript", "py": "python"}


@dataclass(frozen=True)
class Page:
    """One upstream page: its URL and its Markdown text."""

    url: str
    text: str


def split_pages(text: str) -> list[Page]:
    """Split ``text`` at its source markers; text before the first marker is dropped."""
    pages: list[Page] = []
    url = ""
    lines: list[str] = []
    for line in scan(text):
        match = None if line.in_fence else SOURCE_MARKER_RE.match(line.text)
        if match:
            if url:
                pages.append(Page(url, "\n".join(lines)))
            url = match.group("url")
            lines = []
            continue
        lines.append(line.text)
    if url:
        pages.append(Page(url, "\n".join(lines)))
    return pages


def first_heading(text: str) -> str | None:
    """Return the title of the first heading outside code, if any."""
    return next((found[1] for line in scan(text) if (found := heading(line))), None)


def drop_first_heading(text: str) -> str:
    """Remove the first heading outside code; it becomes the unit title instead."""
    lines = text.split("\n")
    for index, line in enumerate(scan(text)):
        if heading(line):
            return "\n".join(lines[:index] + lines[index + 1 :])
    return text


def humanize(slug: str) -> str:
    """Turn a URL slug such as ``chain-of-responsibility`` into ``Chain of Responsibility``."""
    return slug.replace("-", " ").title().replace(" Of ", " of ")


def gang_of_four_unit(page: Page, source: Source) -> Unit | None:
    """Build the unit for a refactoring.guru page, or ``None`` when ``page`` is from elsewhere."""
    match = GOF_URL_RE.search(page.url)
    if not match:
        return None
    slug = match.group("slug")
    title = humanize(slug)
    return Unit(
        unit_id=f"GOF:{slug}",
        title=f"{title} (Gang of Four)",
        url=page.url,
        body=clean_body(_fence_gang_of_four_code(page.text)),
        source=source,
    )


def _fence_gang_of_four_code(text: str) -> str:
    """Re-fence the example code the refactoring.guru extraction left unfenced, and drop page navigation."""
    out: list[str] = []
    block: list[str] = []
    language = ""

    def flush() -> None:
        body = "\n".join(block).strip("\n")
        if body:
            out.extend([f"```{language}", body, "```", ""])

    for line in text.split("\n"):
        if GOF_NAV_RE.match(line):
            continue
        if HEADING_RE.match(line):
            if language:
                flush()
                block = []
            file_heading = GOF_FILE_HEADING_RE.match(line)
            if file_heading:
                language = FENCE_LANGUAGE.get(file_heading.group("ext"), "text")
            elif GOF_OUTPUT_HEADING_RE.match(line):
                language = "text"
            else:
                language = ""
            out.append(line)
            continue
        (block if language else out).append(line)
    if language:
        flush()
    return "\n".join(out)
