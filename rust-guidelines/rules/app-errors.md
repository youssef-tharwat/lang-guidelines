# app-errors

Application crates, and crates only the application uses, may use one app-level error type such as `ohno::AppError`, `anyhow` or `eyre` throughout; don't mix several.

**Why:** Nobody matches on these errors; context matters more than variants.

**Binding in:** applications only.

**Sources:** M-APP-ERROR

---

## Applications may use Anyhow or derivatives (M-APP-ERROR)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

> Note, this guideline is primarily a relaxation and clarification of M-ERRORS-CANONICAL-STRUCTS.

Applications, and crates in your own repository exclusively used from your application, may use [ohno::AppError](https://docs.rs/crate/ohno/latest#structs), [anyhow](https://github.com/dtolnay/anyhow),
[eyre](https://github.com/eyre-rs/eyre) or similar application-level error crates instead of implementing their own types.

For example, in your application crates you may just re-export and use eyre's common `Result` type, which should be able to automatically
handle all third party library errors, in particular the ones following
M-ERRORS-CANONICAL-STRUCTS.

```rust
use ohno::AppError;

fn start_application() -> Result<(), AppError> {
    start_server()?;
    Ok(())
}
```

Once you selected your application error crate you should switch all application-level errors to that type, and you should not mix multiple
application-level error types.

Libraries (crates used by more than one crate) should always follow M-ERRORS-CANONICAL-STRUCTS instead.
