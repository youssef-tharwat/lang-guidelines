---
type: regex
target: {source: file, path: orders.ts}
pattern: 'for\s*\(\s*(const|let|var)\s+\w+\s+in\s'
match: not_contains
---

Rule `braces-and-loops`: no for...in over arrays.
