---
type: regex
target: {source: file, path: report.py}
pattern: 'def\s+\w+\([^)]*=\s*(\[\]|\{\}|dict\(\)|list\(\))'
match: not_contains
---

Rule `no-mutable-defaults` (B006).
