---
type: regex
target: {source: file, path: report.py}
pattern: '^\s*assert\b'
match: not_contains
flags: m
---

Rule `no-assert-validation`.
