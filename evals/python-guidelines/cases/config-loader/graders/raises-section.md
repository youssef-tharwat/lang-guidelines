---
type: regex
target: {source: file, path: config_loader.py}
pattern: 'Raises:'
match: contains
---

Rule `docstrings`: fallible functions document Raises.
