---
type: regex
target: {source: file, path: cart.ts}
pattern: '^\s*public\s'
match: not_contains
flags: m
---

Rule `visibility`: no redundant public.
