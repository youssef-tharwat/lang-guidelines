---
type: regex
target: {source: file, path: orders.ts}
pattern: 'new\s+Array\s*\('
match: not_contains
---

Rule `array-literals`.
