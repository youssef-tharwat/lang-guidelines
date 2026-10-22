# expect-not-unwrap

Prove `Some`/`Ok` with `if let`, `match` or `let ... else` instead of checking then unwrapping; when a panic is justified, write `.expect("why this cannot fail")`, not `.unwrap()`.

**Why:** The panic site documents its invariant.

**Sources:** G:prefer-expect-over-unwrap, G:prefer-pattern-matching-over-check-then-unwrap

---

## Prefer `expect` over `unwrap` (G:prefer-expect-over-unwrap)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-expect-over-unwrap), CC BY 3.0.

If a panic is necessary because an invariant cannot be expressed in the type system, prefer `expect` over `unwrap` to document the reason.


## Prefer pattern matching over check-then-unwrap (G:prefer-pattern-matching-over-check-then-unwrap)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-pattern-matching-over-check-then-unwrap), CC BY 3.0.

Avoid potentially panicking operations when the input data guarantees they cannot panic. For example, instead of using `Option::unwrap` on a value known to be valid, use pattern matching to prove correctness to the compiler.

✅ Good:

```rust
// Good: The match arm proves to the compiler that `x` is `Some`.
// A panic is obviously not possible.
if let Some(value) = option {
    use_value(value);
}
```

❌ Bad:

```rust
// Bad: Correctness of `unwrap` relies on a runtime check that `option` is `Some`.
if option.is_some() {
    use_value(option.unwrap());
}
```
