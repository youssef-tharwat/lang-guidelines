---
type: llm
focus: {source: file, path: report.py}
weight: 3
---

Judge the refactored module in `report.py`. Pass when ALL of these hold:

1. `add_row` no longer uses a mutable default argument.
2. The wildcard import is gone; imports are one per line and import modules (or explicit names).
3. The pass-through `rows` property/setter pair is replaced by a plain public attribute (or a property only if it adds logic).
4. `header` is a module-level function rather than a `staticmethod`.
5. Strings are built with f-strings/`.format()`/`join`, not `+` chains or `+=` in loops.
6. Emptiness uses implicit truth (`if not report.rows:`); dictionaries are iterated directly or with `.items()`.
7. Logging uses a constant pattern with arguments, not an f-string.
8. `save` validates `path` by raising (not `assert`), writes with a `with` block or `Path.write_text()`, and does not swallow exceptions with a bare `except`.

Fail if any item is missing. List each item as met or not met before the verdict.
