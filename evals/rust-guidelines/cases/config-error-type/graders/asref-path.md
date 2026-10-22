---
type: regex
target: {source: file, path: lib.rs}
pattern: 'AsRef<(std::path::)?Path>'
match: contains
---

Rule `asref-params`: `load` accepts `impl AsRef<Path>`.
