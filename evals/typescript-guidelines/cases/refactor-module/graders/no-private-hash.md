---
type: regex
target: {source: file, path: orders.ts}
pattern: '#\w+'
match: not_contains
---

Rule `class-members`: no #private fields.
