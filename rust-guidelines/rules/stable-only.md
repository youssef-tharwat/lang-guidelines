# stable-only

Use no unstable features, run no code before `main()` (no `ctor`-style constructors), and treat other crates' `#[doc(hidden)]` items as private.

**Why:** Builds stay on stable and startup stays predictable.

**Sources:** G:no-unstable-features, G:do-not-run-code-before-main, G:do-not-access-items-marked-dochidden-that-you-dont-own

---

## No unstable features (G:no-unstable-features)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#no-unstable-features), CC BY 3.0.

Don’t use unstable features.


## Do not run code before `main()` (G:do-not-run-code-before-main)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#do-not-run-code-before-main), CC BY 3.0.

Do not cause code to run before `main()`, for example by using techniques such as the [ctor crate](https://docs.rs/ctor/latest/ctor/).


## Do not access items marked `#[doc(hidden)]` that you don’t own (G:do-not-access-items-marked-dochidden-that-you-dont-own)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#do-not-access-items-marked-dochidden-that-you-dont-own), CC BY 3.0.

Treat items marked `#[doc(hidden)]` as private. Don’t access them unless you own the code.
