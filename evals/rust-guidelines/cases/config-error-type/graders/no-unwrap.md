---
type: regex
target: {source: file, path: lib.rs}
pattern: '\.unwrap\(\)'
match: not_contains
---

Rule `error-contract`: no unwrap on input-dependent results.
