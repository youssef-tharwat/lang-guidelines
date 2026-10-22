# honest-macros

A macro never misrepresents what is written: no struct-to-enum rewrites, altered signatures or changed `async`-ness, and no hidden generated types (a same-name item in another namespace, as Rocket does, is the one exception).

**Why:** Readers must be able to predict the expansion.

**Sources:** M-MACROS-DONT-LIE, M-PROC-IMPLIED-ITEMS

---

## Macros don't lie about signatures (M-MACROS-DONT-LIE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Macros must not (make users) misrepresent signatures or the shape of items.

Macros have the ability to arbitrarily rewrite token streams. They could convert structs to enums, traits to functions, or perform any other transformation imaginable. They should, however, do none of that, as the resulting code will be highly confusing and virtually impossible to predict or reason about.

Among others, macros must not

- visibly convert the nature of data types (e.g., structs to enums, ...),
- alter function signatures,
- convert the `async`-ness of items,
- do anything else that materially detaches _what's written_ from _what's happening_.

```rust
// Bad: Adds extra parameter and marks function `async`. Impossible to 
// predict from reading code. 
#[magic_transform]
fn foo() { }

foo(token).await
```


## Proc macros don't produce implied or hidden items (M-PROC-IMPLIED-ITEMS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Macros should not define magic types on their own, in particular not public ones, or ones that don't rely on namespace tricks.

Some macros want to define types, for example

```rust
#[my_macro]
struct UserType;

// would expand to

struct UserType;
struct ExtraType; 
impl UserType {
    fn foo() -> ExtraType { ... };
}
```

This is almost always a bad idea for several reasons:

- they can conflict with existing user-defined types inside the same module,
- if done naively, they can conflict with other expansions of the same macro,
- they can clash with the user's naming conventions,
- they are invisible at source code level and easily forgotten to be re-exported where needed.

While it is possible for users to work around these limitations somewhat, these are paper cuts your users will have to deal with, possibly months after the fact when refactoring otherwise unrelated code.

Note that there is one exception to this rule that has generally acceptable UX, the overloaded use of [namespaces](https://doc.rust-lang.org/reference/names/namespaces.html) made prominent by crates like Rocket:

```rust
#[my_macro]
fn foo() { ... }

// would expand to

fn foo() { ... }

struct foo;
impl SomeTrait for foo { ... }
```

Here a new type `foo` is introduced with the same name as the function `foo`. Due to Rust's namespace rules they can co-exist and are automatically re-exported with their parent, and due to [Rust's casing rules (C-CASE)](https://rust-lang.github.io/api-guidelines/naming.html#casing-conforms-to-rfc-430-c-case) these are highly unlikely to clash with user-defined types. However, they would still not make for a pretty _public_ type, and are therefore mainly used inside root crates to define request handlers or FFI functions.

> ###  Namespaces != Modules
>
> Namespaces in Rust have nothing to do with namespaces in other languages. A namespace in C# is approximately a module in Rust. A namespace in Rust
is an esoteric property of names (e.g., `fn foo`, `struct Bar {}`, `moo!`) that decides which 'naming bucket' it lives in inside a module.
