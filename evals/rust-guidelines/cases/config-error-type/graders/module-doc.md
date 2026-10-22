---
type: regex
target: {source: file, path: lib.rs}
pattern: '^//!'
match: contains
flags: m
---

Rule `doc-public-items`: the crate root has `//!` module docs.
