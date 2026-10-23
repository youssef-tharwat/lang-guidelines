# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Split the Python sources into units, and build ``ruff.toml`` from the Ruff tier digest.

Unit ids: ``G:<anchor>`` (a Google Python Style Guide section, by its page anchor) and
``P:<path>`` (a python-patterns.guide page, by its URL path).
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from .errors import BuildError
from .guide import split_sections
from .json_shape import as_array, as_object, as_str
from .lint import LintRule, parse_lint_digest, require_docs
from .markdown_text import clean_body
from .pages import humanize, split_pages
from .units import Source, Unit

if TYPE_CHECKING:
    from pathlib import Path

GOOGLE = Source(
    title="Google Python Style Guide",
    license="CC BY 3.0",
    home="https://google.github.io/styleguide/pyguide.html",
)
RHODES = Source(
    title="Python Design Patterns by Brandon Rhodes (python-patterns.guide)",
    license="copyright Brandon Rhodes, redistributed with attribution",
    home="https://python-patterns.guide/",
)

GOOGLE_FILE = "google-python-style-guide.md"
PATTERNS_FILE = "python-patterns.md"
LINT_FILE = "ruff-rules.md"
INVENTORY_FILE = "ruff-inventory.json"
SELECTABLE_STATUSES = frozenset({"Stable", "Preview"})
FRAMEWORKS = ("airflow", "django", "fastapi", "numpy", "pandas")
VENDORED = ("lint", "style.md", "frameworks")

TOC_ENTRY_RE = re.compile(r"\[(?P<number>\d+(?:\.\d+)*) [^\]]*\]\(#(?P<anchor>[^)\s]+)\)")
SECTION_TITLE_RE = re.compile(r"^(?P<number>\d+(?:\.\d+)*)\s+(?P<title>.+?)\s*$")
HTML_ANCHOR_RE = re.compile(r'^\s*<a id="[^"]*"></a>\s*$')
TOC_END = "</details>"


class UnanchoredSectionError(BuildError):
    """A guide section has no number, or its number has no anchor in the table of contents."""

    def __init__(self, title: str) -> None:
        """Name the section that could not be anchored."""
        super().__init__(f"Google Python guide section {title!r} has no table-of-contents anchor")


class MissingVendoredError(BuildError):
    """A vendored file the skill points to is missing."""

    def __init__(self, paths: list[str]) -> None:
        """Name every missing path."""
        super().__init__(f"python-guidelines is missing vendored files: {', '.join(paths)}")


def load_units(sources_dir: Path) -> list[Unit]:
    """Parse the Google guide and the pattern pages in ``sources_dir``."""
    return [
        *parse_google((sources_dir / GOOGLE_FILE).read_text(encoding="utf-8")),
        *parse_patterns((sources_dir / PATTERNS_FILE).read_text(encoding="utf-8")),
    ]


def parse_google(text: str) -> list[Unit]:
    """One unit per numbered h2 or h3 section with text of its own, identified by its TOC anchor."""
    toc, _, guide = text.partition(TOC_END)
    anchors = {match.group("number"): match.group("anchor") for match in TOC_ENTRY_RE.finditer(toc)}
    body = "\n".join(line for line in guide.split("\n") if not HTML_ANCHOR_RE.match(line))
    units: list[Unit] = []
    for section in split_sections(body, frozenset({2, 3})):
        match = SECTION_TITLE_RE.match(section.title)
        anchor = anchors.get(match.group("number")) if match else None
        if not match or not anchor:
            raise UnanchoredSectionError(section.title)
        units.append(
            Unit(
                unit_id=f"G:{anchor}",
                title=match.group("title"),
                url=f"{GOOGLE.home}#{anchor}",
                body=clean_body(section.body),
                source=GOOGLE,
            )
        )
    return units


def parse_patterns(text: str) -> list[Unit]:
    """One unit per python-patterns.guide page; the pages carry no title heading, so the path names them."""
    units: list[Unit] = []
    for page in split_pages(text):
        path = page.url.removeprefix(RHODES.home).strip("/")
        units.append(
            Unit(
                unit_id=f"P:{path}",
                title=humanize(path.rsplit("/", 1)[-1]),
                url=page.url,
                body=clean_body(page.text),
                source=RHODES,
            )
        )
    return units


def selectable_codes(sources_dir: Path) -> tuple[str, frozenset[str]]:
    """Return the pinned Ruff version and the rule codes it can select (stable or preview).

    A new preview rule can ship before it is assigned a code; with no code it cannot be
    selected by code, so it is skipped.
    """
    inventory = as_object(json.loads((sources_dir / INVENTORY_FILE).read_text(encoding="utf-8")), INVENTORY_FILE)
    version = as_str(inventory.get("ruff_version"), "ruff_version")
    codes: set[str] = set()
    for item in as_array(inventory.get("rules"), "rules"):
        rule = as_object(item, "rule")
        code = rule.get("code")
        if code is not None and as_str(rule.get("status"), "status") in SELECTABLE_STATUSES:
            codes.add(as_str(code, "code"))
    return version, frozenset(codes)


def extra_outputs(sources_dir: Path) -> dict[str, str]:
    """Return ``ruff.toml`` selecting every digest rule the pinned Ruff can still select, naming the rest."""
    rules = parse_lint_digest((sources_dir / LINT_FILE).read_text(encoding="utf-8"))
    version, codes = selectable_codes(sources_dir)
    selected = [rule for rule in rules if rule.code in codes]
    omitted = ", ".join(_label(rule) for rule in rules if rule.code not in codes)
    lines = "\n".join(f'    "{rule.code}",  # {rule.name} (tier {rule.tier})' for rule in selected)
    header = (
        "# Tier 1 (correctness, security) and Tier 2 (modernization, performance) Ruff rules.\n"
        "# Generated by build/compile.py from sources/python/ruff-rules.md, for Ruff >= "
        f"{version}. Use it when the\n"
        "# project has no Ruff configuration of its own:  ruff check --config <this file> <paths>\n"
        "# Preview rules are named by exact code, so only the ones listed here run.\n"
        f"# Omitted because Ruff {version} no longer has them: {omitted or 'none'}.\n"
    )
    config = f"[lint]\npreview = true\nexplicit-preview-rules = true\nselect = [\n{lines}\n]\n"
    return {"ruff.toml": f"{header}\n{config}"}


def _label(rule: LintRule) -> str:
    return f"{rule.code} ({rule.name})" if rule.code else rule.name


def check_vendored(sources_dir: Path, folder: Path) -> None:
    """Fail unless every digest rule has its doc and every framework file and style.md exist."""
    rules = parse_lint_digest((sources_dir / LINT_FILE).read_text(encoding="utf-8"))
    require_docs(rules, lambda rule: folder / "lint" / rule.name / "index.md")
    expected = ["style.md", *(f"frameworks/{name}.md" for name in FRAMEWORKS)]
    missing = [path for path in expected if not (folder / path).is_file()]
    if missing:
        raise MissingVendoredError(missing)
