---
type: regex
target: {source: file, path: client.rs}
pattern: 'fn build\('
match: contains
---

Rule `builders`: the builder finishes with `.build()`.
