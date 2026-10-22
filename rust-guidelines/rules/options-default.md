# options-default

Give options structs (all-public fields, passed to one function) a `Default` impl so callers write `..Default::default()`.

**Why:** Callers set only what they care about.

**Sources:** G:options-structs-should-implement-default

---

## Options structs should implement Default (G:options-structs-should-implement-default)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#options-structs-should-implement-default), CC BY 3.0.

Structs with all-public fields that are primarily used as a “bag of options” for a function should implement `Default`.

**Rationale**

This enables convenient use of struct update syntax (`Struct { a: 0, ..Default::default()}` ).
