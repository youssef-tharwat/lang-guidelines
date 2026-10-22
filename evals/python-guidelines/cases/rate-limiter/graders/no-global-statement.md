---
type: regex
target: {source: file, path: rate_limiter.py}
pattern: '^\s*global\s'
match: not_contains
flags: m
---

Rule `global-state`: no global statements.
