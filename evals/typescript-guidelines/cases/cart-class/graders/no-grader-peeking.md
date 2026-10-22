---
type: regex
target: trace
pattern: 'evals/'
match: not_contains
arm: both
---

Guard: the agent never read the eval suite, which sits inside the plugin folder under test.
