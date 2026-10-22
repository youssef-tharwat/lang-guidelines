# on-stack-dispatch

On cold paths that pick one of several types, bind `&mut dyn Trait` to the chosen branch instead of boxing or duplicating code.

**Why:** Dynamic dispatch without allocation or code bloat.

**Sources:** P:idioms/on-stack-dyn-dispatch

---

## On-Stack Dynamic Dispatch (P:idioms/on-stack-dyn-dispatch)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/on-stack-dyn-dispatch.html), MPL-2.0.

### Description

We can dynamically dispatch over multiple values, however, to do so, we need to
declare multiple variables to bind differently-typed objects. To extend the
lifetime as necessary, we can use deferred conditional initialization, as seen
below:

### Example

```rust
use std::io;
use std::fs;

// We need to describe the type to get dynamic dispatch.
let readable: &mut dyn io::Read = if arg == "-" {
    &mut io::stdin()
} else {
    &mut fs::File::open(arg)?
};

// Read from `readable` here.

```

### Motivation

Rust monomorphises code by default. This means a copy of the code will be
generated for each type it is used with and optimized independently. While this
allows for very fast code on the hot path, it also bloats the code in places
where performance is not of the essence, thus costing compile time and cache
usage.

Luckily, Rust allows us to use dynamic dispatch, but we have to explicitly ask
for it.

### Advantages

We do not need to allocate anything on the heap. Neither do we need to
initialize something we won't use later, nor do we need to monomorphize the
whole code that follows to work with both `File` or `Stdin`.

### Disadvantages

Before Rust 1.79.0, the code needed two `let` bindings with deferred
initialization, which made up more moving parts than the `Box`-based version:

```rust
// We still need to ascribe the type for dynamic dispatch.
let readable: Box<dyn io::Read> = if arg == "-" {
    Box::new(io::stdin())
} else {
    Box::new(fs::File::open(arg)?)
};
// Read from `readable` here.
```

Luckily, this disadvantage is now gone. Yay!

### Discussion

Since Rust 1.79.0, the compiler will automatically extend the lifetimes of
temporary values within `&` or `&mut` as long as possible within the scope of
the function.

This means we can simply use a `&mut` value here without worrying about placing
the contents into some `let` binding (which would have been needed for deferred
initialization, which was the solution used before that change).

We still have a place for each value (even if that place is temporary), the
compiler knows the size of each value and each borrowed value outlives all
references borrowed from it.

### See also

- Finalisation in destructors and
  RAII guards can benefit from tight control
  over lifetimes.
- For conditionally filled `Option<&T>`s of (mutable) references, one can
  initialize an `Option<T>` directly and use its `.as_ref()` method to get an
  optional reference.
