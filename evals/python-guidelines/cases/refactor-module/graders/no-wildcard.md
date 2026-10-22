---
type: regex
target: {source: file, path: report.py}
pattern: 'import\s+\*'
match: not_contains
---

Rule `import-modules`: no wildcard imports.
