---
type: llm
focus: {source: file, path: orders.ts}
weight: 3
---

Judge the refactored module in `orders.ts`. Pass when ALL of these hold:

1. Named exports only; no `export default`.
2. `var`, `for...in` over arrays and `new Array()` are replaced (`const`/`let`, `for...of` or `map`, literals).
3. `values.map(parseInt)` becomes an explicit arrow that parses safely (`Number()` with a NaN check, or `parseInt(v, 10)` inside an arrow at minimum).
4. The `switch` has a `default` group, and `throw 'missing total'` becomes `throw new Error(...)` (or an Error subclass).
5. `@ts-ignore` and `any` are gone; parameters are typed; the order shape is an `interface` without an `I` prefix.
6. `#count` becomes a TypeScript `private` field (or is removed), the redundant `public` modifier is gone, and the `_api` parameter loses its underscore.
7. The click handler is not installed with `.bind(this)`; it uses an arrow function (or an arrow-function property if it must be removed later).

Fail if any item is missing. List each item as met or not met before the verdict.
