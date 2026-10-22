---
type: regex
target: {source: file, path: client.rs}
pattern: '#\[derive\([^)]*\bClone\b|impl Clone for'
match: contains
---

Rule `services-clone`: the client implements `Clone`.
