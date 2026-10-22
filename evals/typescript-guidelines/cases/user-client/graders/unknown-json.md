---
type: regex
target: {source: file, path: userClient.ts}
pattern: '\bunknown\b'
match: contains
---

Pattern `runtime-validation` / rule `no-any`: untrusted JSON is unknown until checked.
