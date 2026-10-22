#!/usr/bin/env python3
"""Compile a skill folder from its upstream sources and its manifest.

    python3 build/compile.py rust           # regenerate rust-guidelines/ (likewise python, typescript)
    python3 build/compile.py rust --check   # exit 1 when rust-guidelines/ is stale

Inputs: ``sources/<language>/`` (upstream text) and ``build/<language>/`` (``manifest.toml`` plus
``SKILL.template.md``). The compiler owns every file in the skill folder except the paths a skill
declares as vendored (its lint docs, style and framework digests), which it only verifies.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from skillc import manifest, python, render, rust, typescript
from skillc.errors import BuildError

if TYPE_CHECKING:
    from collections.abc import Callable

    from skillc.units import Unit

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class SkillConfig:
    """Where a language's skill lives, how its sources are parsed, and which paths it vendors.

    Vendored paths (a file, or a directory and everything under it) are produced by another
    pipeline and committed as-is; the compiler never writes or deletes them, and
    ``check_vendored(sources, folder)`` verifies they still match what the sources expect.
    """

    folder: str
    load_units: Callable[[Path], list[Unit]]
    extra_outputs: Callable[[Path], dict[str, str]]
    vendored: tuple[str, ...] = ()
    check_vendored: Callable[[Path, Path], None] | None = None

    def is_vendored(self, path: str) -> bool:
        """Whether ``path`` (relative to the skill folder) belongs to a vendored file or directory."""
        return any(path == vendored or path.startswith(f"{vendored}/") for vendored in self.vendored)


SKILLS = {
    "rust": SkillConfig(folder="rust-guidelines", load_units=rust.load_units, extra_outputs=rust.extra_outputs),
    "python": SkillConfig(
        folder="python-guidelines",
        load_units=python.load_units,
        extra_outputs=python.extra_outputs,
        vendored=python.VENDORED,
        check_vendored=python.check_vendored,
    ),
    "typescript": SkillConfig(
        folder="typescript-guidelines",
        load_units=typescript.load_units,
        extra_outputs=typescript.extra_outputs,
        vendored=typescript.VENDORED,
        check_vendored=typescript.check_vendored,
    ),
}


class VendoredOutputError(BuildError):
    """The compiler was about to write a path the skill declares as vendored."""

    def __init__(self, paths: list[str]) -> None:
        """Name every vendored path the outputs collide with."""
        super().__init__(f"generated outputs collide with vendored paths: {', '.join(paths)}")


class UnexpectedFilesError(BuildError):
    """The skill folder holds files the compiler neither produces nor vendors."""

    def __init__(self, folder: Path, paths: list[str]) -> None:
        """Name the folder and every file that should not be there."""
        super().__init__(f"{folder.name} holds files the compiler does not produce: {', '.join(paths)}")


def compile_skill(language: str) -> tuple[Path, dict[str, str]]:
    """Return the skill folder and every file the compiler owns in it."""
    config = SKILLS[language]
    sources = ROOT / "sources" / language
    inputs = ROOT / "build" / language
    folder = ROOT / config.folder
    units = config.load_units(sources)
    mapping = manifest.load(inputs / "manifest.toml", units)
    template = (inputs / "SKILL.template.md").read_text(encoding="utf-8")
    outputs = render.render_outputs(mapping, units, template) | config.extra_outputs(sources)
    collisions = sorted(path for path in outputs if config.is_vendored(path))
    if collisions:
        raise VendoredOutputError(collisions)
    if config.check_vendored:
        config.check_vendored(sources, folder)
    return folder, outputs


def owned_files_on_disk(language: str) -> set[str]:
    """Every non-hidden, non-vendored file in the skill folder, as a folder-relative POSIX path."""
    config = SKILLS[language]
    folder = ROOT / config.folder
    relative = (path.relative_to(folder).as_posix() for path in folder.rglob("*") if path.is_file())
    return {path for path in relative if not path.rsplit("/", 1)[-1].startswith(".") and not config.is_vendored(path)}


def stale_paths(language: str, folder: Path, outputs: dict[str, str]) -> list[str]:
    """Paths whose content differs from the compiled output, plus owned files the compiler does not produce."""
    changed = [
        path
        for path, text in outputs.items()
        if not (folder / path).is_file() or (folder / path).read_text(encoding="utf-8") != text
    ]
    unexpected = [f"{path} (not generated)" for path in sorted(owned_files_on_disk(language) - outputs.keys())]
    return sorted(changed) + unexpected


def write(language: str, folder: Path, outputs: dict[str, str]) -> None:
    """Replace the generated directories and files, refusing to leave hand-made files behind."""
    for directory in sorted({path.split("/", 1)[0] for path in outputs if "/" in path}):
        if (folder / directory).exists():
            shutil.rmtree(folder / directory)
    for path, text in outputs.items():
        destination = folder / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    unexpected = sorted(owned_files_on_disk(language) - outputs.keys())
    if unexpected:
        raise UnexpectedFilesError(folder, unexpected)


def summary(folder: Path, outputs: dict[str, str]) -> str:
    """Sizes of what a model reads; tokens are estimated as bytes / 4."""
    skill_bytes = len(outputs["SKILL.md"].encode())
    rules = sum(1 for path in outputs if path.startswith("rules/"))
    patterns = sum(1 for path in outputs if path.startswith("patterns/"))
    return (
        f"{folder.name}: SKILL.md {skill_bytes} bytes (~{skill_bytes // 4} tokens, estimate), "
        f"{rules} rule files, {patterns} pattern files"
    )


def main() -> int:
    """Compile or check the requested skill."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("language", choices=sorted(SKILLS))
    parser.add_argument("--check", action="store_true", help="exit 1 if the committed skill folder is stale")
    arguments = parser.parse_args()
    try:
        folder, outputs = compile_skill(arguments.language)
        if arguments.check:
            stale = stale_paths(arguments.language, folder, outputs)
            sys.stdout.write("\n".join(stale) + "\n" if stale else f"{folder.name} is up to date\n")
            return 1 if stale else 0
        write(arguments.language, folder, outputs)
    except BuildError as error:
        sys.stderr.write(f"{error}\n")
        return 1
    sys.stdout.write(summary(folder, outputs) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
