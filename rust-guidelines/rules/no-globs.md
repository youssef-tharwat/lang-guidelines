# no-globs

No glob imports or re-exports, and no `prelude` modules; re-export items by name (`pub use foo::{A, B};`). Allowed: `use super::*` in inline test modules, `use Enum::*` inside an enum-focused function, cfg-gated platform re-exports. This overrides Google's allowance for `pub use x::*` in non-leaf modules.

**Why:** Globs leak items, collide across crates and hide where names come from.

**Sources:** M-NO-GLOB-REEXPORTS, M-NO-PRELUDE, G:dont-use-glob-imports

---

## Don't glob re-export items (M-NO-GLOB-REEXPORTS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Don't `pub use foo::*` from other modules, especially not from other crates. You might accidentally export more than you want,
and globs are hard to review in PRs. Re-export items individually instead:

```rust
pub use foo::{A, B, C};
```

Glob exports are permissible for technical reasons, like doing platform specific re-exports from a set of HAL (hardware abstraction layer) modules:

```rust
#[cfg(target_os = "windows")]
mod windows { /* ... */ }

#[cfg(target_os = "linux")]
mod linux { /* ... */ }

// Acceptable use of glob re-exports, this is a common pattern
// and it is clear everything is just forwarded from a single 
// platform.

#[cfg(target_os = "windows")]
pub use windows::*;

#[cfg(target_os = "linux")]
pub use linux::*;
```


## Don't define preludes (M-NO-PRELUDE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Crates must not define a `prelude` or any namespace intended to be imported as `use foo::*`.

While the Rust Standard Library successfully uses [preludes](https://doc.rust-lang.org/std/prelude/index.html) to define edition items, preludes in crates cause more harm than good. Given today's IDE support they are not needed, and once multiple preludes are used from different crates there is potential for conflicts:

```rust
use foo::prelude::*;
use bar::prelude::*;
use baz::prelude::*;

_ = Client::new();

// error[E0659]: `Client` is ambiguous
//   --> src/lib.rs:17:13
//    |
// 17 |     _ = Client; 
//    |         ^^^^^^ ambiguous name
//    |
//    = note: ambiguous because of multiple glob imports of a name in the same module
```

Preludes in particular do not resolve bad module design. If it looks like a prelude would make the crate easier to use or understand, this is almost always an indication that the existing module system needs restructuring, see M-BALANCED-MODULES.


## Don’t use glob imports (G:dont-use-glob-imports)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#dont-use-glob-imports), CC BY 3.0.

Don’t use glob imports, except in the following situations where you may optionally do so at your own discretion:

*   `use super::*` for inline modules

*   `use enum::*` in method bodies of enums, and functions that are primarily dealing with that enum

*   `pub use submodule::*` for non-leaf modules

*   C++ interop: Since the same namespace (in C++) is a submodule in different Rust crates (in Rust), you may merge the namespaces into a private copy using glob imports. For example:

    ```rust
    mod absl {
        pub use status::absl::*;
        pub use strings::absl::*;
    }
    ```

    In this hypothetical example, you can use `absl::Status` and `absl::StrCat` from Rust, the same way you would from C++, instead of spelling them as `status::absl::Status` and `strings::absl::StrCat`.

    This must only be used for merging C++ namespaces, and the resulting merged module must not be public.

If using third-party crates that encourage a prelude, it is up to the reviewer’s discretion to allow it.

This also means that defining preludes should be avoided.

**Rationale**

Glob imports increase toil for code janitors running LSCs, and make it harder to know where a type comes from in contexts without xrefs.
