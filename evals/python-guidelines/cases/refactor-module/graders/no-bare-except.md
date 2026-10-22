---
type: regex
target: {source: file, path: report.py}
pattern: 'except\s*:'
match: not_contains
---

Rule `narrow-except`.
