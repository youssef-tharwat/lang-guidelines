# must-use

Add `#[must_use]` to pure functions and to functions whose result carries critical information (unless the return type already is `#[must_use]`), and to lazy-computation and error types.

**Why:** Ignoring the value is a bug.

**Sources:** G:must_use-on-functions, G:must_use-on-types

---

## `#[must_use]` on functions (G:must_use-on-functions)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#must_use-on-functions), CC BY 3.0.

Use `#[must_use]` on functions in these cases:

*   The caller cannot use the function correctly if they ignore the return value. This includes pure functions (functions without side effects), such as `HashMap::get()`.

*   Any function whose return value represents an error or otherwise critical information about the function’s behavior. If the return type is already annotated `#[must_use]` (which is true of `Result`, for example), the function does not need to be annotated `#[must_use]`.


## `#[must_use]` on types (G:must_use-on-types)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#must_use-on-types), CC BY 3.0.

Use `#[must_use]` on types intended to be returned by functions that would otherwise be annotated `#[must_use]` according to the rules above.

Examples:

*   The type is an error type (similar to `Result` or `StatusOr`).

*   The type represents a lazily evaluated computation. In other words, the function call doesn’t do anything by itself, and the return value needs to be accessed to cause some desired side effect.
