# lifetime-and-generic-names

Give lifetimes descriptive names (single letters only for a simple input-to-output link, `'_` where it works); name type parameters after their main bound, using `T`/`U` only when unbounded.

**Why:** The name says what is borrowed or abstracted.

**Sources:** G:naming-lifetimes, G:naming-generic-parameters

---

## Naming lifetimes (G:naming-lifetimes)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#naming-lifetimes), CC BY 3.0.

Lifetimes should have descriptive names, especially type lifetimes.

Exceptions:

*   Type lifetimes that are extremely generic abstractions like `Cow`.

*   It is fine to use anonymous lifetimes (`'_`) where they work.

*   Single-character lifetimes are okay when they are simply expressing the relationship between a method’s input and output, or needed for a local higher-ranked lifetime bounds (`for<'a>`). Up to two such local lifetimes are fine, if more are needed, we strongly advise you to use descriptive names.


## Naming generic parameters (G:naming-generic-parameters)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#naming-generic-parameters), CC BY 3.0.

Use a short name for your generic parameters (either single or multi character), related to the kind of thing they represent. Single-letter generics are okay, but the letter chosen should be somewhat indicative of the object type, ideally taken from the most important trait bound.

`T` or `U` are fine when the generics are in a relatively unbound context; i.e. it is an API intended for use with most types, like `Vec<T>`.
