# poison-is-panic

Treat a poisoned lock as a panic (`lock().expect("...")`); never recover the guard from a `PoisonError`.

**Why:** Poison means another thread already panicked mid-update.

**Sources:** G:handling-poison

---

## Handling poison (G:handling-poison)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#handling-poison), CC BY 3.0.

Never reach inside a poisoned mutex to get at its insides, no matter how tempting the use case may seem.
