# no-catch-unwind

Use `panic::catch_unwind` only as a last resort at an entry point (for example per request in a server, so other requests can finish) and then restart the application; libraries never catch a panic to continue, and code must stay correct under `panic = "abort"`.

**Why:** A caught panic can leave otherwise impossible state behind.

**Sources:** G:dont-call-paniccatch_unwind, M-PANIC-CONTINUATION

---

## Don’t call `panic::catch_unwind` (G:dont-call-paniccatch_unwind)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#dont-call-paniccatch_unwind), CC BY 3.0.

Use of `panic::catch_unwind` is prohibited in first-party Rust code.

Exceptions:

*   It is acceptable as a defense in depth mechanism as long as it is never _relied_ upon for any properties. A codebase that is already attempting to avoid panics may choose to wrap critical entry points with a `catch_unwind` recovery mechanism just in case a panic slips through. Code authors must convince the reviewer that the codebase is doing most of what it can to avoid panics. This exception only applies to code that has the possibility of being run with `panic=unwind` (so this does not apply to Chrome, Android, Fuchsia).

**Rationale**

Rust code may be used in many environments, and `panic::catch_unwind` will only function correctly in environments with `panic=unwind`. While the final panic disposition of prod binaries has not yet been determined, Chrome, Android, and Fuchsia all require `panic=abort`.


## Panic continuation is last resort (M-PANIC-CONTINUATION)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Panic recovery via `catch_unwind()` is a matter of last resort and must generally be followed by a controlled application restart.

Panics indicate the program has reached an unrecoverable state (compare M-PANIC-IS-STOP and M-PANIC-ON-BUG). Library code in particular should not attempt to catch a panic and continue execution, as there is a risk of observing otherwise impossible state:

```rust
thread_local! {
    static ALWAYS_EQUAL: RefCell<(i32, i32)> = RefCell::new((0, 0));
}

fn main() {
    let _ = panic::catch_unwind(|| {
        ALWAYS_EQUAL.with_borrow_mut(|p| {
            p.0 += 1;        
            panic!("Assume some user-provided closure failed here");  
            p.1 += 1;
        });
    });

    ALWAYS_EQUAL.with_borrow(|p| {
        assert_eq!(p.0, p.1);  // Broken!
    });
}
```

Although the example above is slightly contrived, the side effects and interactions of a caught panic can be harder to identify, can have wide blast radius, and be subtle.

Systems where many unrelated tasks are in flight (e.g., server request handlers) can use `catch_unwind` on a per-request basis, but should still promote an application restart after a request handler caused a panic. The purpose of `catch_unwind` here is not to continue execution indefinitely, but to allow all other requests to gracefully finish.
