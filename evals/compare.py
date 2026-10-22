#!/usr/bin/env python3
"""Compare two ``claude plugin eval`` runs of a skill: the no-skill baseline, before, and after.

    python3 evals/compare.py <before/aggregate-result.json> <after/aggregate-result.json>

The before run must include the no-skill arm (``--ablation with-without``). Token counts
come from each run's trace (its final ``result`` record); a run whose trace is gone
reports no tokens rather than a guess.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import TypeAlias

Json: TypeAlias = "dict[str, Json] | list[Json] | str | int | float | bool | None"


class ResultShapeError(Exception):
    """An eval result file does not have the expected shape."""

    def __init__(self, where: str, expected: str) -> None:
        """Name the value and the shape it should have had."""
        super().__init__(f"{where}: expected {expected}")


def as_object(value: Json, where: str) -> dict[str, Json]:
    """Narrow ``value`` to a JSON object."""
    if not isinstance(value, dict):
        raise ResultShapeError(where, "an object")
    return value


def as_array(value: Json, where: str) -> list[Json]:
    """Narrow ``value`` to a JSON array."""
    if not isinstance(value, list):
        raise ResultShapeError(where, "an array")
    return value


def as_number(value: Json, where: str) -> float:
    """Narrow ``value`` to a JSON number."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ResultShapeError(where, "a number")
    return float(value)


@dataclass(frozen=True)
class Run:
    """One agent run of one case in one arm."""

    score: float
    cost_usd: float
    turns: float
    skill_fired: bool | None
    peeked: bool
    reads: int | None
    input_tokens: int | None
    output_tokens: int | None


@dataclass(frozen=True)
class Trace:
    """What the run's trace says about its token use and file reads."""

    reads: int
    input_tokens: int
    output_tokens: int


def read_trace(path: Path) -> Trace | None:
    """Sum Read calls and take the final usage totals, or ``None`` when the trace is gone."""
    if not path.is_file():
        return None
    reads = 0
    usage: dict[str, Json] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        record = as_object(json.loads(line), str(path))
        if record.get("type") == "result":
            usage = as_object(record.get("usage"), f"{path}: usage")
        if record.get("type") == "assistant":
            content = as_array(as_object(record.get("message"), "message").get("content"), "content")
            reads += sum(1 for block in content if isinstance(block, dict) and block.get("name") == "Read")
    input_keys = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
    return Trace(
        reads=reads,
        input_tokens=int(sum(as_number(usage.get(key, 0), key) for key in input_keys)),
        output_tokens=int(as_number(usage.get("output_tokens", 0), "output_tokens")),
    )


def grader_passed(run: dict[str, Json], name: str) -> bool | None:
    """Return whether the named grader passed in ``run``, or ``None`` when it did not run."""
    for grader in as_array(run.get("graders"), "graders"):
        entry = as_object(grader, "grader")
        if entry.get("name") == name:
            return entry.get("passed") is True
    return None


def parse_run(raw: Json) -> Run:
    """Build a ``Run`` from one entry of a case's ``arms`` lists."""
    run = as_object(raw, "run")
    trace_path = run.get("tracePath")
    trace = read_trace(Path(trace_path)) if isinstance(trace_path, str) else None
    return Run(
        score=as_number(run.get("score"), "score"),
        cost_usd=as_number(run.get("costUsd"), "costUsd"),
        turns=as_number(run.get("turns"), "turns"),
        skill_fired=grader_passed(run, "skill-fired"),
        peeked=grader_passed(run, "no-grader-peeking") is False,
        reads=trace.reads if trace else None,
        input_tokens=trace.input_tokens if trace else None,
        output_tokens=trace.output_tokens if trace else None,
    )


def load_arms(path: Path, arm: str) -> dict[str, list[Run]]:
    """Map each case name to its runs in ``arm`` (``with`` or ``without``)."""
    result = as_object(json.loads(path.read_text(encoding="utf-8")), str(path))
    runs_by_case: dict[str, list[Run]] = {}
    for raw_case in as_array(result.get("cases"), "cases"):
        case = as_object(raw_case, "case")
        arms = as_object(case.get("arms"), "arms")
        runs_by_case[str(case.get("name"))] = [parse_run(run) for run in as_array(arms.get(arm), arm)]
    return runs_by_case


def average(values: list[float]) -> str:
    """Format a mean, or a dash when there is nothing to average."""
    return f"{mean(values):,.2f}" if values else "-"


def row(label: str, runs: list[Run]) -> str:
    """One Markdown table row summarizing ``runs``."""
    fired = [1.0 if run.skill_fired else 0.0 for run in runs if run.skill_fired is not None]
    cells = [
        label,
        str(len(runs)),
        average([run.score for run in runs]),
        average([run.input_tokens for run in runs if run.input_tokens is not None]),
        average([run.output_tokens for run in runs if run.output_tokens is not None]),
        average([run.reads for run in runs if run.reads is not None]),
        average([run.turns for run in runs]),
        average([run.cost_usd for run in runs]),
        average(fired),
        str(sum(run.peeked for run in runs)),
    ]
    return "| " + " | ".join(cells) + " |"


HEADER = (
    "| arm | runs | score | input tokens | output tokens | Read calls | turns | cost USD | skill fired | peeked |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
)


def main() -> int:
    """Print one table per case and an overall table."""
    before_path, after_path = (Path(argument) for argument in sys.argv[1:3])
    arms = {
        "no skill": load_arms(before_path, "without"),
        "before": load_arms(before_path, "with"),
        "after": load_arms(after_path, "with"),
    }
    cases = sorted(arms["before"])
    sections = [
        f"### {case}\n\n{HEADER}\n" + "\n".join(row(name, runs.get(case, [])) for name, runs in arms.items())
        for case in cases
    ]
    overall = "\n".join(
        row(name, [run for case_runs in runs.values() for run in case_runs]) for name, runs in arms.items()
    )
    sys.stdout.write("\n\n".join([*sections, f"### overall\n\n{HEADER}\n{overall}"]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
