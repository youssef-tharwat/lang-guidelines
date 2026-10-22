# std-traits

Implement the standard trait (`FromStr`, `From`, `Default`, `Display`, `Iterator`, ...) instead of a look-alike inherent method, and `#[derive]` whenever a derive fits.

**Why:** Generic code, `?` and `collect` work with std traits.

**Sources:** G:implement-known-standard-library-traits-instead-of-custom-methods, G:use-derive-if-possible

---

## Implement known standard library traits instead of custom methods (G:implement-known-standard-library-traits-instead-of-custom-methods)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#implement-known-standard-library-traits-instead-of-custom-methods), CC BY 3.0.

If a method matches the purpose and behavior of a standard library trait, implement that trait. For example, instead of writing `fn from_str(&str) -> Self` on `Foo`, you should `impl FromStr for Foo`.

It is acceptable to have both the method and the trait impl for discoverability reasons.

For context, see Clippy lint [`should_implement_trait`](https://rust-lang.github.io/rust-clippy/master/index.html#should_implement_trait) ([list of traits](https://github.com/rust-lang/rust-clippy/blob/928349795f9f28f54e69bd0f0ffeed33de5e272a/clippy_lints/src/methods/mod.rs#L3940-L3971)).


## Use `#[derive()]` if possible (G:use-derive-if-possible)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#use-derive-if-possible), CC BY 3.0.

Manual implementations should be avoided if they can be expressed as a `#[derive()]`.
