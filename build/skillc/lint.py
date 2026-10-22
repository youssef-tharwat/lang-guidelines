"""Read a tiered lint digest: ``## Tier N`` headings over one ``### rule`` entry per lint rule."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .errors import BuildError
from .markdown_text import scan

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

TIER_RE = re.compile(r"^## Tier (?P<tier>\d)\b")
ENTRY_RE = re.compile(r"^### (?P<name>[\w./-]+)(?: \((?P<code>[A-Z]+[0-9]+)\))?\s*$")


@dataclass(frozen=True)
class LintRule:
    """One lint rule from the digest: its name (``slug`` or ``plugin/slug``), Ruff code if any, and tier."""

    name: str
    code: str | None
    tier: int


class LintDigestError(BuildError):
    """The lint digest or the per-rule docs beside it are inconsistent."""


class RuleBeforeTierError(LintDigestError):
    """A rule entry appears before any ``## Tier N`` heading."""

    def __init__(self, name: str) -> None:
        """Name the orphaned rule."""
        super().__init__(f"rule {name} appears before any tier heading")


class EmptyDigestError(LintDigestError):
    """The digest holds no rule entries."""

    def __init__(self) -> None:
        """Explain what was expected."""
        super().__init__("the lint digest holds no '### rule' entries under a tier heading")


class MissingRuleDocsError(LintDigestError):
    """Rules in the digest have no per-rule doc."""

    def __init__(self, names: list[str]) -> None:
        """Name every rule whose doc is missing."""
        super().__init__(f"lint rules without a doc: {', '.join(names)}")


def parse_lint_digest(text: str) -> list[LintRule]:
    """Every rule entry, tagged with the tier heading above it; fail on entries before any tier."""
    rules: list[LintRule] = []
    tier = 0
    for line in scan(text):
        if line.in_fence:
            continue
        tier_match = TIER_RE.match(line.text)
        if tier_match:
            tier = int(tier_match.group("tier"))
            continue
        entry = ENTRY_RE.match(line.text)
        if entry:
            if not tier:
                raise RuleBeforeTierError(entry.group("name"))
            rules.append(LintRule(name=entry.group("name"), code=entry.group("code"), tier=tier))
    if not rules:
        raise EmptyDigestError
    return rules


def require_docs(rules: list[LintRule], doc_path: Callable[[LintRule], Path]) -> None:
    """Fail unless every rule has its per-rule doc, so the card's pointer to them holds."""
    missing = [rule.name for rule in rules if not doc_path(rule).is_file()]
    if missing:
        raise MissingRuleDocsError(missing)
