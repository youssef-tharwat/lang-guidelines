---
description: An extern "C" export; tests unsafe hygiene, safety docs and FFI error handling.
tags: [unsafe, docs, errors]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Expose a Rust function to C. It takes a NUL-terminated C string holding a file path and returns the file's size in bytes, or a negative error code when the pointer is null, the path is not valid UTF-8, or the file can't be read. Write the Rust side, with the doc comments a C caller needs, to `ffi.rs` in the current directory; don't create other files.
