---
type: regex
target: {source: file, path: cart.ts}
pattern: '#\w+\s*[=:;(]'
match: not_contains
---

Rule `class-members`: TypeScript private, not #private.
