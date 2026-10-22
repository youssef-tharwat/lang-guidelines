# iterator-boundaries

Functions that only iterate accept `impl IntoIterator`; return `impl Iterator` rather than a freshly built `Vec` unless callers need an owned, indexable collection. Application code may use slices and `Vec`.

**Why:** Callers choose how to consume and skip allocations.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** G:iterators-vs-owned-collections-in-return-types, G:iterators-vs-slices-in-function-parameters

---

## Iterators vs. owned collections in return types (G:iterators-vs-owned-collections-in-return-types)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#iterators-vs-owned-collections-in-return-types), CC BY 3.0.

Prefer returning iterators (either concrete types or `impl Iterator`) where possible over returning `Vec<T>`.

Note: In application code, returning a `Vec<T>` is fine if it simplifies the code and if flexibility and performance advantages of iterators are not clearly needed.

Exceptions:

*   Most callers will need to construct an owned vector.

*   The function’s implementation naturally constructs a vector.

*   The returned value will likely need to be randomly indexed.

*   The algorithm works better as a `for` loop and the forced allocation doesn’t matter too much.

*   The function’s intended purpose is creating a new owned collection.

*   The function is returning a pre-existing vector.

**Rationale**

Highly reusable library code generally should strive to provide more flexible and performant APIs. Returning an iterator allows callers to choose how to consume the data: collect it into a vector, process it in a loop, or chain further iterator adapters. Some of these options allow users to avoid unnecessary allocations.

In application code, the usage patterns for a function are often easier to predict. If it is clear that performance is not a concern, or that data would be collected into a vector anyway, returning a vector makes for a simpler API.


## Iterators vs. slices in function parameters (G:iterators-vs-slices-in-function-parameters)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#iterators-vs-slices-in-function-parameters), CC BY 3.0.

Highly reusable library code should accept iterators or `impl IntoIterator` if it only needs to iterate over the input.

Note: In application code, accepting a slice `&[T]` is fine if it simplifies the code and if flexibility and performance advantages of iterators are not clearly needed.

**Rationale**

Highly reusable library code generally should strive to provide more flexible and performant APIs. Functions that accept iterators offer callers:

*   More flexibility (data can be supplied from any collection)

*   Efficiency (data does not need to be copied into a contiguous piece of memory)

*   Composability (the function works better with iterator chains)

In application code, the usage patterns for a function are often easier to predict. If it is clear that performance is not a concern, or that callers would always have a vector anyway, accepting a slice makes for a simpler API.
