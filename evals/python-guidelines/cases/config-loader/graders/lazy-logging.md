---
type: regex
target: {source: file, path: config_loader.py}
pattern: '(log|logger|logging|LOGGER|_LOGGER|_logger)\.(debug|info|warning|error|exception)\(\s*f["\x27]'
match: not_contains
---

Rule `lazy-logging` (G004): no f-strings in logging calls.
