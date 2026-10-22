# proc-macro-crates

Proc macros are thin shims in `foo_proc` that delegate to a tested `foo_proc_impl` library; they emit paths through the main crate `foo`, and reach third-party items through a `#[doc(hidden)] pub mod _private` re-export there.

**Why:** Logic stays unit-testable and users depend on one crate.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-PROC-IMPL, M-MACRO-MAIN-CRATE, M-MACRO-HELPERS

---

## Proc macros should have separate impl crate incl. tests (M-PROC-IMPL)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Proc macros should be thin shims inside some `foo_proc` crate that delegate to a separate, regular library crate, usually called `foo_proc_impl`, which contains the actual token-stream transformation logic and its tests.

As proc macro crates are special, testing them from `foo_proc` usually requires workarounds for unit and snapshot tests. Instead, consider having a `foo_proc_impl` crate:

```rust
use proc_macro2::TokenStream;

pub fn my_macro(attr: TokenStream, item: TokenStream) -> TokenStream { ... }
```

These can come with regular [insta](https://insta.rs/) or similar snapshot tests, and are then exported as genuine proc macros via a `foo_proc` crate like so:

```rust
#[proc_macro_attribute]
pub fn my_macro(attr: TokenStream, item: TokenStream) -> TokenStream {
    foo_proc_impl::my_macro(attr.into(), item.into()).into()
}
```

The macros are then re-exported from the core crate:

```rust
pub use foo_proc::my_macro;
```

Inside the core crate, we also recommend adding [trybuild](https://docs.rs/trybuild/latest/trybuild/) UI tests with negative examples to ensure consistent error messages.


## Macros assume main crate (M-MACRO-MAIN-CRATE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Procedural macros can (and should) assume they are used through their main crate and emit paths for that.

For crates including proc macros it is common to ship them split in 3 for technical reasons:

- `foo` - the main crate that re-exports macros from `foo_proc`, along with extra traits or types,
- `foo_proc` - facade re-exporting macros from `foo_proc_impl` with `proc-macro = true`,
- `foo_proc_impl` - the actual macro implementation and unit tests.

In some cases there can be additional crates involved. Authors might be tempted to make `foo`, `foo_proc`, and siblings all work, resulting in complex re-export hierarchies or the use of 3rd party helpers. In reality, the minimal UX gain is usually not worth the added complexity (or compile time overhead), given the ecosystem precedent of mostly not supporting these usage modes in the first place.

This also implies you should not attempt to support use cases where your crate is imported under a different name.


## Third party items come from hidden `_private` module (M-MACRO-HELPERS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When a macro expansion needs to refer to third-party items, the host crate should re-export those from a hidden module, and the macro should emit fully-qualified paths through that module rather than expecting the user's crate to depend on the third-party crate directly.

For example, a crate `foo` requiring `bar` traits would do:

```rust
#[doc(hidden)]
pub mod _private {
    pub use ::bar::Bar;
}

pub use foo_proc::my_macro;
```

The `my_macro!` implementation would then rely on its presence in its emitted code:

```rust
impl ::foo::_private::Bar for MyType { ... }
```
