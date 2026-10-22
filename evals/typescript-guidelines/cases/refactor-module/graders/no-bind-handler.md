---
type: regex
target: {source: file, path: orders.ts}
pattern: '\.bind\(\s*this\s*\)'
match: not_contains
---

Rule `this-usage`.
