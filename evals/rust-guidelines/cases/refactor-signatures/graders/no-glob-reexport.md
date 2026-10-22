---
type: regex
target: {source: file, path: report.rs}
pattern: 'pub use [\w:]+::\*'
match: not_contains
---

Rule `no-globs`: no `pub use x::*` re-exports.
