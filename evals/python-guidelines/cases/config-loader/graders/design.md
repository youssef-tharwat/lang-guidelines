---
type: llm
focus: {source: file, path: config_loader.py}
weight: 3
---

Judge the module in `config_loader.py`. Pass when ALL of these hold:

1. Library exceptions subclass a built-in exception, end in `Error`, and don't repeat the module name.
2. No bare `except:` and no `except Exception` unless it re-raises; `try` blocks are minimal.
3. The file is opened with a `with` block, or read whole with `Path.read_text()`/`read_bytes()`.
4. Logging calls pass a constant pattern string plus arguments (`logger.debug('Skipped %s', line)`), not f-strings.
5. Public functions and classes have docstrings; `load` documents `Args:`, `Returns:` and `Raises:`.
6. Parameters and return types are annotated; anything nullable is written `X | None`; parameters use abstract or path-like types where sensible.
7. No `assert` is used to validate input.

Fail if any item is missing. List each item as met or not met before the verdict.
