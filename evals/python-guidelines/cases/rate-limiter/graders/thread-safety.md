---
type: regex
target: {source: file, path: rate_limiter.py}
pattern: 'threading\.(Lock|RLock|Condition)|queue\.Queue'
match: contains
---

Rule `thread-communication`: shared state is guarded by threading primitives.
