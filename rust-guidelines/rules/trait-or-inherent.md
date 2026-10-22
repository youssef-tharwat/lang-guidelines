# trait-or-inherent

Define a trait only for generic bounds, `impl Trait`/`dyn Trait`, or an extension; implement core functionality as inherent methods and have trait impls forward to them. Don't use traits to organize code.

**Why:** Callers find methods without importing traits.

**Sources:** G:when-to-define-a-trait-versus-an-inherent-implementation, M-ESSENTIAL-FN-INHERENT

---

## When to define a trait versus an inherent implementation (G:when-to-define-a-trait-versus-an-inherent-implementation)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#when-to-define-a-trait-versus-an-inherent-implementation), CC BY 3.0.

Define a trait only for the following purposes:

*   To enable generic programming (to use `T: Trait` in constraints of generic functions and types).

*   To accept or return an `impl Trait` or `dyn Trait`.

*   To define an extension trait (but see also the caveats in the section on extension traits).

In all other cases where you want to implement functionality for a type, use an [inherent implementation](https://doc.rust-lang.org/std/keyword.impl.html#inherent-implementations).

Don’t use traits merely to organize code.


## Essential functionality should be inherent (M-ESSENTIAL-FN-INHERENT)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Types should implement core functionality inherently. Trait implementations should forward to inherent functions, and not replace them. Instead of this

```rust
struct HttpClient {}

// Offloading essential functionality into traits means users
// will have to figure out what other traits to `use` to
// actually use this type.
impl Download for HttpClient {
    fn download_file(&self, url: impl AsRef<str>) {
        // ... logic to download a file
    }
}
```

do this:

```rust
struct HttpClient {}

impl HttpClient {
    fn download_file(&self, url: impl AsRef<str>) {
        // ... logic to download a file
    }
}

// Forward calls to inherent impls. `HttpClient` can be used
impl Download for HttpClient {
    fn download_file(&self, url: impl AsRef<str>) {
        Self::download_file(self, url)
    }
}
```
