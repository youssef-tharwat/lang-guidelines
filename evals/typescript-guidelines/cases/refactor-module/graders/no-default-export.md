---
type: regex
target: {source: file, path: orders.ts}
pattern: 'export\s+default\b'
match: not_contains
---

Rule `named-exports`.
