---
type: llm
focus: {source: file, path: client.rs}
weight: 3
---

Judge the API in `client.rs`. Pass when ALL of these hold:

1. Construction goes through a builder: `Client::builder(...)` takes the required base URL and returns a builder whose chainable setters are named after the option (no `set_` prefix), finished by `build()`.
2. The client is a cheap `Clone` handle over shared state held in an `Arc` (or is documented and implemented as cheaply cloneable), so components clone it rather than wrap it in `Arc` themselves.
3. Public signatures do not expose `Arc`, `Rc`, `Box` or `Mutex` wrappers to callers.
4. No public type is named with `Service`, `Manager` or `Factory`.
5. The client is evidently `Send + Sync` (asserted, or every field is), so it can cross tokio tasks.
6. Failures use a dedicated error type, not `String` or `Box<dyn Error>`.
7. Public items have `///` docs.

Fail if any item is missing. List each item as met or not met before the verdict.
