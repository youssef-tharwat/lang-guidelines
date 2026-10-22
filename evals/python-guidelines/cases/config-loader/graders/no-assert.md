---
type: regex
target: {source: file, path: config_loader.py}
pattern: '^\s*assert\b'
match: not_contains
flags: m
---

Rule `no-assert-validation` (S101): no assert for validation.
