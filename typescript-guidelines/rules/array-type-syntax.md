# array-type-syntax

Write `T[]` or `readonly T[]` for simple element types and `Array<T>` for anything more complex.

**Why:** Short where simple, unambiguous where not.

**Sources:** G:arrayt-type

---

## `Array<T>` Type (G:arrayt-type)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#arrayt-type), CC BY 3.0.

For simple types (containing just alphanumeric characters and dot), use the syntax sugar for arrays, `T[]` or `readonly T[]`, rather than the longer form `Array<T>` or `ReadonlyArray<T>`.

For multi-dimensional non-`readonly` arrays of simple types, use the syntax sugar form (`T[][]`, `T[][][]`, and so on) rather than the longer form.

For anything more complex, use the longer form `Array<T>`.

These rules apply at each level of nesting, i.e. a simple `T[]` nested in a more complex type would still be spelled as `T[]`, using the syntax sugar.

✅ Good:

```ts
let a: string[];
let b: readonly string[];
let c: ns.MyObj[];
let d: string[][];
let e: Array<{n: number, s: string}>;
let f: Array<string|number>;
let g: ReadonlyArray<string|number>;
let h: InjectionToken<string[]>;  // Use syntax sugar for nested types.
let i: ReadonlyArray<string[]>;
let j: Array<readonly string[]>;
```

❌ Bad:

```ts
let a: Array<string>;  // The syntax sugar is shorter.
let b: ReadonlyArray<string>;
let c: Array<ns.MyObj>;
let d: Array<string[]>;
let e: {n: number, s: string}[];  // The braces make it harder to read.
let f: (string|number)[];         // Likewise with parens.
let g: readonly (string | number)[];
let h: InjectionToken<Array<string>>;
let i: readonly string[][];
let j: (readonly string[])[];
```
