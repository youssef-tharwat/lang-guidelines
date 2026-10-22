# method-names

Follow std naming: `as_`/`to_`/`into_` by cost and ownership; getters `foo()`/`foo_mut()` without `get_`; `set_foo`, `take_foo`, `replace_foo`; `with_foo(|f| ...)` for scoped access to interior state.

**Why:** Readers predict cost and ownership from the name.

**Sources:** G:naming-methods, G:getters-and-setters, M-UPSTREAM-GUIDELINES

---

## Naming methods (G:naming-methods)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#naming-methods), CC BY 3.0.

Follow the Rust standard library style for naming methods. See also the guidance on [naming conventions](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions.html) in the Comprehensive Rust course.

Specific considerations:

*   Use prefixes such as `as_...()`, `to_...()`, or `into_...()` with the appropriate `self` convention. See also [this section](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv) of the Rust API Guidelines and the Clippy lint [`wrong_self_convention`](https://rust-lang.github.io/rust-clippy/master/index.html#wrong_self_convention).


## Getters and setters (G:getters-and-setters)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#getters-and-setters), CC BY 3.0.

Writing and naming getters and setters should follow these guidelines:

*   `foo()` for a getter that returns a `T` by value.

*   `foo_mut()` for a getter that returns a `&mut T`.

*   `take_foo()` for a getter that “clears” the value (by setting it to `None` or some other default state) and returns the old value.

*   `set_foo()` for a setter that takes a `T` by value.

*   `with_foo()` / `with_mut_foo()` for an accessor that operates via a closure (see details below). Such an accessor is invoked as `object.with_foo(|foo| frob(foo))`.

*   `replace_foo()` for a setter that returns the old value.

Examples

```rust
impl Stuff {
   fn foo(&self) -> &Foo { ...  }
   fn foo_mut(&mut self) -> &mut Foo { ... }

   /// Sets "baz" property to `None` and returns the old value.
   fn take_baz(&mut self) -> Option<Baz> { ... }

   fn set_foo(&mut self, foo: Foo) { ... }

   /// Calls `f` with a borrow of the "bar" property.
   /// Returns the return value of `f`.
   fn with_bar<R>(&self, f: impl FnOnce(&Bar) -> R) -> R { ... }

   /// Calls `f` with a mutable borrow of the "bar" property.
   /// Returns the return value of `f`.
   fn with_mut_bar<R>(&self, f: impl FnOnce(&mut i32) -> R) -> R { ... }

   /// Sets "foo" property to `foo` and returns the old value.
   fn replace_foo(&mut self, foo: Foo) -> Foo  { ... }
}
```

### More on accessors that accept closures

Accessors that accept a closure (`.with_foo()`) are typically invoked as `object.with_foo(|foo| do_something_with(foo))`. They can be a good choice in the following situations:

*   When the property is contained in an interior mutability wrapper (e.g. `Mutex` or `RefCell`). These mechanisms need to constrain access to the property to a scope, and the closure provides this scope. This is usually preferable to directly returning the RAII object that implements the scope (e.g. `MutexGuard<T>`) because the latter would leak an implementation detail.

*   When follow-up work or validation is needed after a property is changed and a `set_foo()` accessor cannot be used (for example because the property’s type is expensive to clone or cannot be cloned at all).

A `with_foo()` accessor will often allow the closure to return a value and forward it by returning it from `with_foo()`.

If you need to provide two closure-accepting accessors, one for read-only access and one for mutable access, it is common to name them `with_foo()` and `with_mut_foo()`. Otherwise, `with_foo()` is often also used for mutating accessors.


## Follow the upstream guidelines (M-UPSTREAM-GUIDELINES)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

The guidelines in this book complement existing Rust guidelines, in particular:

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html)
- [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns//intro.html)
- [Rust Reference - Undefined Behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

We recommend you read through these as well, and apply them in addition to this book's items. Pay special attention to the ones below, as they are frequently forgotten:

- [ ] [C-CONV](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv) - Ad-hoc conversions
  follow  `as_`, `to_`, `into_` conventions
- [ ] [C-GETTER](https://rust-lang.github.io/api-guidelines/naming.html#getter-names-follow-rust-convention-c-getter) - Getter names follow Rust convention
- [ ] [C-COMMON-TRAITS](https://rust-lang.github.io/api-guidelines/interoperability.html#c-common-traits) - Types eagerly implement common traits
  - `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Default`, `Debug`
  - `Display` where type wants to be displayed
- [ ] [C-CTOR](https://rust-lang.github.io/api-guidelines/predictability.html?highlight=new#constructors-are-static-inherent-methods-c-ctor) -
  Constructors are static, inherent methods
  - In particular, have `Foo::new()`, even if you have `Foo::default()`
- [ ] [C-FEATURE](https://rust-lang.github.io/api-guidelines/naming.html#feature-names-are-free-of-placeholder-words-c-feature) - Feature names
  are free of placeholder words
