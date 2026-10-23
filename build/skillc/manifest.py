# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Load a skill manifest and check it against the upstream units it cites."""

from __future__ import annotations

import tomllib
from collections import Counter
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from .errors import BuildError

if TYPE_CHECKING:
    from pathlib import Path

    from .units import Unit


class Scope(StrEnum):
    """Where a rule is binding."""

    ALL = "all"
    LIB = "lib"
    APP = "app"


class GroupKind(StrEnum):
    """What a group holds."""

    RULE = "rule"
    PATTERN = "pattern"


@dataclass(frozen=True)
class Group:
    """A heading on the rule card or the pattern index, ordered as declared."""

    group_id: str
    title: str
    kind: GroupKind


@dataclass(frozen=True)
class Entry:
    """A rule or pattern: one line on the card, one file of upstream text on demand."""

    entry_id: str
    group_id: str
    summary: str
    why: str
    scope: Scope
    sources: tuple[str, ...]


@dataclass(frozen=True)
class Lint:
    """An upstream rule a default-on lint already enforces, so the card names the lint instead."""

    lint: str
    sources: tuple[str, ...]


@dataclass(frozen=True)
class Exclusion:
    """An upstream unit deliberately kept out of the skill, with the reason."""

    unit_id: str
    reason: str


@dataclass(frozen=True)
class Manifest:
    """The hand-maintained mapping from upstream units to what the model reads."""

    groups: tuple[Group, ...]
    rules: tuple[Entry, ...]
    patterns: tuple[Entry, ...]
    lints: tuple[Lint, ...]
    exclusions: tuple[Exclusion, ...]


class ManifestError(BuildError):
    """The manifest is malformed or disagrees with the upstream units."""


class FieldError(ManifestError):
    """A manifest value is missing or has the wrong type."""

    def __init__(self, where: str, key: str, expected: str) -> None:
        """Describe the field at ``where``/``key`` and the type it should have."""
        super().__init__(f"{where}: {key!r} must be {expected}")


class MappingError(ManifestError):
    """The manifest's mapping of upstream units is inconsistent."""

    def __init__(self, problems: list[str]) -> None:
        """Report every problem at once, one per line."""
        super().__init__("\n".join(problems))


class UnknownKeysError(ManifestError):
    """A manifest table carries keys the compiler does not read, usually a typo."""

    def __init__(self, where: str, keys: list[str]) -> None:
        """Name the table and its unknown keys."""
        super().__init__(f"{where}: unknown keys {', '.join(keys)}")


ROOT_KEYS = frozenset({"group", "rule", "pattern", "lint", "exclusion"})
GROUP_KEYS = frozenset({"id", "title", "kind"})
RULE_KEYS = frozenset({"id", "group", "text", "why", "scope", "sources"})
PATTERN_KEYS = frozenset({"id", "group", "when", "sources"})
LINT_KEYS = frozenset({"lint", "sources"})
EXCLUSION_KEYS = frozenset({"unit", "reason"})


class Table:
    """One TOML table, read through typed accessors so malformed input fails loudly."""

    def __init__(self, raw: object, where: str) -> None:
        """Wrap ``raw``, which must be a TOML table; ``where`` names it in errors."""
        if not isinstance(raw, dict):
            raise FieldError(where, "(table)", "a table")
        self.raw: dict[object, object] = raw
        self.where = where

    def only(self, allowed: frozenset[str]) -> Table:
        """Fail if the table has keys outside ``allowed``; return it for chaining."""
        unknown = sorted(str(key) for key in self.raw if key not in allowed)
        if unknown:
            raise UnknownKeysError(self.where, unknown)
        return self

    def string(self, key: str, default: str | None = None) -> str:
        """Return the string at ``key``, or ``default`` when the key is absent and a default is given."""
        value = self.raw.get(key, default)
        if not isinstance(value, str):
            raise FieldError(self.where, key, "a string")
        return value

    def strings(self, key: str) -> tuple[str, ...]:
        """Return the non-empty list of strings at ``key``."""
        value = self.raw.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
            raise FieldError(self.where, key, "a non-empty list of strings")
        return tuple(str(item) for item in value)

    def tables(self, key: str, allowed: frozenset[str]) -> list[Table]:
        """Return the array of tables at ``key``, each checked against the ``allowed`` keys."""
        value = self.raw.get(key)
        if not isinstance(value, list):
            raise FieldError(self.where, key, "an array of tables")
        return [Table(item, f"{key}[{index}]").only(allowed) for index, item in enumerate(value)]


def load(path: Path, units: list[Unit]) -> Manifest:
    """Read ``path`` and fail unless every unit is mapped exactly as the manifest claims."""
    with path.open("rb") as handle:
        root = Table(tomllib.load(handle), path.name).only(ROOT_KEYS)
    manifest = Manifest(
        groups=tuple(
            Group(group_id=item.string("id"), title=item.string("title"), kind=GroupKind(item.string("kind")))
            for item in root.tables("group", GROUP_KEYS)
        ),
        rules=tuple(_entry(item, "text") for item in root.tables("rule", RULE_KEYS)),
        patterns=tuple(_entry(item, "when") for item in root.tables("pattern", PATTERN_KEYS)),
        lints=tuple(
            Lint(lint=item.string("lint"), sources=item.strings("sources")) for item in root.tables("lint", LINT_KEYS)
        ),
        exclusions=tuple(
            Exclusion(unit_id=item.string("unit"), reason=item.string("reason"))
            for item in root.tables("exclusion", EXCLUSION_KEYS)
        ),
    )
    _validate(manifest, {unit.unit_id for unit in units})
    return manifest


def _entry(item: Table, summary_key: str) -> Entry:
    return Entry(
        entry_id=item.string("id"),
        group_id=item.string("group"),
        summary=item.string(summary_key),
        why=item.string("why", ""),
        scope=Scope(item.string("scope", Scope.ALL)),
        sources=item.strings("sources"),
    )


def _validate(manifest: Manifest, unit_ids: set[str]) -> None:
    problems: list[str] = []
    entries = manifest.rules + manifest.patterns
    duplicates = [entry_id for entry_id, count in Counter(e.entry_id for e in entries).items() if count > 1]
    problems.extend(f"duplicate entry id {entry_id}" for entry_id in duplicates)

    kinds = {group.group_id: group.kind for group in manifest.groups}
    expected = [(entry, GroupKind.RULE) for entry in manifest.rules]
    expected += [(entry, GroupKind.PATTERN) for entry in manifest.patterns]
    problems.extend(
        f"{entry.entry_id}: group {entry.group_id!r} is not a {kind} group"
        for entry, kind in expected
        if kinds.get(entry.group_id) != kind
    )
    problems.extend(f"rule {entry.entry_id} has no why" for entry in manifest.rules if not entry.why)

    cited = [source for entry in entries for source in entry.sources]
    cited += [source for lint in manifest.lints for source in lint.sources]
    excluded = [exclusion.unit_id for exclusion in manifest.exclusions]
    problems.extend(f"unknown unit {unit_id}" for unit_id in sorted(set(cited + excluded) - unit_ids))
    problems.extend(f"unit {unit_id} is both cited and excluded" for unit_id in sorted(set(cited) & set(excluded)))
    problems.extend(f"unmapped unit {unit_id}" for unit_id in sorted(unit_ids - set(cited) - set(excluded)))
    if problems:
        raise MappingError(problems)
