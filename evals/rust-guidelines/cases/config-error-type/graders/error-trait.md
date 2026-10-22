---
type: regex
target: {source: file, path: lib.rs}
pattern: 'impl\s+(std::error::)?Error\s+for'
match: contains
---

Rule `library-errors`: the error implements `std::error::Error`.
