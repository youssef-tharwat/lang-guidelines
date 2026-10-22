# doc-inline-reexports

Mark re-exports of your own items `#[doc(inline)]`; the foreign items you may still re-export (`no-foreign-reexports`) go without it.

**Why:** Re-exported items then render like native ones.

**Sources:** M-DOC-INLINE

---

## Mark `pub use` items with `#[doc(inline)]` (M-DOC-INLINE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When publicly re-exporting crate items via `pub use foo::Foo` or `pub use foo::*`, they show up in an opaque re-export block. In most cases, this is not
helpful to the reader:

Instead, you should annotate them with `#[doc(inline)]` at the `use` site, for them to be inlined organically:

```rust
#[doc(inline)]
pub use foo::*;

// or

#[doc(inline)]
pub use foo::Foo;
```

This does not apply to `std` or 3rd party types; these should always be re-exported without inlining to make it clear they are external.

> ###  Still avoid glob exports
>
> The `#[doc(inline)]` trick above does not change M-NO-GLOB-REEXPORTS; you generally should not re-export items via wildcards.
