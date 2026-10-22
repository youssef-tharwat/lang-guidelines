---
description: CPU-bound work inside an async service; tests yield points and structured logging.
tags: [async, logging]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

In our tokio-based service, write an async function that computes the SHA-256 digest (use the `sha2` crate) of every blob in a batch that can hold hundreds of thousands of large blobs, and logs one event per blob with its index and hex digest using `tracing`. Return the digests in order. Write it to `hashing.rs` in the current directory; don't create other files.
