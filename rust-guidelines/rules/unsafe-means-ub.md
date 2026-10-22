# unsafe-means-ub

Mark a function `unsafe` only when misuse can cause undefined behavior, not because it is merely dangerous.

**Why:** Keeps `unsafe` meaningful.

**Sources:** M-UNSAFE-IMPLIES-UB

---

## Unsafe implies undefined behavior (M-UNSAFE-IMPLIES-UB)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

The marker `unsafe` may only be applied to functions and traits if misuse implies the risk of undefined behavior (UB).
It must not be used to mark functions that are dangerous to call for other reasons.

```rust
// Valid use of unsafe
unsafe fn print_string(x: *const String) { }

// Invalid use of unsafe
unsafe fn delete_database() { }
```
