---
type: regex
target: {source: file, path: orders.ts}
pattern: '@ts-(ignore|nocheck|expect-error)'
match: not_contains
---

Rule `type-check`.
