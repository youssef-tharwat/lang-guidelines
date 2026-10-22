# collection-sizing

Create collections with `with_capacity` when the size is known, or build them with `collect`; `shrink_to_fit` a large, long-lived collection that grew without a reservation.

**Why:** Avoids repeated reallocation and up to 2x wasted memory.

**Sources:** M-INITIAL-CAPACITY, M-SHRINK-TO-FIT

---

## Collections are created with sufficient initial capacity (M-INITIAL-CAPACITY)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Where the final or approximate size of a collection (`Vec`, `String`, `HashMap`, `HashSet`, etc.) is known at construction time, it should be created via   `with_capacity` rather than `new` or `default`.

Collections created without capacity may be re-allocated multiple times during their initialization, which also includes copying their content. Creating them with sufficient capacity can entirely avoid this needless overhead.

```rust
// Bad, probably re-allocates and copies content over multiple times.
let mut rval = Vec::new();
for x in &other {
    rval.push(convert(x));
}

// Better, creates collection with sufficient capacity upfront.
let mut rval = Vec::with_capacity(other.len());
for x in &other {
    rval.push(convert(x));
}
```

Iterator-driven construction (`collect`) inherits this behavior via `size_hint` and should be preferred over manual `push` loops when possible:

```rust
// Ideal, looks nicer and is performant
let rval: Vec<_> = other.iter().map(convert).collect();
```


## Shrink collections to fit after building (M-SHRINK-TO-FIT)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Where large, long-lived, growable collections such as `Vec` or `String` were built without an exact size reservation (compare M-INITIAL-CAPACITY), the resulting collection should be shrunk via `shrink_to_fit` before storing it.

Many Rust collections grow by powers of two when iteratively adding elements. In the worst case a collection might therefore use ~2x of its needed memory.

```rust
// Bad, long lived object might end up using 2x needed memory.
let mut long_lived = Vec::new();
for x in large_iter {
    long_lived.push(x);
}

// Good, frees up extra memory.
long_lived.shrink_to_fit();
```

Note that this does not apply to conversions done via `into_boxed_*` and friends (compare M-BOX-DST), as these generally shrink before converting already.
