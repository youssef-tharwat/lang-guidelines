---
type: regex
target: {source: file, path: orders.ts}
pattern: '\.map\(\s*parse(Int|Float)\s*\)'
match: not_contains
---

Rule `explicit-callbacks`.
