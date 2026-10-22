# enum-not-bool

Use a two-variant `enum` instead of a `bool` parameter whose meaning is unclear at the call site.

**Why:** `render(doc, Mode::Draft)` reads; `render(doc, true)` doesn't.

**Sources:** G:prefer-enum-over-bool-in-apis

---

## Prefer `enum` over `bool` in APIs (G:prefer-enum-over-bool-in-apis)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-enum-over-bool-in-apis), CC BY 3.0.

Use `enum` function parameters instead of `bool` in cases where the purpose of the parameter is not obvious.

If you do use `bool`, consider using an inline comment to document the purpose of the `bool` in an argument list.
