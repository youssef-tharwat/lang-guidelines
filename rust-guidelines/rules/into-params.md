# into-params

Accept `impl Into<T>` only where call-site ergonomics dominate; application code takes `T`.

**Why:** Generic parameters cost code size and inference clarity.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** G:accepting-into

---

## Accepting `Into` (G:accepting-into)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#accepting-into), CC BY 3.0.

When designing library APIs that accept a `T` but users are likely to have various types, consider accepting `impl Into<T>` instead of `T` if **call-site ergonomics are paramount**.

Tip: This should be balanced against code bloat concerns; it is not a requirement to use lots of `Into<T>` in your code.

Note: Application code should almost never use `impl Into<T>` parameters.

**Rationale**

Using `impl Into<T>` allows a function to directly accept various arguments of various compatible types. For example, a function accepting `impl Into<String>` could be called with a `String` or a `&str` literal directly.

The tradeoff here is balancing the convenience of avoiding a `.into()` at the callsite against the cost of generics (more complex API signature, increased code size, sometimes even type inference difficulties).
