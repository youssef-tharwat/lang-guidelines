---
description: Library crate with a fallible loader; tests error-type design, path parameters and docs.
tags: [errors, signatures, docs]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

I'm writing `config-loader`, a library crate that several other crates in our workspace depend on. Write its library root to `lib.rs` in the current directory: a `load` function that reads a file of `key = value` lines into a `Config` (keys mapped to values) and fails on I/O errors, malformed lines and duplicate keys. Include the error type and documentation. Don't create other files.
