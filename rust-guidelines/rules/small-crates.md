# small-crates

Split a module into its own crate when it can be used on its own; use features only for functionality that can't stand alone.

**Why:** Faster builds and no dependency cycles.

**Sources:** M-SMALLER-CRATES, P:patterns/structural/small-crates

---

## If in doubt, split the crate (M-SMALLER-CRATES)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

You should err on the side of having too many crates rather than too few, as this leads to dramatic compile time improvements—especially
during the development of these crates—and prevents cyclic component dependencies.

Essentially, if a submodule can be used independently, its contents should be moved into a separate crate.

Performing this crate split may cause you to lose access to some `pub(crate)` fields or methods. In many situations, this is a desirable
side-effect and should prompt you to design more flexible abstractions that would give your users similar affordances.

In some cases, it is desirable to re-join individual crates back into a single _umbrella crate_, such as when dealing with proc macros, or runtimes.
Functionality split for technical reasons (e.g., a `foo_proc` proc macro crate) should always be re-exported. Otherwise, re-exports should be used sparingly.

> ###  Features vs. Crates
>
> As a rule of thumb, crates are for items that can reasonably be used on their own. Features should unlock extra functionality that
> can't live on its own. In the case of umbrella crates, see below, features may also be used to enable constituents (but then that functionality
> was extracted into crates already).
>
> For example, if you defined a `web` crate with the following modules, users only needing client calls would also have to pay for the compilation of server code:
>
> ```text
> web::server
> web::client
> web::protocols
> ```
>
> Instead, you should introduce individual crates that give users the ability to pick and choose:
>
> ```text
> web_server
> web_client
> web_protocols
> ```


## Prefer small crates (P:patterns/structural/small-crates)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/structural/small-crates.html), MPL-2.0.

### Description

Prefer small crates that do one thing well.

Cargo and crates.io make it easy to add third-party libraries, much more so than
in say C or C++. Moreover, since packages on crates.io cannot be edited or
removed after publication, any build that works now should continue to work in
the future. We should take advantage of this tooling, and use smaller, more
fine-grained dependencies.

### Advantages

- Small crates are easier to understand, and encourage more modular code.
- Crates allow for re-using code between projects. For example, the `url` crate
  was developed as part of the Servo browser engine, but has since found wide
  use outside the project.
- Since the compilation unit of Rust is the crate, splitting a project into
  multiple crates can allow more of the code to be built in parallel.

### Disadvantages

- This can lead to "dependency hell", when a project depends on multiple
  conflicting versions of a crate at the same time. For example, the `url` crate
  has both versions 1.0 and 0.5. Since the `Url` from `url:1.0` and the `Url`
  from `url:0.5` are different types, an HTTP client that uses `url:0.5` would
  not accept `Url` values from a web scraper that uses `url:1.0`.
- Packages on crates.io are not curated. A crate may be poorly written, have
  unhelpful documentation, or be outright malicious.
- Two small crates may be less optimized than one large one, since the compiler
  does not perform link-time optimization (LTO) by default.

### Examples

The [`url`](https://crates.io/crates/url) crate provides tools for working with
URLs.

The [`num_cpus`](https://crates.io/crates/num_cpus) crate provides a function to
query the number of CPUs on a machine.

The [`ref_slice`](https://crates.io/crates/ref_slice) crate provides functions
for converting `&T` to `&[T]`. (Historical example)

### See also

- [crates.io: The Rust community crate host](https://crates.io/)
