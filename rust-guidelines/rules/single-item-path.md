# single-item-path

Make each public item reachable through exactly one public path: re-export from a private (`pub(crate)`) module, never from a public one, and don't keep old paths alive after a refactor.

**Why:** Duplicate paths confuse users and agents and outlive their reason.

**Sources:** M-SINGLE-ITEM-PATH

---

## Items are only visible through one path (M-SINGLE-ITEM-PATH)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Public items within a crate should be reachable only through one path. For example some `crate::db::Connection` should not also be visible as `crate::Connection`:

```rust
// Not OK
pub mod db {
    pub struct Connection;
}

pub use db::Connection;
```

This rule is often violated by agents creating or refactoring large code bases over several iterations. In an attempt to _simplify_ their task, they re-export items under multiple paths, often previous ones from before some change, instead of cleanly redesigning structures where it makes sense.

Note this only targets the duplication of user-facing items. Within a crate it is acceptable (and often unavoidable) to see the same item multiple times as export trees are constructed:

```rust
// OK
pub(crate) mod db {
    pub struct Connection;
}

pub use db::Connection;
```

Similarly, re-exports of foreign items are not covered by this rule, although they should follow M-FOREIGN-REEXPORTS.

Likewise, this rule also does not apply to public-but-hidden `_private` modules needed by macros, compare M-MACRO-HELPERS.
