# import-style

One module per `use` statement (`use foo::bar::{A, B};`, rustfmt `imports_granularity = "Module"`); import types and use them unqualified; call free functions through their module (`mem::take`, not a bare `take`); import a trait inside the function that needs it unless the whole file uses it.

**Why:** Names read the same everywhere and refactor cleanly.

**Sources:** G:a-use-statement-should-import-items-from-one-module, G:type-names-should-be-imported-and-used-unqualified, G:qualify-calls-to-top-level-functions-with-a-module-name, G:prefer-locally-scoped-trait-imports

---

## A `use` statement should import items from one module (G:a-use-statement-should-import-items-from-one-module)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#a-use-statement-should-import-items-from-one-module), CC BY 3.0.

This rule corresponds to the rustfmt setting `imports_granularity = Module`.

Basically, there should not be any `::`’s inside the `{..}` block of a `use` statement. For example:

✅ Good:

```rust
use foo::Foo;
use foo::bar::Bar;
use foo::bar::Baz;
```

✅ Good:

```rust
use foo::Foo;
use foo::bar::{Bar, Baz};
```

❌ Bad:

```rust
use foo::{Foo, bar::Bar};
```


## Type names should be imported and used unqualified (G:type-names-should-be-imported-and-used-unqualified)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#type-names-should-be-imported-and-used-unqualified), CC BY 3.0.

By default, types and traits should be referenced in code without using their module path, e.g., code should use `Regex`, not `regex::Regex`, with a `use regex::Regex` at the top of the file or potentially in the relevant function.

Exceptions:

*   In cases where there are ambiguities, it is acceptable to directly reference types with common names like `io::Error`. It is also acceptable to rename (`use std::io::Error as IoError`).

*   In cases where you have a large “group” of types, e.g. the [`hir module in rustc`](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir/hir/index.html) which contains a large number of HIR types.

*   In macros and generated code; where requiring a `use` is counterproductive.

*   In code with lots of dependencies, where importing everything would lead to a very large import block with little benefit.

**Rationale**

This rule largely exists to avoid reviewer disagreements.


## Qualify calls to top-level functions with a module name (G:qualify-calls-to-top-level-functions-with-a-module-name)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#qualify-calls-to-top-level-functions-with-a-module-name), CC BY 3.0.

To use top-level functions defined in other modules or crates, import their module and call them with `modulename::functionname()`. For example:

✅ Good:

```rust
use std::mem;

let x = mem::transmute(y);
```

❌ Bad:

```rust
use std::mem::transmute;

let x = transmute(y);
```

Exceptions:

*   When importing functions with sufficiently disambiguated names, e.g., functions from C++ (where it is typical to call top-level (free) functions directly).

*   When the module name itself is prone to collisions. For example, when the module name is a C++ namespace name, and multiple crates define the same submodules.

**Rationale**

Many Rust codebases consistently keep a style such that unqualified lowercase names are assumed local, so `foo()` can be assumed to be from the same module. This rule largely exists to avoid reviewer disagreements, the benefit is mostly consistency and a minor edge on reading code without xrefs.


## Prefer locally-scoped trait imports (G:prefer-locally-scoped-trait-imports)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-locally-scoped-trait-imports), CC BY 3.0.

Import traits within function bodies, unless the trait’s methods are used extensively throughout the file.

✅ Good:

```rust
fn foo(x: u8) {
    // Import the trait within a function, not at the module scope.
    use std::str::FromStr;

    let string: String = x.parse();
}
```
