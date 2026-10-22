---
type: regex
target: {source: file, path: userClient.ts}
pattern: ':\s*any\b|<any>|as\s+any\b'
match: not_contains
---

Rule `no-any` (typescript/no-explicit-any).
