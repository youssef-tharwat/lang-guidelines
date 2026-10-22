# interfaces-over-aliases

Declare object types with `interface`, not object-literal `type` aliases.

**Why:** Two equivalent forms; pick the one with better tooling.

**Sources:** G:prefer-interfaces

---

## Prefer interfaces over type literal aliases (G:prefer-interfaces)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#prefer-interfaces), CC BY 3.0.

TypeScript supports [type aliases](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-aliases) for naming a type expression. This can be used to name primitives, unions, tuples, and any other types.

However, when declaring types for objects, use interfaces instead of a type alias for the object literal expression.

✅ Good:

```ts
interface User {
  firstName: string;
  lastName: string;
}
```

❌ Bad:

```ts
type User = {
  firstName: string,
  lastName: string,
}
```

**Why?**

These forms are nearly equivalent, so under the principle of just choosing one out of two forms to prevent variation, we should choose one. Additionally, there are also [interesting technical reasons to prefer interface](https://ncjamieson.com/prefer-interfaces/). That page quotes the TypeScript team lead: Honestly, my take is that it should really just be interfaces for anything that they can model. There is no benefit to type aliases when there are so many issues around display/perf.
