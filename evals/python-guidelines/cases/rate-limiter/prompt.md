---
description: Thread-safe shared state; tests threading, global state, classes and docs.
tags: [resources, classes, docs]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Write a Python module `rate_limiter.py` providing a token-bucket rate limiter that many threads in one process share: callers ask whether an operation identified by a string key may proceed now, with a configurable rate and burst size per limiter. Include type annotations and docstrings, and a small command-line entry point that runs a demo. Write it to `rate_limiter.py` in the current directory; don't create other files.
