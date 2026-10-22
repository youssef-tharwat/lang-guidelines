---
type: regex
target: {source: file, path: ffi.rs}
pattern: 'SAFETY:'
match: contains
---

Rule `unsafe-justified`: unsafe blocks carry `// SAFETY:` comments.
