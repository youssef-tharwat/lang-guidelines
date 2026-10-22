---
type: regex
target: {source: file, path: report.rs}
pattern: 'fn get_name'
match: not_contains
---

Rule `method-names`: getters are named `name()`, not `get_name()`.
