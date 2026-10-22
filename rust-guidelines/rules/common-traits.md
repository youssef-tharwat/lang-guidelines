# common-traits

Implement the common traits that fit (libraries eagerly, applications as needed): `Debug` on every public type, hand-written and redacting for secrets with a test; `Display` for user-readable types and errors; `Clone` unless it is a resource handle; `Copy` while it will stay plain data; `PartialEq`/`Eq`/`Hash` for keys; `Ord` only for a true total order.

**Why:** Types then work in collections, logs and tests.

**Sources:** G:specific-guidance-for-important-traits, G:add-trait-implementations-when-they-become-necessary, M-PUBLIC-DEBUG, M-PUBLIC-DISPLAY, M-UPSTREAM-GUIDELINES

---

## Specific guidance for important traits (G:specific-guidance-for-important-traits)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#specific-guidance-for-important-traits), CC BY 3.0.

*   **Types with public fields**: Consider implementing traits implemented by all subfields.

*   **Error types**: Implement the `Copy` trait whenever possible. `Copy` types are simpler to manage and propagate because they can be passed by value without moving ownership. An example of a case where this is not possible is if the error must contain non-`Copy` fields like a `String`.

*   **`Copy`**: Implement whenever it is reasonably clear that the type will continue to be `Copy` in the future.

*   **`Clone`**: Most types should implement `Clone` unless they represent some external resource.

*   **`Default`**: Implement if the type implements `new()` or otherwise has a default state. For context, see Clippy lint [`new_without_default`](https://rust-lang.github.io/rust-clippy/master/index.html#new_without_default).

*   **`PartialEq`** / **`Eq`**: If you want users to use the `==` operator, prefer implementing `PartialEq` over `Eq`. When you do implement `Eq`, be aware of the additionally required reflexivity (details: https://doc.rust-lang.org/std/cmp/trait.Eq.html).

*   **`PartialOrd`** / **`Ord`**: If you want users to use the `<` or `>` operators, prefer implementing `PartialOrd` over `Ord`. When you do implement `Ord`, be aware that it requires total ordering (details: https://doc.rust-lang.org/std/cmp/trait.Ord.html).

*   **Map keys**

    *   If you think it is likely that a type will be used as a map key or otherwise cached, implement `Hash` and `Eq`.

    *   If, in addition, the type has a clear total ordering, implement `Ord` (and any traits it needs).


## Add trait implementations when they become necessary (G:add-trait-implementations-when-they-become-necessary)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#add-trait-implementations-when-they-become-necessary), CC BY 3.0.

As a general rule, low-level library code should anticipate users’ needs proactively, while application code should add trait impls as needed.


## Public types are Debug (M-PUBLIC-DEBUG)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

All public types exposed by a crate should implement `Debug`. Most types can do so via `#[derive(Debug)]`:

```rust
#[derive(Debug)]
struct Endpoint(String);
```

Types designed to hold sensitive data should also implement `Debug`, but do so via a custom implementation.
This implementation must employ unit tests to ensure sensitive data isn't actually leaked, and will not be in the future.

```rust
use std::fmt::{Debug, Formatter};

struct UserSecret(String);

impl Debug for UserSecret {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "UserSecret(...)")
    }
}

#[test]
fn test() {
    let key = "552d3454-d0d5-445d-ab9f-ef2ae3a8896a";
    let secret = UserSecret(key.to_string());
    let rendered = format!("{:?}", secret);

    assert!(rendered.contains("UserSecret"));
    assert!(!rendered.contains(key));
}
```


## Public types meant to be read are Display (M-PUBLIC-DISPLAY)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

If your type is expected to be read by upstream consumers, be it developers or end users, it should implement `Display`. This in particular includes:

- Error types, which are mandated by `std::error::Error` to implement `Display`
- Wrappers around string-like data

Implementations of `Display` should follow Rust customs; this includes rendering newlines and escape sequences.
The handling of sensitive data outlined in M-PUBLIC-DEBUG applies analogously.


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
