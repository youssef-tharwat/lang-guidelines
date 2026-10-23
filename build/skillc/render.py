# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Render a manifest and its units into the files a model reads."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from .errors import BuildError
from .manifest import GroupKind, Scope

if TYPE_CHECKING:
    from .manifest import Entry, Manifest
    from .units import Unit

SCOPE_TAG = {Scope.ALL: "", Scope.LIB: " `[lib]`", Scope.APP: " `[app]`"}
SCOPE_TEXT = {
    Scope.LIB: "libraries (code other packages depend on); a strong recommendation in application-only code",
    Scope.APP: "applications only",
}
RULE_CARD = "{{RULE_CARD}}"
PATTERN_INDEX = "{{PATTERN_INDEX}}"
LINTS = "{{LINTS}}"


class TemplateError(BuildError):
    """The SKILL.md template does not hold each placeholder exactly once."""

    def __init__(self, placeholder: str) -> None:
        """Name the placeholder that is missing or repeated."""
        super().__init__(f"template must contain {placeholder} exactly once")


def render_outputs(manifest: Manifest, units: list[Unit], template: str) -> dict[str, str]:
    """Return every generated file keyed by its path inside the skill folder."""
    by_id = {unit.unit_id: unit for unit in units}
    outputs = {"SKILL.md": render_skill(template, manifest)}
    outputs.update(
        {f"rules/{entry.entry_id}.md": render_entry(entry, by_id, GroupKind.RULE) for entry in manifest.rules}
    )
    outputs.update(
        {f"patterns/{entry.entry_id}.md": render_entry(entry, by_id, GroupKind.PATTERN) for entry in manifest.patterns}
    )
    return outputs


def render_skill(template: str, manifest: Manifest) -> str:
    """Fill the template's placeholders with the rule card, the lint line and the pattern index."""
    replacements = {
        RULE_CARD: render_index(manifest, GroupKind.RULE),
        PATTERN_INDEX: render_index(manifest, GroupKind.PATTERN),
        LINTS: render_lints(manifest),
    }
    for placeholder, text in replacements.items():
        if template.count(placeholder) != 1:
            raise TemplateError(placeholder)
        template = template.replace(placeholder, text)
    return template


def render_index(manifest: Manifest, kind: GroupKind) -> str:
    """One line per entry, under the group headings in declaration order."""
    entries = manifest.rules if kind is GroupKind.RULE else manifest.patterns
    lines_by_group: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        lines_by_group[entry.group_id].append(_index_line(entry))
    groups = [group for group in manifest.groups if group.kind is kind]
    return "\n\n".join(f"### {group.title}\n\n" + "\n".join(lines_by_group[group.group_id]) for group in groups)


def _index_line(entry: Entry) -> str:
    why = f" _{entry.why}_" if entry.why else ""
    return f"- `{entry.entry_id}`{SCOPE_TAG[entry.scope]} {entry.summary}{why}"


def render_lints(manifest: Manifest) -> str:
    """List the lints that enforce part of the rules; the template words the sentence around them."""
    return ", ".join(f"`{lint.lint}`" for lint in manifest.lints)


def render_entry(entry: Entry, units: dict[str, Unit], kind: GroupKind) -> str:
    """Render the on-demand file for one entry: the card line, then each cited upstream section in full."""
    header = [f"# {entry.entry_id}", "", entry.summary, ""]
    if entry.why:
        header += [f"**Why:** {entry.why}", ""]
    if kind is GroupKind.RULE and entry.scope in SCOPE_TEXT:
        header += [f"**Binding in:** {SCOPE_TEXT[entry.scope]}.", ""]
    header += [f"**Sources:** {', '.join(entry.sources)}"]
    sections = [_source_section(units[unit_id]) for unit_id in entry.sources]
    return "\n".join(header) + "\n\n---\n\n" + "\n\n".join(sections)


def _source_section(unit: Unit) -> str:
    return (
        f"## {unit.title} ({unit.unit_id})\n\n[{unit.source.title}]({unit.url}), {unit.source.license}.\n\n{unit.body}"
    )
