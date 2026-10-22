# error-contract

Return `Option` when absence is the only failure, `Result` when callers must tell failures apart, and `panic!` only for a detected bug or broken invariant, never for bad input, I/O or control flow.

**Why:** A panic means stop the program; it is not an exception.

**Sources:** G:reporting-errors, M-PANIC-IS-STOP, M-PANIC-ON-BUG

---

## Reporting errors (G:reporting-errors)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#reporting-errors), CC BY 3.0.

Choose the error reporting mechanism that fits your API contract: `Option`, `Result`, or `panic!`.

**Use `Option` for simple failures** where the cause is obvious and the caller would not benefit from further details. This is best for standard, anticipated outcomes like a missing value or a parsing mismatch.

✅ Good:

```rust
// Good: The cause of the failure is obvious (integer overflow). No further
// details could be reasonably provided.
fn checked_add(a: u32, b: u32) -> Option<u32> { ... }
```

**Use `Result` for recoverable failures where the caller needs context** to handle the error. These are often “unavoidable” errors caused by external factors (like I/O or network) that even correctly implemented code cannot prevent with checks ahead of time. Nevertheless, the caller can reasonably anticipate the kinds of errors (a file-related function can fail with an I/O error). The error details allow the caller to distinguish failure modes and recover appropriately.

✅ Good:

```rust
// Good: The caller needs to know *why* it failed (NotFound vs PermissionDenied).
fn open_file(path: &Path) -> Result<File, io::Error> { ... }
```

**Use `panic!` to report bugs and violated invariants.** These errors are avoidable: the program is missing a check, and is calling an operation without fulfilling a precondition. These defects must be fixed in the code, not handled at runtime, although coarse-grained recovery might be possible with `catch_unwind`.

✅ Good:

```rust
// Good: Panics if the invariant (index must be in bounds) is violated.
// This indicates a bug in the caller's logic.
impl<T> MyVec<T> {
    pub fn remove(&mut self, index: usize) -> T {
        if index >= self.len() {
            panic!("index out of bounds");
        }
        // ...
    }
}
```

Note: Some codebases may choose to avoid panics entirely, and require even broken invariants to be reported via `Result`.

Exceptions:

*   Developer-facing binaries may use panics for non-fatal errors.

*   Tests may use panics for assertions.


## Panic means 'stop the program' (M-PANIC-IS-STOP)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Panics are not exceptions. Instead, they suggest immediate program termination.

Although your code must be [panic-safe](https://doc.rust-lang.org/nomicon/exception-safety.html) (i.e., a survived panic may not lead to
inconsistent state), invoking a panic means _this program should stop now_. It is not valid to:

- use panics to communicate (errors) upstream,
- use panics to handle self-inflicted error conditions,
- assume panics will be caught, even by your own code.

For example, if the application calling you is compiled with a `Cargo.toml` containing

```toml
[profile.release]
panic = "abort"
```

then any invocation of panic will cause an otherwise functioning program to needlessly abort. Valid reasons to panic are:

- when encountering a programming error, e.g., `x.expect("must never happen")`,
- anything invoked from const contexts, e.g., `const { foo.unwrap() }`,
- when user requested, e.g., providing an `unwrap()` method yourself,
- when encountering a poison, e.g., by calling `unwrap()` on a lock result (a poisoned lock signals another thread has panicked already).

Any of those are directly or indirectly linked to programming errors.


## Detected programming bugs are panics, not errors (M-PANIC-ON-BUG)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

As an extension of M-PANIC-IS-STOP above, when an unrecoverable programming error has been
detected, libraries and applications must panic, i.e., request program termination.

In these cases, no `Error` type should be introduced or returned, as any such error could not be acted upon at runtime.

Contract violations, i.e., the breaking of invariants either within a library or by a caller, are programming errors and must therefore panic.

However, what constitutes a violation is situational. APIs are not expected to go out of their way to detect them, as such
checks can be impossible or expensive. Encountering `must_be_even == 3` during an already existing check clearly warrants
a panic, while a function `parse(&str)` clearly must return a `Result`. If in doubt, we recommend you take inspiration from the standard library.

```rust
// Generally, a function with bad parameters must either
// - Ignore a parameter and/or return the wrong result
// - Signal an issue via Result or similar
// - Panic
// If in this `divide_by` we see that y == 0, panicking is
// the correct approach.
fn divide_by(x: u32, y: u32) -> u32 { ... }

// However, it can also be permissible to omit such checks
// and return an unspecified (but not an undefined) result.
fn divide_by_fast(x: u32, y: u32) -> u32 { ... }

// Here, passing an invalid URI is not a contract violation.
// Since parsing is inherently fallible, a Result must be returned.
fn parse_uri(s: &str) -> Result<Uri, ParseError> { };

```

> ###  Make it 'Correct by Construction'
>
> While panicking on a detected programming error is the 'least bad option', your panic might still ruin someone's day.
> For any user input or calling sequence that would otherwise panic, you should also explore if you can use the type
> system to avoid panicking code paths altogether.
