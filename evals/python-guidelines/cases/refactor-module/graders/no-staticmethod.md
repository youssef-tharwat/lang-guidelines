---
type: regex
target: {source: file, path: report.py}
pattern: '@staticmethod'
match: not_contains
---

Rule `decorators`: no staticmethod.
