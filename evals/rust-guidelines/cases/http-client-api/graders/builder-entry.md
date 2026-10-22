---
type: regex
target: {source: file, path: client.rs}
pattern: 'fn builder\('
match: contains
---

Rule `builders`: construction starts at `Client::builder(...)`.
