---
type: regex
target: {source: file, path: client.rs}
pattern: 'Arc<'
match: contains
---

Rule `services-clone`: the shared client is a handle over an `Arc`.
