---
type: regex
target: {source: file, path: report.py}
pattern: 'len\([^)]*\)\s*==\s*0'
match: not_contains
---

Rule `implicit-false`.
