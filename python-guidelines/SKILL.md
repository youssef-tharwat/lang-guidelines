---
name: python-guidelines
description: Enforce Python lint rules (Ruff) for all Python code generation and edits. Rules must be applied while writing code, not only in review. Triggers on any task that writes, edits, or refactors Python code.
---

# Python Development Guidelines

Every rule in `guidelines.txt` is a hard constraint. Apply them **while
writing code**, not only during review. Source: Ruff (docs.astral.sh/ruff).

## Reading protocol

Load files in this order; stop when the task's scope is satisfied.

1. **Always**: `guidelines.txt` — 642 correctness + security + modernization rules. Never skip.
2. **Always**: `idioms.md` — positive patterns (what to prefer, not just what to avoid).
3. **If reviewing / matching a project style guide**: `style.md` — 275 style/pedantic rules.
4. **Framework-gated**: `frameworks/<name>.md` — load only if the project's
   manifest (`pyproject.toml`, `requirements*.txt`) depends on or imports the named framework.

   - `frameworks/airflow.md` (11 rules)
   - `frameworks/django.md` (7 rules)
   - `frameworks/fastapi.md` (3 rules)
   - `frameworks/numpy.md` (4 rules)
   - `frameworks/pandas.md` (13 rules)
5. **On demand for edge cases**: `rules/<slug>/index.md` — full docs with
   additional examples, configuration, and references.

## Rule format

Each rule in the compiled files follows this shape:

```
### <slug> (<code>)
<imperative rule in one sentence>
❌ <minimal bad example>
✅ <minimal good example>
```

Treat the `✅` example as the canonical pattern. When a bad snippet appears in
code under edit, rewrite to the good snippet unless the user has explicitly
documented an exception.

## Compliance marker

After producing compliant code (only when the user has explicitly asked for a
compliance check), append:

```
# Python guideline compliant (Ruff)
```

## Hard rules

- Never ship a diff containing a Tier-1 violation.
- Do not silently lower standards. If a rule must be violated, surface it
  explicitly with a one-line rationale.
- When refactoring touched code, fix violations in-flight rather than
  preserving legacy patterns.
- Prefer each rule's `✅` example as the idiomatic pattern.
