# format-strings

Build strings from three or more pieces, or substitute into a literal, with `format!`/`write!`, not `+` chains or `str::replace`.

**Why:** Fewer allocations and standard syntax.

**Sources:** G:prefer-format--write-for-concatenation-and-substitution, P:idioms/concat-format

---

## Prefer `format!` / `write!` for concatenation and substitution (G:prefer-format--write-for-concatenation-and-substitution)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-format--write-for-concatenation-and-substitution), CC BY 3.0.

Prefer `format!()` and `write!()` to other alternatives in the following situations:

*   To concatenate more than two strings. For example, use `format!("{a}{b}{c}")` instead of `a + b + c`.

*   To perform substitutions on a literal string (instead of using `str::replace`).

**Rationale**

*   `format!` / `write!` require fewer allocations than concatenating strings using `+`.

*   Prefer standard format strings to inventing your own templating syntax.


## Concatenating strings with `format!` (P:idioms/concat-format)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/concat-format.html), MPL-2.0.

### Description

It is possible to build up strings using the `push` and `push_str` methods on a
mutable `String`, or using its `+` operator. However, it is often more
convenient to use `format!`, especially where there is a mix of literal and
non-literal strings.

### Example

```rust
fn say_hello(name: &str) -> String {
    // We could construct the result string manually.
    // let mut result = "Hello ".to_owned();
    // result.push_str(name);
    // result.push('!');
    // result

    // But using format! is better.
    format!("Hello {name}!")
}
```

### Advantages

Using `format!` is usually the most succinct and readable way to combine
strings.

### Disadvantages

It is usually not the most efficient way to combine strings - a series of `push`
operations on a mutable string is usually the most efficient (especially if the
string has been pre-allocated to the expected size).
