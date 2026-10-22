---
type: regex
target: {source: file, path: lib.rs}
pattern: 'Backtrace'
match: contains
---

Rule `library-errors`: the library error captures a `Backtrace`.
