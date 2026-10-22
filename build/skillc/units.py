"""The upstream text model every parser produces and every renderer consumes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    """One upstream publication and the terms it is redistributed under."""

    title: str
    license: str
    home: str


@dataclass(frozen=True)
class Unit:
    """One addressable section of an upstream source (a guideline, a style rule, a pattern page)."""

    unit_id: str
    title: str
    url: str
    body: str
    source: Source
