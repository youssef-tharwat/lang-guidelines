---
type: regex
target: {source: file, path: userClient.ts}
pattern: 'throw\s+[\x27"`{]'
match: not_contains
---

Rule `throw-errors`: never throw strings or objects.
