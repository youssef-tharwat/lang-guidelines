---
type: regex
target: {source: file, path: config_loader.py}
pattern: 'class\s+\w*Error\s*\('
match: contains
---

Rule `exception-types`: custom exceptions end in Error.
