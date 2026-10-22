---
type: regex
target: {source: file, path: ffi.rs}
pattern: '\.unwrap\(\)'
match: not_contains
---

Rule `error-contract`: nothing unwraps on input-dependent results at the boundary.
