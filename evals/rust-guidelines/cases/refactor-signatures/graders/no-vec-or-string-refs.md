---
type: regex
target: {source: file, path: report.rs}
pattern: '&Vec<|&String\b'
match: not_contains
---

Rule `borrowed-params`: parameters and return types take `&[T]` and `&str`, not `&Vec<T>` or `&String`.
