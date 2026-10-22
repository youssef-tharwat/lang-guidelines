---
type: regex
target: {source: file, path: hashing.rs}
pattern: '(info|debug|trace|event)!\(\s*(name:\s*"|[a-z_.]+\s*=|%|\?|[a-z_]+\s*,)'
match: contains
---

Rule `structured-logging`: events carry fields, not just a formatted string.
