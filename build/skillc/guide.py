"""Split a style guide into sections at chosen heading levels."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .markdown_text import heading, scan

ANCHOR_LINE_RE = re.compile(r'^\s*<a id="(?P<anchor>[^"]+)"></a>\s*$')


@dataclass(frozen=True)
class Section:
    """One section: its heading title (empty for text before the first heading) and raw body."""

    title: str
    body: str


@dataclass(frozen=True)
class AnchoredSection:
    """A section plus the page anchor declared on the line before its heading ("" when none)."""

    anchor: str
    title: str
    body: str


def split_anchored_sections(text: str, levels: frozenset[int]) -> list[AnchoredSection]:
    """Split like ``split_sections``, attaching each ``<a id>`` line to the heading right after it.

    Anchor lines are removed from every body; blank lines between an anchor and its heading
    are allowed. Sections whose body is blank are dropped.
    """
    sections: list[AnchoredSection] = []
    anchor, title, lines = "", "", []
    pending = ""
    for line in scan(text):
        anchor_match = None if line.in_fence else ANCHOR_LINE_RE.match(line.text)
        if anchor_match:
            pending = anchor_match.group("anchor")
            continue
        found = heading(line)
        if found and found[0] in levels:
            sections.append(AnchoredSection(anchor, title, "\n".join(lines)))
            anchor, title, lines, pending = pending, found[1], [], ""
            continue
        if line.text.strip():
            pending = ""
        lines.append(line.text)
    sections.append(AnchoredSection(anchor, title, "\n".join(lines)))
    return [section for section in sections if section.body.strip()]


def split_sections(text: str, levels: frozenset[int]) -> list[Section]:
    """Split ``text`` at headings of the given levels; deeper headings stay inside their section.

    Sections whose body is blank (a heading immediately followed by a sub-heading) are dropped.
    """
    sections: list[Section] = []
    title = ""
    lines: list[str] = []
    for line in scan(text):
        found = heading(line)
        if found and found[0] in levels:
            sections.append(Section(title, "\n".join(lines)))
            title, lines = found[1], []
            continue
        lines.append(line.text)
    sections.append(Section(title, "\n".join(lines)))
    return [section for section in sections if section.body.strip()]
