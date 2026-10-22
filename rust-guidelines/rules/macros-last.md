# macros-last

Use a macro only when the language runs out: prefer functions, types and traits; when you must generate code, `macro_rules!` before external codegen before proc macros.

**Why:** Macros are opaque, slow builds and break at edition boundaries.

**Sources:** G:macros, M-MACRO-LAST-RESORT, M-EXAMPLE-OVER-PROC

---

## Macros (G:macros)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#macros), CC BY 3.0.

When considering how to express an API, prefer in order:

*   Regular Rust functions, types, traits, objects, and modules. (Avoid macros, code generation, and metaprogramming where possible).

*   `macro_rules!`-style macros.

*   Other code generation strategies (e.g. `genrule`)

*   `proc_macro` macros.

When you decide to use a macro or code generation, please weigh the benefits against the costs:

*   IDEs, Code Search and other developer tools will work less well on code that uses macros.

*   Macros can create dialects of the language that make it harder for engineers to work across the codebase.

*   Large scale changes are more difficult and expensive to apply.

**Rationale**

**Prefer non-macro facilities:** Macros can create dialects of the language that make it harder for engineers to work across the codebase. When a reader sees a usage of a macro, they can make fewer assumptions about that code than if it didn’t use a macro. Macros are harder to write correctly than regular Rust code.

**Use `macro_rules!` for simple code generation:** Since Rust macros operate on the AST, they can be less fragile than textual code generation.


## Macros are a last resort (M-MACRO-LAST-RESORT)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Macros should only be used if no other viable solution exists, compare this adage:

> As @littlecalculist always told me, “macros are for when you run out of language”. If you still have language left — and Rust gives you a lot of language — use the language first.
>
> @pcwalton

Macros are powerful, but come with several downsides. They

- are magic, and it can be impossible to predict what they do, or how they do it,
- disproportionally increase compilation time in projects that otherwise don't rely on them,
- can cause subtle breakage at edition boundaries where Rust syntax and semantics can change.

Counterintuitively, the more structurally complex the result of a macro expansion is, the worse an idea it is to use macros for that in the first place. The ideal macro makes your users go "_I know exactly what this will generate, but I don't want to write all of that by hand_".


## Prefer 'macros by example' over proc macros (M-EXAMPLE-OVER-PROC)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When a 'macro by example' can do the job, it should be preferred over proc macros.

Proc macros are more powerful, but their expansion can't easily be inspected. Where this versatility isn't needed, a simple 'macro by example' is the better option.

```rust
// Bad, attribute macro requires proc macro machinery, can be hard to 
// inspect in some IDEs, and isn't needed here.
#[make_new_id]
struct MyId;

// Good, easier to write, maintain and inspect, faster compilation speed.
make_new_id!(MyId);
```
