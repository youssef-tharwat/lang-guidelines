---
type: regex
target: {source: file, path: report.rs}
pattern: 'verbose: bool'
match: not_contains
---

Rule `enum-not-bool`: the unclear `verbose: bool` parameter becomes a two-variant enum.
