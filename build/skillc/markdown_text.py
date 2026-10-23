# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Fence-aware Markdown helpers shared by every skill's source parsers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

FENCE_RE = re.compile(r"^(?P<prefix>[\s>]*)(?P<fence>`{3,}|~{3,})(?P<info>[^`]*)$")
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6}) (?P<title>.+?)\s*$")
RUSTDOC_HIDDEN_RE = re.compile(r"^\s*#(\s|$)")
RELATIVE_LINK_RE = re.compile(r"(?<!!)\[(?P<text>[^\]]+)\]\((?!https?://|mailto:)[^)]*\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK_DEFINITION_RE = re.compile(r"^\s*\[(?P<label>[^\]^][^\]]*)\]:\s+\S+\s*$")
FULL_REFERENCE_RE = re.compile(r"\[(?P<text>[^\]]+)\]\[[^\]]*\]")
SHORTCUT_REFERENCE_RE = re.compile(r"(?<![!\]])\[(?P<text>[^\]^][^\]]*)\](?![(\[:])")
BLANK_RUN_RE = re.compile(r"\n{3,}")
PERMALINK_RE = re.compile(r"\[¶\]\([^)]*\)")


class Role(Enum):
    """Where a line sits relative to code fences."""

    PROSE = "prose"
    FENCE_OPEN = "fence-open"
    CODE = "code"
    FENCE_CLOSE = "fence-close"


@dataclass(frozen=True)
class Line:
    """One source line, its role, and the info string of the fence it belongs to."""

    text: str
    role: Role
    fence_info: str

    @property
    def in_fence(self) -> bool:
        """Whether the line is a fence marker or code inside a fence."""
        return self.role is not Role.PROSE


def scan(text: str) -> Iterator[Line]:
    """Yield each line of ``text`` tagged with whether it sits inside a code fence.

    Follows CommonMark: a fence closes only on a run of the same character, at least as
    long as the opening run, with no info string.
    """
    open_fence = ""
    info = ""
    for raw in text.split("\n"):
        match = FENCE_RE.match(raw)
        if match:
            fence = match.group("fence")
            if not open_fence:
                open_fence, info = fence, match.group("info").strip()
                yield Line(raw, Role.FENCE_OPEN, info)
                continue
            closes = fence[0] == open_fence[0] and len(fence) >= len(open_fence) and not match.group("info").strip()
            if closes:
                yield Line(raw, Role.FENCE_CLOSE, info)
                open_fence, info = "", ""
                continue
        yield Line(raw, Role.CODE if open_fence else Role.PROSE, info)


def close_open_fence(text: str) -> str:
    """Append a closing fence when ``text`` ends inside a code block."""
    opener: Line | None = None
    for line in scan(text):
        if line.role is Role.FENCE_OPEN:
            opener = line
        elif line.role is Role.FENCE_CLOSE:
            opener = None
    match = FENCE_RE.match(opener.text) if opener else None
    return f"{text}\n{match.group('prefix')}{match.group('fence')}" if match else text


def heading(line: Line) -> tuple[int, str] | None:
    """Return ``(level, title)`` when ``line`` is a Markdown heading outside code."""
    if line.in_fence:
        return None
    match = HEADING_RE.match(line.text)
    if not match:
        return None
    return len(match.group("hashes")), match.group("title")


def map_prose(text: str, transform: Callable[[str], str]) -> str:
    """Apply ``transform`` to every line outside code fences."""
    return "\n".join(line.text if line.in_fence else transform(line.text) for line in scan(text))


def normalize_rust_fences(text: str) -> str:
    """Reduce rustdoc fence attributes (``rust,ignore``) to ``rust`` and drop hidden doctest lines."""
    kept: list[str] = []
    for line in scan(text):
        is_rust = line.fence_info.replace(" ", "").startswith("rust")
        if line.role is Role.FENCE_OPEN and is_rust:
            marker = FENCE_RE.match(line.text)
            kept.append(f"{marker.group('prefix')}{marker.group('fence')}rust" if marker else line.text)
            continue
        if line.role is Role.CODE and is_rust and RUSTDOC_HIDDEN_RE.match(line.text.lstrip(" >")):
            continue
        kept.append(line.text)
    return "\n".join(kept)


def demote_headings(text: str, top_level: int) -> str:
    """Shift headings so the shallowest one becomes ``top_level`` (capped at level 6)."""
    levels = [found[0] for line in scan(text) if (found := heading(line))]
    if not levels:
        return text
    shift = top_level - min(levels)
    shifted: list[str] = []
    for line in scan(text):
        found = heading(line)
        if found:
            shifted.append(f"{'#' * min(found[0] + shift, 6)} {found[1]}")
        else:
            shifted.append(line.text)
    return "\n".join(shifted)


def unlink_relative(line: str) -> str:
    """Keep the text of links that point inside the upstream site, which do not resolve here."""
    return RELATIVE_LINK_RE.sub(r"\g<text>", line)


def drop_images(line: str) -> str:
    """Remove image embeds; screenshots carry no information for a model."""
    return IMAGE_RE.sub("", line)


def strip_reference_links(text: str) -> str:
    """Replace reference-style links with their text and drop the ``[label]: url`` definitions."""
    labels = {
        match.group("label").lower()
        for line in scan(text)
        if not line.in_fence and (match := LINK_DEFINITION_RE.match(line.text))
    }

    def unlink(line: str) -> str:
        line = FULL_REFERENCE_RE.sub(r"\g<text>", line)
        return SHORTCUT_REFERENCE_RE.sub(
            lambda match: match.group("text") if match.group("text").lower() in labels else match.group(0),
            line,
        )

    kept = (line for line in scan(text) if line.in_fence or not LINK_DEFINITION_RE.match(line.text))
    return "\n".join(line.text if line.in_fence else unlink(line.text) for line in kept)


def clean_body(text: str) -> str:
    """Apply the cleanup every upstream section gets, rooting its headings at level 3."""
    text = strip_reference_links(text)
    text = map_prose(text, lambda line: unlink_relative(drop_images(PERMALINK_RE.sub("", line))))
    text = normalize_rust_fences(text)
    text = demote_headings(text, top_level=3)
    return collapse_blank_lines(text)


def collapse_blank_lines(text: str) -> str:
    """Collapse runs of blank lines and trim the ends."""
    return BLANK_RUN_RE.sub("\n\n", text).strip() + "\n"


def slugify(title: str) -> str:
    """Return the kramdown anchor for a heading (Google style guide anchors use this scheme)."""
    plain = title.lower().replace("`", "")
    plain = re.sub(r"[^a-z0-9 _-]", "", plain)
    return plain.replace(" ", "-")
