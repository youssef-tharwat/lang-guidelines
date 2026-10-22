---
description: Public API of a shared async client; tests builders, shared ownership, naming and Send.
tags: [types, ownership, naming, traits]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Design the public API of a library crate that wraps a REST user-directory service. Constructing the client needs a base URL (required) and, optionally, a timeout, a retry count, a user agent and a proxy URL. One client will be shared by many tokio tasks and components across the application. Write the public types and function signatures, with doc comments, to `client.rs` in the current directory; method bodies may be `todo!()`. Don't create other files.
