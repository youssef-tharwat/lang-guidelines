# mimalloc

Set `mimalloc` as the application's global allocator.

**Why:** Measurable speedups on allocation-heavy paths.

**Binding in:** applications only.

**Sources:** M-MIMALLOC-APPS

---

## Use mimalloc for apps (M-MIMALLOC-APPS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Applications should set [mimalloc](https://crates.io/crates/mimalloc) as their global allocator. This usually results in notable performance
increases along allocating hot paths; we have seen up to 25% benchmark improvements.

Changing the allocator only takes a few lines of code. Add mimalloc to your `Cargo.toml` like so:

```toml
[dependencies]
mimalloc = { version = "0.1" } # Or later version if available
```

Then use it from your `main.rs`:

```rust
use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;
```
