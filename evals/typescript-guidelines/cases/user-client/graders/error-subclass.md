---
type: regex
target: {source: file, path: userClient.ts}
pattern: 'class\s+\w+\s+extends\s+Error\b'
match: contains
---

Rule `throw-errors`: a custom Error subclass.
