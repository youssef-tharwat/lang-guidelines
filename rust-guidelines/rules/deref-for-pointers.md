# deref-for-pointers

Implement `Deref` only for smart pointers and owning-to-borrowed views (`Vec<T>` to `[T]`), never to emulate inheritance.

**Why:** Deref polymorphism surprises method resolution and readers.

**Sources:** P:idioms/deref, P:anti/patterns/deref

---

## Collections are smart pointers (P:idioms/deref)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/deref.html), MPL-2.0.

### Description

Use the [`Deref`](https://doc.rust-lang.org/std/ops/trait.Deref.html) trait to
treat collections like smart pointers, offering owning and borrowed views of
data.

### Example

```rust
use std::ops::Deref;

struct Vec<T> {
    data: RawVec<T>,
    //..
}

impl<T> Deref for Vec<T> {
    type Target = [T];

    fn deref(&self) -> &[T] {
        //..
    }
}
```

A `Vec<T>` is an owning collection of `T`s, while a slice (`&[T]`) is a borrowed
collection of `T`s. Implementing `Deref` for `Vec` allows implicit dereferencing
from `&Vec<T>` to `&[T]` and includes the relationship in auto-dereferencing
searches. Most methods you might expect to be implemented for `Vec`s are instead
implemented for slices.

Also `String` and `&str` have a similar relation.

### Motivation

Ownership and borrowing are key aspects of the Rust language. Data structures
must account for these semantics properly to give a good user experience. When
implementing a data structure that owns its data, offering a borrowed view of
that data allows for more flexible APIs.

### Advantages

Most methods can be implemented only for the borrowed view, they are then
implicitly available for the owning view.

Gives clients a choice between borrowing or taking ownership of data.

### Disadvantages

Methods and traits only available via dereferencing are not taken into account
when bounds checking, so generic programming with data structures using this
pattern can get complex (see the `Borrow` and `AsRef` traits, etc.).

### Discussion

Smart pointers and collections are analogous: a smart pointer points to a single
object, whereas a collection points to many objects. From the point of view of
the type system, there is little difference between the two. A collection owns
its data if the only way to access each datum is via the collection and the
collection is responsible for deleting the data (even in cases of shared
ownership, some kind of borrowed view may be appropriate). If a collection owns
its data, it is usually useful to provide a view of the data as borrowed so that
it can be referenced multiple times.

Most smart pointers (e.g., `Foo<T>`) implement `Deref<Target=T>`. However,
collections will usually dereference to a custom type. `[T]` and `str` have some
language support, but in the general case, this is not necessary. `Foo<T>` can
implement `Deref<Target=Bar<T>>` where `Bar` is a dynamically sized type and
`&Bar<T>` is a borrowed view of the data in `Foo<T>`.

Commonly, ordered collections will implement `Index` for `Range`s to provide
slicing syntax. The target will be the borrowed view.

### See also

- Deref polymorphism anti-pattern.
- [Documentation for `Deref` trait](https://doc.rust-lang.org/std/ops/trait.Deref.html).


## `Deref` polymorphism (P:anti/patterns/deref)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/anti/patterns/deref.html), MPL-2.0.

### Description

Misuse the `Deref` trait to emulate inheritance between structs, and thus reuse
methods.

### Example

Sometimes we want to emulate the following common pattern from OO languages such
as Java:

```java
class Foo {
    void m() { ... }
}

class Bar extends Foo {}

public static void main(String[] args) {
    Bar b = new Bar();
    b.m();
}
```

We can use the deref polymorphism anti-pattern to do so:

```rust
use std::ops::Deref;

struct Foo {}

impl Foo {
    fn m(&self) {
        //..
    }
}

struct Bar {
    f: Foo,
}

impl Deref for Bar {
    type Target = Foo;
    fn deref(&self) -> &Foo {
        &self.f
    }
}

fn main() {
    let b = Bar { f: Foo {} };
    b.m();
}
```

There is no struct inheritance in Rust. Instead we use composition and include
an instance of `Foo` in `Bar` (since the field is a value, it is stored inline,
so if there were fields, they would have the same layout in memory as the Java
version (probably, you should use `#[repr(C)]` if you want to be sure)).

In order to make the method call work we implement `Deref` for `Bar` with `Foo`
as the target (returning the embedded `Foo` field). That means that when we
dereference a `Bar` (for example, using `*`) then we will get a `Foo`. That is
pretty weird. Dereferencing usually gives a `T` from a reference to `T`, here we
have two unrelated types. However, since the dot operator does implicit
dereferencing, it means that the method call will search for methods on `Foo` as
well as `Bar`.

### Advantages

You save a little boilerplate, e.g.,

```rust
impl Bar {
    fn m(&self) {
        self.f.m()
    }
}
```

### Disadvantages

Most importantly this is a surprising idiom - future programmers reading this in
code will not expect this to happen. That's because we are misusing the `Deref`
trait rather than using it as intended (and documented, etc.). It's also because
the mechanism here is completely implicit.

This pattern does not introduce subtyping between `Foo` and `Bar` like
inheritance in Java or C++ does. Furthermore, traits implemented by `Foo` are
not automatically implemented for `Bar`, so this pattern interacts badly with
bounds checking and thus generic programming.

Using this pattern gives subtly different semantics from most OO languages with
regards to `self`. Usually it remains a reference to the sub-class, with this
pattern it will be the 'class' where the method is defined.

Finally, this pattern only supports single inheritance, and has no notion of
interfaces, class-based privacy, or other inheritance-related features. So, it
gives an experience that will be subtly surprising to programmers used to Java
inheritance, etc.

### Discussion

There is no one good alternative. Depending on the exact circumstances it might
be better to re-implement using traits or to write out the facade methods to
dispatch to `Foo` manually. We do intend to add a mechanism for inheritance
similar to this to Rust, but it is likely to be some time before it reaches
stable Rust. See these [blog](http://aturon.github.io/blog/2015/09/18/reuse/)
[posts](http://smallcultfollowing.com/babysteps/blog/2015/10/08/virtual-structs-part-4-extended-enums-and-thin-traits/)
and this [RFC issue](https://github.com/rust-lang/rfcs/issues/349) for more
details.

The `Deref` trait is designed for the implementation of custom pointer types.
The intention is that it will take a pointer-to-`T` to a `T`, not convert
between different types. It is a shame that this isn't (probably cannot be)
enforced by the trait definition.

Rust tries to strike a careful balance between explicit and implicit mechanisms,
favouring explicit conversions between types. Automatic dereferencing in the dot
operator is a case where the ergonomics strongly favour an implicit mechanism,
but the intention is that this is limited to degrees of indirection, not
conversion between arbitrary types.

### See also

- Collections are smart pointers idiom.
- Delegation crates for less boilerplate like
  [delegate](https://crates.io/crates/delegate) or
  [ambassador](https://crates.io/crates/ambassador)
- [Documentation for `Deref` trait](https://doc.rust-lang.org/std/ops/trait.Deref.html).
