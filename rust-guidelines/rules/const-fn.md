# const-fn

Mark a public function `const` only if it will stay `const`.

**Why:** Removing `const` is a breaking change.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** G:use-const-functions-responsibly

---

## Use `const` functions responsibly (G:use-const-functions-responsibly)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#use-const-functions-responsibly), CC BY 3.0.

Mark a public function as `const` only if you expect it to remain `const` in the future (or can commit to helping clients migrate when it changes).

**Rationale**

It’s a breaking change to turn a `const` function into a regular function.
