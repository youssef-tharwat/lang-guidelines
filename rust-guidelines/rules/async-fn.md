# async-fn

Write `async fn` rather than `fn -> impl Future` unless a trait or a hot path requires the explicit form.

**Why:** Reads as normal code, without a wrapping `async` block.

**Sources:** M-ASYNC-FN

---

## Functions are `async` over returning a Future (M-ASYNC-FN)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Functions should be declared `async fn foo()` over `fn foo() -> impl Future` when both are viable.

Functions marked `async` are more idiomatic and easier to read. An explicit `Future`-returning signature should only be used when required, for example inside traits or for _hot 'n heavy_ async functions, compare M-ASYNC-STACK-SIZE.

```rust
impl Foo {
    // Bad, signature is noisier and the body needs an extra `async` block
    fn foo() -> impl Future<Output = Result<T, E>> { async { Ok(t) } }

    // Good, method and implementation reads normally
    async fn foo() -> Result<T, E> { Ok(t) }
}
```
