# fast-hasher

Hash trusted, internal keys with a fast non-cryptographic hasher such as `foldhash` or `FxHash`; keep the default hasher for untrusted input.

**Why:** The default hasher pays for DoS resistance you may not need.

**Sources:** M-FAST-HASHER

---

## Use a fast hasher where possible (M-FAST-HASHER)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When hashing trusted, internal keys, prefer a fast non-cryptographic hasher (e.g., `foldhash`, `FxHash`) over the standard library default.

Rust's default hasher is reasonably DoS safe on untrusted user input, but this comes at a performance penalty. If you can trust that keys are not maliciously crafted to overflow individual buckets, a custom fast hasher can yield significant performance gains.

```rust
// Bad, uses default hasher for keys we control.
let lookup = HashMap::<UserID, Data>::with_capacity(1024);

// Good, uses faster foldhash for internal keys.
let lookup = foldhash::HashMap<UserID, Data>::with_capacity(1024);

```
