---
type: regex
target: {source: file, path: userClient.ts}
pattern: 'export\s+default\b'
match: not_contains
---

Rule `named-exports` (import/no-default-export).
