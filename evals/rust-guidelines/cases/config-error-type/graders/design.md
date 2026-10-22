---
type: llm
focus: {source: file, path: lib.rs}
weight: 3
---

Judge the library root in `lib.rs`. Pass when ALL of these hold:

1. `load` accepts `impl AsRef<Path>` (or a generic bounded by `AsRef<Path>`).
2. The public error type is a struct, not a public enum that exposes every failure variant; any kind enum is private and callers distinguish failures through methods such as `is_io()`/`is_malformed()` or accessors.
3. The error captures a `std::backtrace::Backtrace`.
4. The error implements `Debug`, `Display` and `std::error::Error`, exposing the I/O cause through `source()`.
5. The crate root has `//!` docs, and public items have `///` docs; `load` documents its failures under `# Errors`.
6. Bad input never panics: no `unwrap()`/`expect()` on results that depend on the file's content or I/O.

Fail if any item is missing. List each item as met or not met before the verdict.
