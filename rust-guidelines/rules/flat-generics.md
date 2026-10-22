# flat-generics

Keep public service types free of nested type parameters (`Service<Backend<Store>>`): at most one visible level. Name complex bounds, especially `Fn` bounds, with a custom trait.

**Why:** Nested generics infect every user's types and errors.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-SIMPLE-ABSTRACTIONS, P:patterns/structural/trait-for-bounds

---

## Abstractions don't visibly nest (M-SIMPLE-ABSTRACTIONS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When designing your public types and primary API surface, avoid exposing nested or complex parametrized types to your users.

While powerful, type parameters introduce a cognitive load, even more so if the involved traits are crate-specific. Type parameters
become infectious to user code holding on to these types in their fields, often come with complex trait hierarchies on their own, and
might cause confusing error messages.

From the perspective of a user authoring `Foo`, where the other structs come from your crate:

```rust
struct Foo {
    service: Service // Great
    service: Service<Backend> // Acceptable
    service: Service<Backend<Store>> // Bad

    list: List<Rc<u32>> // Great, `List<T>` is simple container,
                        // other types user provided.

    matrix: Matrix4x4 // Great
    matrix: Matrix4x4<f32> // Still ok
    matrix: Matrix<f32, Const<4>, Const<4>, ArrayStorage<f32, 4, 4>> // ?!?
}
```

_Visible_ type parameters should be avoided in _service-like_ types (i.e., types mainly instantiated once per thread / application that are often passed
as dependencies), in particular if the nestee originates from the same crate as the service.

Containers, smart-pointers and similar data structures obviously must expose a type parameter, e.g., `List<T>` above. Even then, care should
be taken to limit the number and nesting of parameters.

To decide whether type parameter nesting should be avoided, consider these factors:

- Will the type be **named** by your users?
  - Service-level types are always expected to be named (e.g., `Library<T>`),
  - Utility types, such as the many [`std::iter`](https://doc.rust-lang.org/stable/std/iter/index.html) types like `Chain`, `Cloned`, `Cycle`, are not
    expected to be named.
- Does the type primarily compose with non-user types?
- Do the used type parameters have complex bounds?
- Do the used type parameters affect inference in other types or functions?

The more of these factors apply, the bigger the cognitive burden.

As a rule of thumb, primary service API types should not nest _on their own volition_, and if they do, only 1 level deep. In other words, these
APIs should not require users having to deal with an `Foo<Bar<FooBar>>`. However, if `Foo<T>` users want to bring their own `A<B<C>>` as `T` they
should be free to do so.

> ###  Type Magic for Better UX?
>
> The guideline above is written with 'bread-and-butter' types in mind you might create during  _normal_ development activity. Its intention is to
> reduce friction users encounter when working with your code.
>
> However, when designing API patterns and ecosystems at large, there might be valid reasons to introduce intricate type magic to overall _lower_
> the cognitive friction involved, [Bevy's ECS](https://docs.rs/bevy_ecs/latest/bevy_ecs/) or
> [Axum's request handlers](https://docs.rs/axum/latest/axum/handler/trait.Handler.html) come to mind.
>
> The threshold where this pays off is high though. If there is any doubt about the utility of your creative use of generics, your users might be
> better off without them.


## Use custom traits to avoid complex type bounds (P:patterns/structural/trait-for-bounds)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/structural/trait-for-bounds.html), MPL-2.0.

### Description

Trait bounds can become somewhat unwieldy, especially if one of the `Fn` traits[^fn-traits]
is involved and there are specific requirements on the output type. In such
cases the introduction of a new trait may help reduce verbosity, eliminate some
type parameters and thus increase expressiveness. Such a trait can be
accompanied with a generic `impl` for all types satisfying the original bound.

### Example

Let's imagine some sort of monitoring or information gathering system. The
system retrieves values of various types from diverse sources. It may derive
from them some sort of status indicating issues. For example, the total amount
of free memory should be above a certain theshold, and the user with the id `0`
should always be named "root".

For management reasons, we probably want type erasure on the top level. However,
we also need to provide specific (user configurable) assesments for specific
types of data sources (e.g. thresholds and ranges for numerical types). And
since sources for these values are diverse, we may choose to supply data sources
as closures that return a value when called. Because we are probably getting
those values from the operating system, we are likely confronted with operations
that may fail.

We thus may have settled on the following types and traits for handling specific
values:

```rust
use std::fmt::Display;

struct Value<G: FnMut() -> Result<T, Error>, S: Fn(&T) -> Status, T: Display> {
    value: Option<T>,
    getter: G,
    status: S,
}

impl<G: FnMut() -> Result<T, Error>, S: Fn(&T) -> Status, T: Display> Value<G, S, T> {
    pub fn update(&mut self) -> Result<(), Error> {
        (self.getter)().map(|v| self.value = Some(v))
    }

    pub fn value(&self) -> Option<&T> {
        self.value.as_ref()
    }

    pub fn status(&self) -> Option<Status> {
        self.value().map(&self.status)
    }
}

// ...

enum Status {
    // ...
}

struct Error {
    // ...
}
```

With these types, we will need to repeat the trait bounds for `G` in at least a
few places. Readability suffers, partially due the the fact that the getter
returns a `Result`. Introducing a bound for "getters" allows a more expressive
bound and eliminate one of the type parameters:

```rust
trait Getter {
    type Output: Display;

    fn get_value(&mut self) -> Result<Self::Output, Error>;
}

impl<F: FnMut() -> Result<T, Error>, T: Display> Getter for F {
    type Output = T;

    fn get_value(&mut self) -> Result<Self::Output, Error> {
        self()
    }
}

struct Value<G: Getter, S: Fn(&G::Output) -> Status> {
    value: Option<G::Output>,
    getter: G,
    status: S,
}

// ...
```

### Advantages

Introducing a new trait can help simplify type bounds, particularly via the
elimination of type parameters. A good name for the new trait will also make the
bound more expressive. The new trait, an abstraction, also offers opportunities
in itself, including:

- additional, specialized types implementing the new trait (e.g. representing an
  idendity of some sort) as well as other useful traits such as `Default` and
- additional methods, as long as they can be implemented for all relevant types.

### Disadvantages

Introducing new items such as the trait means we need to find an appropriate
name and place for it. It also means one more item users of the original
functionality need to investigate[^read-docs]. Depending on presentation, it may
not be obvious right away that a simple closure may be used as a `Getter` in the
example above.

[^fn-traits]: i.e. `Fn`, `FnOnce` and `FnMut`

[^read-docs]: meaning they may need to read more documentation
