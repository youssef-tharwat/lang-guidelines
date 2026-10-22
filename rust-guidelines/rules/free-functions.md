# free-functions

Functionality that needs no receiver is a free function, not an associated function; associated functions are for construction.

**Why:** Free functions are first-class in Rust.

**Sources:** M-REGULAR-FN

---

## Prefer regular over associated functions (M-REGULAR-FN)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Associated functions should primarily be used for instance creation, not general purpose computation.

In contrast to some OO languages, regular functions are first-class citizens in Rust and need no module or _class_ to host them. Functionality that
does not clearly belong to a receiver should therefore not reside in a type's `impl` block:

```rust
struct Database {}

impl Database {
    // Ok, associated function creates an instance
    fn new() -> Self {}

    // Ok, regular method with `&self` as receiver
    fn query(&self) {}

    // Not ok, this function is not directly related to `Database`,
    // it should therefore not live under `Database` as an associated
    // function.
    fn check_parameters(p: &str) {}
}

// As a regular function this is fine
fn check_parameters(p: &str) {}
```

Regular functions are more idiomatic, and reduce unnecessary noise on the caller side. Associated trait functions are perfectly idiomatic though:

```rust
pub trait Default {
    fn default() -> Self;
}

struct Foo;

impl Default for Foo {
    fn default() -> Self { Self }
}
```
