# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Split the TypeScript sources into units, and build ``oxlintrc.jsonc`` from the Oxlint tier digest.

Unit ids: ``G:<anchor>`` (a Google TypeScript Style Guide section, by its page anchor),
``P:<slug>`` (a Systemic TypeScript page) and ``GOF:<slug>`` (a refactoring.guru page).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .errors import BuildError
from .guide import split_anchored_sections
from .json_shape import as_array, as_object, as_str
from .lint import LintRule, parse_lint_digest, require_docs
from .markdown_text import clean_body
from .pages import gang_of_four_unit, humanize, split_pages
from .units import Source, Unit

if TYPE_CHECKING:
    from pathlib import Path

GOOGLE = Source(
    title="Google TypeScript Style Guide",
    license="CC BY 3.0",
    home="https://google.github.io/styleguide/tsguide.html",
)
SYSTEMIC = Source(
    title="Systemic TypeScript by Vincent Alandev (valand.dev)",
    license="copyright the author, redistributed with attribution",
    home="https://valand.dev/systemic-ts",
)
GANG_OF_FOUR = Source(
    title="Design Patterns in TypeScript (refactoring.guru)",
    license="CC BY-SA 4.0",
    home="https://refactoring.guru/design-patterns/typescript",
)

GOOGLE_FILE = "google-typescript-style-guide.md"
PATTERNS_FILE = "typescript-patterns.md"
LINT_FILE = "oxlint-rules.md"
INVENTORY_FILE = "oxlint-inventory.json"
FRAMEWORKS = ("jest", "jsdoc", "nextjs", "react", "vitest", "vue")
VENDORED = ("lint", "style.md", "frameworks")
TIER_SEVERITY = {1: "error", 2: "warn"}


class UnanchoredSectionError(BuildError):
    """A guide section has no ``<a id>`` anchor line before its heading."""

    def __init__(self, title: str) -> None:
        """Name the section that could not be anchored."""
        super().__init__(f"Google TypeScript guide section {title!r} has no anchor")


class MissingVendoredError(BuildError):
    """A vendored file the skill points to is missing."""

    def __init__(self, paths: list[str]) -> None:
        """Name every missing path."""
        super().__init__(f"typescript-guidelines is missing vendored files: {', '.join(paths)}")


def load_units(sources_dir: Path) -> list[Unit]:
    """Parse the Google guide and the pattern pages in ``sources_dir``."""
    return [
        *parse_google((sources_dir / GOOGLE_FILE).read_text(encoding="utf-8")),
        *parse_patterns((sources_dir / PATTERNS_FILE).read_text(encoding="utf-8")),
    ]


def parse_google(text: str) -> list[Unit]:
    """One unit per h2 or h3 section with text of its own, identified by its page anchor."""
    units: list[Unit] = []
    for section in split_anchored_sections(text, frozenset({2, 3})):
        if not section.title:
            continue
        if not section.anchor:
            raise UnanchoredSectionError(section.title)
        units.append(
            Unit(
                unit_id=f"G:{section.anchor}",
                title=section.title,
                url=f"{GOOGLE.home}#{section.anchor}",
                body=clean_body(section.body),
                source=GOOGLE,
            )
        )
    return units


def parse_patterns(text: str) -> list[Unit]:
    """One unit per page: Systemic TypeScript pages by slug (they have no title heading), GoF pages by pattern."""
    units: list[Unit] = []
    for page in split_pages(text):
        gang_of_four = gang_of_four_unit(page, GANG_OF_FOUR)
        if gang_of_four:
            units.append(gang_of_four)
            continue
        slug = page.url.rstrip("/").rsplit("/", 1)[-1]
        units.append(
            Unit(
                unit_id=f"P:{slug}",
                title=humanize(slug),
                url=page.url,
                body=clean_body(page.text),
                source=SYSTEMIC,
            )
        )
    return units


def available_rules(sources_dir: Path) -> tuple[str, frozenset[str]]:
    """Return the pinned Oxlint version and its rule names as ``plugin/rule``."""
    inventory = as_object(json.loads((sources_dir / INVENTORY_FILE).read_text(encoding="utf-8")), INVENTORY_FILE)
    version = as_str(inventory.get("oxlint_version"), "oxlint_version")
    names: set[str] = set()
    for item in as_array(inventory.get("rules"), "rules"):
        rule = as_object(item, "rule")
        names.add(f"{as_str(rule.get('scope'), 'scope')}/{as_str(rule.get('rule'), 'rule')}")
    return version, frozenset(names)


def extra_outputs(sources_dir: Path) -> dict[str, str]:
    """Return ``oxlintrc.jsonc`` enabling every digest rule the pinned Oxlint has, naming the rest."""
    rules = parse_lint_digest((sources_dir / LINT_FILE).read_text(encoding="utf-8"))
    version, names = available_rules(sources_dir)
    enabled = [rule for rule in rules if rule.name in names]
    omitted = ", ".join(rule.name for rule in rules if rule.name not in names)
    plugins = sorted({_plugin(rule) for rule in enabled} - {"eslint"})
    entries = ",\n".join(f'    "{_config_name(rule)}": "{TIER_SEVERITY[rule.tier]}"' for rule in enabled)
    header = (
        "// Tier 1 (correctness, security; error) and Tier 2 (modernization, performance; warn) Oxlint rules.\n"
        f"// Generated by build/compile.py from sources/typescript/oxlint-rules.md, for Oxlint >= {version}.\n"
        "// Use it when the project has no Oxlint configuration:  oxlint -c <this file> <paths>\n"
        "// Type-aware rules run only with --type-aware.\n"
        f"// Omitted because Oxlint {version} does not have them: {omitted or 'none'}.\n"
    )
    plugin_list = ", ".join(f'"{plugin}"' for plugin in plugins)
    config = f'{{\n  "plugins": [{plugin_list}],\n  "rules": {{\n{entries}\n  }}\n}}\n'
    return {"oxlintrc.jsonc": header + config}


def _plugin(rule: LintRule) -> str:
    return rule.name.split("/", 1)[0].replace("_", "-")


def _config_name(rule: LintRule) -> str:
    plugin, name = rule.name.split("/", 1)
    return f"{plugin.replace('_', '-')}/{name}"


def check_vendored(sources_dir: Path, folder: Path) -> None:
    """Fail unless every digest rule has its doc and every framework file and style.md exist."""
    rules = parse_lint_digest((sources_dir / LINT_FILE).read_text(encoding="utf-8"))
    require_docs(rules, lambda rule: folder / "lint" / rule.name / "index.md")
    expected = ["style.md", *(f"frameworks/{name}.md" for name in FRAMEWORKS)]
    missing = [path for path in expected if not (folder / path).is_file()]
    if missing:
        raise MissingVendoredError(missing)
