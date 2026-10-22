---
type: regex
target: {source: file, path: report.py}
pattern: '(log|logger|logging)\.\w+\(\s*f["\x27]'
match: not_contains
---

Rule `lazy-logging` (G004).
