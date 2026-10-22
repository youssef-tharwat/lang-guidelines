# unsafe-justified

Use `unsafe` only for a novel abstraction, a benchmarked hot path, or FFI, never to shorten safe code or bypass `Send`, `Sync` or lifetimes; isolate it in the smallest module that can uphold its invariants, give every block a `// SAFETY:` comment, and test it under Miri.

**Why:** Unsafe moves the compiler's job onto review.

**Sources:** M-UNSAFE, G:unsafe-code, P:patterns/structural/unsafe-mods

---

## Unsafe needs reason, should be avoided (M-UNSAFE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

You must have a valid reason to use `unsafe`. The only valid reasons are

1) novel abstractions, e.g., a new smart pointer or allocator,
1) performance, e.g., attempting to call `.get_unchecked()`,
1) FFI and platform calls, e.g., calling into C or the kernel, ...

Unsafe code lowers the guardrails used by the compiler, transferring some of the compiler's responsibilities
to the programmer. Correctness of the resulting code relies primarily on catching all mistakes in code review,
which is error-prone. Mistakes in unsafe code may introduce high-severity security vulnerabilities.

You must not use ad-hoc `unsafe` to

- shorten a performant and safe Rust program, e.g., 'simplify' enum casts via `transmute`,
- bypass `Send` and similar bounds, e.g., by doing `unsafe impl Send ...`,
- bypass lifetime requirements via `transmute` and similar.

Ad-hoc here means `unsafe` embedded in otherwise unrelated code. It is of course permissible to create properly designed, sound abstractions doing these things.

In any case, `unsafe` must follow the guidelines outlined below.

### Novel Abstractions

- [ ] Verify there is no established alternative. If there is, prefer that.
- [ ] Your abstraction must be minimal and testable.
- [ ] It must be hardened and tested against ["adversarial code"](https://cheats.rs/#adversarial-code), esp.
  - If they accept closures they must become invalid (e.g., poisoned) if the closure panics
  - They must assume any safe trait is misbehaving, esp. `Deref`, `Clone` and `Drop`.
- [ ] Any use of `unsafe` must be accompanied by plain-text reasoning outlining its safety
- [ ] It must pass [Miri](https://github.com/rust-lang/miri), including adversarial test cases
- [ ] It must follow all other [unsafe code guidelines](https://rust-lang.github.io/unsafe-code-guidelines/)

### Performance

- [ ] Using `unsafe` for performance reasons should only be done after benchmarking
- [ ] Any use of `unsafe` must be accompanied by plain-text reasoning outlining its safety. This applies to both
  calling `unsafe` methods, as well as providing `_unchecked` ones.
- [ ] The code in question must pass [Miri](https://github.com/rust-lang/miri)
- [ ] You must follow the [unsafe code guidelines](https://rust-lang.github.io/unsafe-code-guidelines/)

### FFI

- [ ] We recommend you use an established interop library to avoid `unsafe` constructs
- [ ] You must follow the [unsafe code guidelines](https://rust-lang.github.io/unsafe-code-guidelines/)
- [ ] You must document your generated bindings to make it clear which call patterns are permissible

### Further Reading

- [Nomicon](https://doc.rust-lang.org/nightly/nomicon/)
- [Unsafe Code Guidelines](https://rust-lang.github.io/unsafe-code-guidelines/)
- [Miri](https://github.com/rust-lang/miri)
- ["Adversarial code"](https://cheats.rs/#adversarial-code)


## Unsafe code (G:unsafe-code)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#unsafe-code), CC BY 3.0.

Don’t write unsafe code unless there is no way to implement the same functionality with safe code.

If you do have to write unsafe code:

*   Encapsulate unsafe code in a safe abstraction and isolate it from business logic as much as possible. Ideally, unsafe code should be in a separate crate with few dependencies beyond the standard library.

*   Add a safety comment starting with `SAFETY:` that explains why the code is correct.

*   Add a technical justification for unsafe code. Depending on context, this can be a justification for an individual unsafe block or a more general justification that covers an entire file or build target. The justification should answer these questions:

    *   Why is this code not written in an equivalent safe way?

    *   If the reason is performance, are there benchmarks?


## Contain unsafety in small modules (P:patterns/structural/unsafe-mods)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/structural/unsafe-mods.html), MPL-2.0.

### Description

If you have `unsafe` code, create the smallest possible module that can uphold
the needed invariants to build a minimal safe interface upon the unsafety. Embed
this into a larger module that contains only safe code and presents an ergonomic
interface. Note that the outer module can contain unsafe functions and methods
that call directly into the unsafe code. Users may use this to gain speed
benefits.

### Advantages

- This restricts the unsafe code that must be audited
- Writing the outer module is much easier, since you can count on the guarantees
  of the inner module

### Disadvantages

- Sometimes, it may be hard to find a suitable interface.
- The abstraction may introduce inefficiencies.

### Examples

- The [`toolshed`](https://docs.rs/toolshed) crate contains its unsafe
  operations in submodules, presenting a safe interface to users.
- `std`'s `String` class is a wrapper over `Vec<u8>` with the added invariant
  that the contents must be valid UTF-8. The operations on `String` ensure this
  behavior. However, users have the option of using an `unsafe` method to create
  a `String`, in which case the onus is on them to guarantee the validity of the
  contents.

### See also

- [Ralf Jung's Blog about invariants in unsafe code](https://www.ralfj.de/blog/2018/08/22/two-kinds-of-invariants.html)
