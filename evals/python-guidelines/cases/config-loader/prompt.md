---
description: Library module with a fallible loader; tests exceptions, resources, logging and docstrings.
tags: [errors, resources, docs]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Write a Python module `config_loader.py` for a library that several of our services import. It provides `load(path)`, which reads a file of `key = value` lines (blank lines and lines starting with `#` are skipped) into a mapping, and fails on I/O errors, malformed lines and duplicate keys. Log each skipped comment line at debug level. Include the module's exception types, type annotations and docstrings. Write it to `config_loader.py` in the current directory; don't create other files.
