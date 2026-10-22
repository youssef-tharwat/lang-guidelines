# explicit-types

Annotate `let` bindings whose type isn't obvious (results of `.into()`, `.parse()`, `.collect()` and long chains) instead of using a turbofish.

**Why:** Readers shouldn't need an IDE to know the type.

**Sources:** G:dont-overuse-type-inference

---

## Don’t overuse type inference (G:dont-overuse-type-inference)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#dont-overuse-type-inference), CC BY 3.0.

Add enough explicit types so that someone familiar with the codebase can figure out what the inferred types are.

Prefer to add the types to variable declarations, rather than as [turbofishes](https://doc.rust-lang.org/reference/glossary.html#turbofish). If the compiler forces you to add a turbofish, it is generally fine to add a `_` inference marker.

Specific situations in which you should probably add types:

*   When calling methods with a generic return type, such as `.into()` or `.parse()`.

*   For the result of complex iterator chains.
