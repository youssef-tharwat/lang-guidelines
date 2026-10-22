---
type: regex
target: {source: file, path: config_loader.py}
pattern: 'except\s*:|except\s+(Exception|BaseException)\b'
match: not_contains
---

Rule `narrow-except` (BLE001): no bare or broad except.
