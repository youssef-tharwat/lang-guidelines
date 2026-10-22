---
type: regex
target: {source: file, path: userClient.ts}
pattern: '\bvar\s'
match: not_contains
---

Rule `const-let` (eslint/no-var).
