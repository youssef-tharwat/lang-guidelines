---
type: llm
focus: {source: file, path: cart.ts}
weight: 3
---

Judge the module in `cart.ts`. Pass when ALL of these hold:

1. Named exports only, and exported symbols have JSDoc that adds information.
2. Discount policies are interchangeable behind one interface or function type (strategy), not a switch on a string inside the cart.
3. Fields never reassigned are `readonly`; visibility uses TypeScript `private`/`protected` (no `#private`, no redundant `public`).
4. Subscribers can unsubscribe (a returned function or a remove method), and listeners are not bound with `.bind(this)`.
5. Object shapes are `interface`s; there is no `any`; money is kept in integer cents.
6. Variables use `const`/`let` and equality uses `===`/`!==`.

Fail if any item is missing. List each item as met or not met before the verdict.
