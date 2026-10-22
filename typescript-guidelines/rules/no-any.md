# no-any

Avoid `any`: use a specific type, `unknown` narrowed with a type guard, or a generic; if `any` is truly needed (a partial test mock), suppress the lint on that line and say why. Avoid `{}`: use `unknown`, `Record<string, T>` or `object`.

**Why:** `any` and `{}` switch off type checking.

**Sources:** G:any, G:empty-interface-type

---

## `any` Type (G:any)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#any), CC BY 3.0.

TypeScript's `any` type is a super and subtype of all other types, and allows dereferencing all properties. As such, `any` is dangerous - it can mask severe programming errors, and its use undermines the value of having static types in the first place.

**Consider _not_ to use `any`.** In circumstances where you want to use `any`, consider one of:

*   Provide a more specific type

*   Use `unknown`

*   Suppress the lint warning and document why

### Providing a more specific type

Use interfaces , an inline object type, or a type alias:

✅ Good:

```ts
// Use declared interfaces to represent server-side JSON.
declare interface MyUserJson {
  name: string;
  email: string;
}

// Use type aliases for types that are repetitive to write.
type MyType = number|string;

// Or use inline object types for complex returns.
function getTwoThings(): {something: number, other: string} {
  // ...
  return {something, other};
}

// Use a generic type, where otherwise a library would say `any` to represent
// they don't care what type the user is operating on (but note "Return type
// only generics" below).
function nicestElement<T>(items: T[]): T {
  // Find the nicest element in items.
  // Code can also put constraints on T, e.g. <T extends HTMLElement>.
}
```

### Using `unknown` over `any`

The `any` type allows assignment into any other type and dereferencing any property off it. Often this behaviour is not necessary or desirable, and code just needs to express that a type is unknown. Use the built-in type `unknown` in that situation — it expresses the concept and is much safer as it does not allow dereferencing arbitrary properties.

✅ Good:

```ts
// Can assign any value (including null or undefined) into this but cannot
// use it without narrowing the type or casting.
const val: unknown = value;
```

❌ Bad:

```ts
const danger: any = value /* result of an arbitrary expression */;
danger.whoops();  // This access is completely unchecked!
```

To safely use `unknown` values, narrow the type using a [type guard](https://www.typescriptlang.org/docs/handbook/advanced-types.html#type-guards-and-differentiating-types)

### Suppressing `any` lint warnings

Sometimes using `any` is legitimate, for example in tests to construct a mock object. In such cases, add a comment that suppresses the lint warning, and document why it is legitimate.

✅ Good:

```ts
// This test only needs a partial implementation of BookService, and if
// we overlooked something the test will fail in an obvious way.
// This is an intentionally unsafe partial mock
// tslint:disable-next-line:no-any
const mockBookService = ({get() { return mockBook; }} as any) as BookService;
// Shopping cart is not used in this test
// tslint:disable-next-line:no-any
const component = new MyComponent(mockBookService, /* unused ShoppingCart */ null as any);
```


## `{}` Type (G:empty-interface-type)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#empty-interface-type), CC BY 3.0.

The `{}` type, also known as an _empty interface_ type, represents a interface with no properties. An empty interface type has no specified properties and therefore any non-nullish value is assignable to it.

❌ Bad:

```ts
let player: {};

player = {
  health: 50,
}; // Allowed.

console.log(player.health) // Property 'health' does not exist on type '{}'.
```

❌ Bad:

```ts
function takeAnything(obj:{}) {

}

takeAnything({});
takeAnything({ a: 1, b: 2 });
```

Google3 code **should not** use `{}` for most use cases. `{}` represents any non-nullish primitive or object type, which is rarely appropriate. Prefer one of the following more-descriptive types:

*   `unknown` can hold any value, including `null` or `undefined`, and is generally more appropriate for opaque values.

*   `Record<string, T>` is better for dictionary-like objects, and provides better type safety by being explicit about the type `T` of contained values (which may itself be `unknown`).

*   `object` excludes primitives as well, leaving only non-nullish functions and objects, but without any other assumptions about what properties may be available.
