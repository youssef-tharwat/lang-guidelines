---
type: regex
target: {source: file, path: config_loader.py}
pattern: 'with\s+(open|[\w.]+\.open)\(|\.read_(text|bytes)\('
match: contains
---

Rule `with-resources` (SIM115): files are opened in a `with` block, or read whole with `Path.read_text()`/`read_bytes()`, which leave nothing open.
