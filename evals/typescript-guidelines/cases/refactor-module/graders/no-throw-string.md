---
type: regex
target: {source: file, path: orders.ts}
pattern: 'throw\s+[\x27"`]'
match: not_contains
---

Rule `throw-errors`.
