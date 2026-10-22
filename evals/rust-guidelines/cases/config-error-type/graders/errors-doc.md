---
type: regex
target: {source: file, path: lib.rs}
pattern: '# Errors'
match: contains
---

Rule `doc-public-items`: fallible public functions document `# Errors`.
