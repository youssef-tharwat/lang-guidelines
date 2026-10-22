# type-inference

Leave trivially inferred types unannotated (`const x = 15`), but annotate empty generic containers (`new Set<string>()`) and complex expressions whose type isn't obvious; return-type annotations are the author's call.

**Why:** Annotations should add information.

**Sources:** G:type-inference

---

## Type inference (G:type-inference)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#type-inference), CC BY 3.0.

Code _may_ rely on type inference as implemented by the TypeScript compiler for all type expressions (variables, fields, return types, etc).

✅ Good:

```ts
const x = 15;  // Type inferred.
```

Leave out type annotations for trivially inferred types: variables or parameters initialized to a `string`, `number`, `boolean`, `RegExp` literal or `new` expression.

❌ Bad:

```ts
const x: boolean = true;  // Bad: 'boolean' here does not aid readability
```

❌ Bad:

```ts
// Bad: 'Set' is trivially inferred from the initialization
const x: Set<string> = new Set();
```

Explicitly specifying types may be required to prevent generic type parameters from being inferred as `unknown`. For example, initializing generic types with no values (e.g. empty arrays, objects, `Map`s, or `Set`s).

✅ Good:

```ts
const x = new Set<string>();
```

For more complex expressions, type annotations can help with readability of the program:

❌ Bad:

```ts
// Hard to reason about the type of 'value' without an annotation.
const value = await rpc.getSomeValue().transform();
```

✅ Good:

```ts
// Can tell the type of 'value' at a glance.
const value: string[] = await rpc.getSomeValue().transform();
```

Whether an annotation is required is decided by the code reviewer.

### Return types

Whether to include return type annotations for functions and methods is up to the code author. Reviewers _may_ ask for annotations to clarify complex return types that are hard to understand. Projects _may_ have a local policy to always require return types, but this is not a general TypeScript style requirement.

There are two benefits to explicitly typing out the implicit return values of functions and methods:

*   More precise documentation to benefit readers of the code.

*   Surface potential type errors faster in the future if there are code changes that change the return type of the function.
