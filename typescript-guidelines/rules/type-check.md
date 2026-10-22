# type-check

All code must pass type checking; never use `@ts-ignore`, `@ts-expect-error` or `@ts-nocheck` outside tests, fix the underlying error instead.

**Why:** Suppressions hide the larger problem behind the error.

**Sources:** G:typescript-compiler

---

## TypeScript compiler (G:typescript-compiler)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#typescript-compiler), CC BY 3.0.

All TypeScript files must pass type checking using the standard tool chain.

### @ts-ignore

Do not use `@ts-ignore` nor the variants `@ts-expect-error` or `@ts-nocheck`.

**Why?**

They superficially seem to be an easy way to fix a compiler error, but in practice, a specific compiler error is often caused by a larger problem that can be fixed more directly.

For example, if you are using `@ts-ignore` to suppress a type error, then it's hard to predict what types the surrounding code will end up seeing. For many type errors, the advice in how to best use `any` is useful.

You may use `@ts-expect-error` in unit tests, though you generally _should not_. `@ts-expect-error` suppresses all errors. It's easy to accidentally over-match and suppress more serious errors. Consider one of:

*   When testing APIs that need to deal with unchecked values at runtime, add casts to the expected type or to `any` and add an explanatory comment. This limits error suppression to a single expression.

*   Suppress the lint warning and document why, similar to suppressing `any` lint warnings.
