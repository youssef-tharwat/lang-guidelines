---
type: regex
target: {source: file, path: hashing.rs}
pattern: 'yield_now|spawn_blocking|block_in_place|rayon'
match: contains
---

Rule `yield-points`: CPU-bound work yields or leaves the async executor.
