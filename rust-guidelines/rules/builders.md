# builders

Give a type with 4+ optional initialization combinations a builder: `Foo::builder(required)` returns `FooBuilder`, setters are chainable, infallible and named `x()` (not `set_x()`), `.build()` finishes and does all validation (returning `Result` if construction can fail), and `FooBuilder::new()` is not public.

**Why:** Construction can grow without breaking callers.

**Sources:** M-INIT-BUILDER, M-BUILD-RESULT, P:patterns/creational/builder

---

## Complex type construction has builders (M-INIT-BUILDER)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Types that could support 4 or more arbitrary initialization permutations should provide builders. In other words, types with up to
2 optional initialization parameters can be constructed via inherent methods:

```rust
struct Foo;

// Supports 2 optional construction parameters, inherent methods ok.
impl Foo {
    pub fn new() -> Self { Self }
    pub fn with_a(a: A) -> Self { Self }
    pub fn with_b(b: B) -> Self { Self }
    pub fn with_a_b(a: A, b: B) -> Self { Self }
}
```

Beyond that, types should provide a builder:

```rust
impl Foo {
    pub fn new() -> Self { ... }
    pub fn builder() -> FooBuilder { ... }
}

impl FooBuilder {
    pub fn a(mut self, a: A) -> Self { ... }
    pub fn b(mut self, b: B) -> Self { ... }
    pub fn c(mut self, c: C) -> Self { ... }
    pub fn build(self) -> Foo { ... }
}

```

The proper name for a builder that builds `Foo` is `FooBuilder`. Its methods must be chainable, with the final method called
`.build()`. The buildable struct must have a shortcut `Foo::builder()`, while the builder itself should _not_ have a public
`FooBuilder::new()`. Builder methods that set a value `x` are called `x()`, not `set_x()` or similar.

### Builders and Required Parameters

Required parameters should be passed when creating the builder, not as setter methods. For builders with multiple required
parameters, encapsulate them into a parameters struct and use the `deps: impl Into<Deps>` pattern to provide flexibility:

> **Note:** A dedicated deps struct is not required if the builder has no required parameters or only a single simple parameter. However,
> for backward compatibility and API evolution, it's preferable to use a dedicated struct for deps even in simple cases, as it makes it
> easier to add new required parameters in the future without breaking existing code.

```rust
#[derive(Debug, Clone)]
pub struct FooDeps {
    pub logger: Logger,
    pub config: Config,
}

impl From<(Logger, Config)> for FooDeps { ... }
impl From<Logger> for FooDeps { ... } // In case we could use default Config instance

impl Foo {
    pub fn builder(deps: impl Into<FooDeps>) -> FooBuilder { ... }
}
```

This pattern allows for convenient usage:

- `Foo::builder(logger)` - when only the logger is needed
- `Foo::builder((logger, config))` - when both parameters are needed
- `Foo::builder(FooDeps { logger, config })` - explicit struct construction

Alternatively, you can use [`fundle`](https://docs.rs/fundle) to simplify the creation of `FooDeps`:

```rust
#[derive(Debug, Clone)]
#[fundle::deps]
pub struct FooDeps {
    pub logger: Logger,
    pub config: Config,
}
```

This pattern enables "dependency injection", see [these docs](https://docs.rs/fundle/latest/fundle/attr.deps.html) for more details.

### Runtime-Specific Builders

For types that are runtime-specific or require runtime-specific configuration, provide dedicated builder creation methods that accept the appropriate runtime parameters:

```rust
#[cfg(feature="smol")]
#[derive(Debug, Clone)]
pub struct SmolDeps {
    pub clock: Clock,
    pub io_context: Context,
}

#[cfg(feature="tokio")]
#[derive(Debug, Clone)]
pub struct TokioDeps {
    pub clock: Clock,
}

impl Foo {
    #[cfg(feature="smol")]
    pub fn builder_smol(deps: impl Into<SmolDeps>) -> FooBuilder { ... }

    #[cfg(feature="tokio")]
    pub fn builder_tokio(deps: impl Into<TokioDeps>) -> FooBuilder { ... }
}
```

This approach ensures type safety at compile time and makes the runtime dependency explicit in the API surface. The resulting
builder methods follow the pattern `builder_{runtime}(deps)` where `{runtime}` indicates the specific runtime or execution environment.

### Further Reading

- [Builder pattern in Rust: self vs. &mut self, and method vs. associated function](https://users.rust-lang.org/t/builder-pattern-in-rust-self-vs-mut-self-and-method-vs-associated-function/72892)
- [fundle](https://docs.rs/fundle)


## Builders validate in final `.build()` (M-BUILD-RESULT)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

A builder's per-field setters should accept input without failing, final validation should be done by `.build()`.

Fallible setters add noise, and still don't guard against interdependent error conditions. Where builders are fallible they should offer a `Result`-carrying `.build()` instead.

```rust
// Bad, forces repeated error checks that provide no value.
Foo::builder()
    .name("Foo")?
    .distance(42)?
    .build();

// Good, consolidates sanity checking and allows for cross-checks 
// between properties.
Foo::builder()
    .name("Foo")
    .distance(42)
    .build()?;
```

That said, individual settings should prefer strong types carrying their own validation where applicable, compare M-STRONG-TYPES-GUARD.


## Builder (P:patterns/creational/builder)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/creational/builder.html), MPL-2.0.

### Description

Construct an object with calls to a builder helper.

### Example

```rust
#[derive(Debug, PartialEq)]
pub struct Foo {
    // Lots of complicated fields.
    bar: String,
}

impl Foo {
    // This method will help users to discover the builder
    pub fn builder() -> FooBuilder {
        FooBuilder::default()
    }
}

#[derive(Default)]
pub struct FooBuilder {
    // Probably lots of optional fields.
    bar: String,
}

impl FooBuilder {
    pub fn new(/* ... */) -> FooBuilder {
        // Set the minimally required fields of Foo.
        FooBuilder {
            bar: String::from("X"),
        }
    }

    pub fn name(mut self, bar: String) -> FooBuilder {
        // Set the name on the builder itself, and return the builder by value.
        self.bar = bar;
        self
    }

    // If we can get away with not consuming the Builder here, that is an
    // advantage. It means we can use the FooBuilder as a template for constructing
    // many Foos.
    pub fn build(self) -> Foo {
        // Create a Foo from the FooBuilder, applying all settings in FooBuilder
        // to Foo.
        Foo { bar: self.bar }
    }
}

#[test]
fn builder_test() {
    let foo = Foo {
        bar: String::from("Y"),
    };
    let foo_from_builder: Foo = FooBuilder::new().name(String::from("Y")).build();
    assert_eq!(foo, foo_from_builder);
}
```

### Motivation

Useful when you would otherwise require many constructors or where construction
has side effects.

### Advantages

Separates methods for building from other methods.

Prevents proliferation of constructors.

Can be used for one-liner initialisation as well as more complex construction.

When you add new fields to the target struct, you can update the builder to
leave client code backwards compatible.

### Disadvantages

More complex than creating a struct object directly, or a simple constructor
function.

### Discussion

This pattern is seen more frequently in Rust (and for simpler objects) than in
many other languages because Rust lacks overloading and default values for
function parameters. Since you can only have a single method with a given name,
having multiple constructors is less nice in Rust than in C++, Java, or others.

This pattern is often used where the builder object is useful in its own right,
rather than being just a builder. For example, see
[`std::process::Command`](https://doc.rust-lang.org/std/process/struct.Command.html)
is a builder for
[`Child`](https://doc.rust-lang.org/std/process/struct.Child.html) (a process).
In these cases, the `T` and `TBuilder` naming pattern is not used.

The example takes and returns the builder by value. It is often more ergonomic
(and more efficient) to take and return the builder as a mutable reference. The
borrow checker makes this work naturally. This approach has the advantage that
one can write code like

```rust
let mut fb = FooBuilder::new();
fb.a();
fb.b();
let f = fb.build();
```

as well as the `FooBuilder::new().a().b().build()` style.

### See also

- [Description in the style guide](https://web.archive.org/web/20210104103100/https://doc.rust-lang.org/1.12.0/style/ownership/builders.html)
- [derive_builder](https://crates.io/crates/derive_builder), a crate for
  automatically implementing this pattern while avoiding the boilerplate.
- Constructor pattern for when construction is simpler.
- [Builder pattern (wikipedia)](https://en.wikipedia.org/wiki/Builder_pattern)
- [Construction of complex values](https://web.archive.org/web/20210104103000/https://rust-lang.github.io/api-guidelines/type-safety.html#c-builder)
