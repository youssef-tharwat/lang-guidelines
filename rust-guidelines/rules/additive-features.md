# additive-features

Make features additive: any combination compiles, a `std` feature instead of `no-std`, no feature removes or changes a public item or needs another enabled by hand, and feature names have no placeholder words.

**Why:** Cargo unifies features across the whole dependency graph.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-FEATURES-ADDITIVE

---

## Features are additive (M-FEATURES-ADDITIVE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

All library features must be additive, and any combination must work, as long as the feature itself would work on the current platform. This implies:

- [ ] You must not introduce a `no-std` feature, use a `std` feature instead
- [ ] Adding any feature `foo` must not disable or modify any public item
  - Adding enum variants is fine if these enums are `#[non_exhaustive]`
- [ ] Features must not rely on other features to be manually enabled
- [ ] Features must not rely on their parent to skip-enable a feature in one of their children

Further Reading

- [Feature Unification](https://doc.rust-lang.org/cargo/reference/features.html#feature-unification)
- [Mutually Exclusive Features](https://doc.rust-lang.org/cargo/reference/features.html#mutually-exclusive-features)
