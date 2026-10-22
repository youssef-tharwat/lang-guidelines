---
type: llm
focus: {source: file, path: userClient.ts}
weight: 3
---

Judge the module in `userClient.ts`. Pass when ALL of these hold:

1. Only named exports; no `export default` and no namespace.
2. Response JSON is treated as `unknown` and validated at runtime before it is used as a user type; no unchecked `as User` casts on raw data.
3. Failures throw an `Error` subclass (never strings or plain objects), with useful messages.
4. Object types are declared with `interface` (optional fields with `?`), and there is no `any`.
5. Equality uses `===`/`!==` and variables use `const`/`let`.
6. Exported symbols have JSDoc that adds information beyond names and types.

Fail if any item is missing. List each item as met or not met before the verdict.
