---
type: regex
target: {source: file, path: rate_limiter.py}
pattern: 'if\s+__name__\s*==\s*["\x27]__main__["\x27]'
match: contains
---

Rule `main-guard`.
