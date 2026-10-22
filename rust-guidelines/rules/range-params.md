# range-params

Take ranges as `Range<T>` or `impl RangeBounds<T>`, never as two numbers or a tuple.

**Why:** Callers write `1..3`, `..` or `5..`.

**Sources:** M-IMPL-RANGEBOUNDS

---

## Accept `impl RangeBounds<>` where feasible (M-IMPL-RANGEBOUNDS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Functions that accept a range of numbers must use a `Range` type or trait over hand-rolled parameters:

```rust
// Bad
fn select_range(low: usize, high: usize) {}
fn select_range(range: (usize, usize)) {}
```

In addition, functions that can work on arbitrary ranges, should accept `impl RangeBounds<T>` rather than `Range<T>`.

```rust
// Callers must call with `select_range(1..3)`
fn select_range(r: Range<usize>) {}

// Callers may call as
//     select_any(1..3)
//     select_any(1..)
//     select_any(..)
fn select_any(r: impl RangeBounds<usize>) {}
```
