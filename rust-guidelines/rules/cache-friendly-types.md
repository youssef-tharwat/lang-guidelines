# cache-friendly-types

In hot types, avoid nested `Arc` indirection and lift hot fields next to where they are read; store frequently created, immutable internal sequences as `Box<[T]>`, `Box<str>` or `Arc<str>` instead of `Vec`/`String`.

**Why:** Each indirection is a sequential memory round trip.

**Sources:** M-AVOID-INDIRECTION, M-BOX-DST

---

## Nested type hierarchies should avoid needless indirection (M-AVOID-INDIRECTION)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Hot types should avoid nested heap indirection and consider lifting hot, cacheable deep fields to improve cache utilization.  

While the gold standard is to benchmark, a pattern that emerges repeatedly when porting C# code to Rust is to reflexively `Arc` nested types, often multiple layers deep. Although this can make sense on very wide or heavyweight types that genuinely need to be shared by multiple owners, this pattern can ruin access latency when multiple rounds of DRAM lookup have to be performed sequentially.

Where nested, shared ownership isn't strictly needed, it is usually better to start with local, embedded data, and lift cacheable fields.

```rust
// Bad, `print` (assuming it is reasonably hot) needs 2 indirections 
// to query whether it is enabled. 
struct Item {
    config: Arc<Config>,
    payload: Payload,
}

struct Config {
    feature: Arc<Feature>
}

impl Item {
    fn print(&self) {
        if self.config.feature.is_enabled() { ... }
    }
}

// Better: `enabled` resides nearby and is likely immediately available 
// once `print` is called.
struct Item {
    config: Arc<Config>,
    payload: Payload,
    enabled: bool,
}

impl Item {
    fn print(&self) {
        if self.enabled { ... }
    }
}

```


## Use boxed slices and strings for immutable owned sequences (M-BOX-DST)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Frequently used, internal, immutable sequences that will not be resized after construction should be stored as `Box<[T]>`, `Arc<str>` or similar, rather than their original  `Vec<T>` or `String` counterparts.

Regular growable collections consist of a `(ptr, len, capacity)` triple. Converting them to boxed slices makes them immutable, executes a shrink-to-fit, and drops the `capacity` bit, reducing their handle size by 1/3.  For this pattern to be useful, the following preconditions should apply:

- the sequence should be frequently instantiated (e.g., >1000's of instances),
- it must be immutable,
- it should not be user-visible, i.e., regular users would just deal with `&str` or similar.

Some collections provide dedicated methods for this, e.g., `String::into_boxed_str`.

```rust
// Bad, with many entries this wastes space and makes
// traversal ultimately slower. 
struct Data {
    ids: Vec<String>
}

// Good, reduces memory consumption and fits more elements 
// into cache.
struct Data {
    ids: Vec<Box<str>>
}
```
