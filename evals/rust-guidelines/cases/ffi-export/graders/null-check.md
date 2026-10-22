---
type: regex
target: {source: file, path: ffi.rs}
pattern: 'is_null\(\)'
match: contains
---

Null pointers are rejected before use.
