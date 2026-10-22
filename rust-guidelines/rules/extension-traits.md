# extension-traits

Name an extension trait `<Type>Ext` and keep it in the crate that owns the type, unless it is foundational.

**Why:** Avoids method-name clashes between extensions.

**Sources:** G:extension-traits, G:naming-extension-traits

---

## Extension traits (G:extension-traits)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#extension-traits), CC BY 3.0.

An [extension trait](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html) is a trait that adds methods to a type from a different crate.

What differentiates an extension trait from other traits is that its sole purpose is to add methods to the type; it is not intended for use in generics (`T: Trait`, `impl Trait`) or dynamic dispatch (`dyn Trait`). To indicate this, the name of an extension trait should carry the suffix `~Ext` (for example, `ForeignTypeExt`).

In general, the team that owns the original type should also own the extension trait.

Exceptions:

*   Extension methods that are expected to become well known and provide significant value, for example, in foundational libraries / frameworks.

Note: This rule is specifically about extension traits. It is relatively common to define a trait as an input trait (e.g., `DateLike`) and implement it on a bunch of foreign types.

Examples

```rust
extern crate foreign_crate;
use foreign_crate::ForeignType;

trait ForeignTypeExt {
  fn additional_method(&self);
}

impl ForeignTypeExt for ForeignType {
  fn additional_method(&self) { ... }
}
```

It is also possible to define an extension trait for every type that implements some foreign trait. Effectively, this is equivalent to adding default methods to the foreign trait:

```rust
extern crate foreign_crate;
use foreign_crate::ForeignTrait;

trait ForeignTraitExt {
  fn additional_method(&self);
}

impl<T: ForeignTrait> ForeignTraitExt for T {
  fn additional_method(&self) { ... }
}
```

**Rationale**

When the same team owns the extension trait and the type being extended, this helps avoid method name conflicts between the base type and the extension trait or between two extension traits.


## Naming extension traits (G:naming-extension-traits)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#naming-extension-traits), CC BY 3.0.

When naming an extension trait, give the name an `~Ext` suffix (for example, `ForeignTypeExt`).
