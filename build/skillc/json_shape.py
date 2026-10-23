# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""Narrow parsed JSON to the shapes a source file must have, failing loudly otherwise."""

from __future__ import annotations

from typing import TypeAlias

from .errors import BuildError

Json: TypeAlias = "dict[str, Json] | list[Json] | str | int | float | bool | None"


class JsonShapeError(BuildError):
    """A JSON source does not have the expected shape."""

    def __init__(self, where: str, expected: str) -> None:
        """Name the value and the shape it should have had."""
        super().__init__(f"{where}: expected {expected}")


def as_object(value: Json, where: str) -> dict[str, Json]:
    """Narrow ``value`` to a JSON object."""
    if not isinstance(value, dict):
        raise JsonShapeError(where, "an object")
    return value


def as_array(value: Json, where: str) -> list[Json]:
    """Narrow ``value`` to a JSON array."""
    if not isinstance(value, list):
        raise JsonShapeError(where, "an array")
    return value


def as_str(value: Json, where: str) -> str:
    """Narrow ``value`` to a JSON string."""
    if not isinstance(value, str):
        raise JsonShapeError(where, "a string")
    return value
