---
type: regex
target: {source: file, path: report.rs}
pattern: '\.unwrap\(\)'
match: not_contains
---

Rule `expect-not-unwrap`: the check-then-unwrap becomes pattern matching.
