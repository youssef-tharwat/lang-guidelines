---
type: regex
target: {source: file, path: hashing.rs}
pattern: '(info|debug|trace|warn)!\(\s*"[^"]*\{[^{}]*\}'
match: not_contains
---

Rule `structured-logging`: no `{}`-interpolated log messages.
