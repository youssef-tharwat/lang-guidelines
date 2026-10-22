# unique-ownership

Prefer unique ownership and borrowing over `Rc`/`Arc`; use shared ownership only when the borrow structure would be unreasonably complex, or for `services-clone`.

**Why:** Shared pointers add runtime cost and hide who owns what.

**Sources:** G:avoid-rc-and-arc

---

## Avoid `Rc` and `Arc` (G:avoid-rc-and-arc)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#avoid-rc-and-arc), CC BY 3.0.

Prefer unique ownership and borrowing over `Rc` and `Arc` for managing memory.

Exception:

*   Use `Rc` and `Arc` when the alternative ownership and borrowing structure would be unreasonably complex to write, understand, or maintain. This is a judgment call to be discussed during code review.

**Rationale**

Generally, Rust allows representing object graphs without using shared ownership smart pointers. These pointers add runtime overhead and their own unique complexity. Engineers coming from other languages might tend to use `Rc` and `Arc` too quickly.
