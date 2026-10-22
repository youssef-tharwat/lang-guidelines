---
type: regex
target: {source: file, path: client.rs}
pattern: 'fn set_'
match: not_contains
---

Rule `builders`: setters are named `x()`, not `set_x()`.
