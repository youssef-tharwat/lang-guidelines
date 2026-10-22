# simple-types

Use the simplest type construct that works: prefer interfaces and `extends` to mapped and conditional types (`Pick`, `Omit`), accepting a little repetition.

**Why:** Complex type operators are hard to read and tool.

**Sources:** G:mapped-conditional-types

---

## Mapped and conditional types (G:mapped-conditional-types)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#mapped-conditional-types), CC BY 3.0.

TypeScript's [mapped types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html) and [conditional types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html) allow specifying new types based on other types. TypeScript's standard library includes several type operators based on these (`Record`, `Partial`, `Readonly` etc).

These type system features allow succinctly specifying types and constructing powerful yet type safe abstractions. They come with a number of drawbacks though:

*   Compared to explicitly specifying properties and type relations (e.g. using interfaces and extension, see below for an example), type operators require the reader to mentally evaluate the type expression. This can make programs substantially harder to read, in particular combined with type inference and expressions crossing file boundaries.

*   Mapped & conditional types' evaluation model, in particular when combined with type inference, is underspecified, not always well understood, and often subject to change in TypeScript compiler versions. Code can accidentally compile or seem to give the right results. This increases future support cost of code using type operators.

*   Mapped & conditional types are most powerful when deriving types from complex and/or inferred types. On the flip side, this is also when they are most prone to create hard to understand and maintain programs.

*   Some language tooling does not work well with these type system features. E.g. your IDE's find references (and thus rename property refactoring) will not find properties in a `Pick<T, Keys>` type, and Code Search won't hyperlink them.

*   

The style recommendation is:

*   Always use the simplest type construct that can possibly express your code.

*   A little bit of repetition or verbosity is often much cheaper than the long term cost of complex type expressions.

*   Mapped & conditional types may be used, subject to these considerations.

For example, TypeScript's builtin `Pick<T, Keys>` type allows creating a new type by subsetting another type `T`, but simple interface extension can often be easier to understand.

```ts
interface User {
  shoeSize: number;
  favoriteIcecream: string;
  favoriteChocolate: string;
}

// FoodPreferences has favoriteIcecream and favoriteChocolate, but not shoeSize.
type FoodPreferences = Pick<User, 'favoriteIcecream'|'favoriteChocolate'>;
```

This is equivalent to spelling out the properties on `FoodPreferences`:

```ts
interface FoodPreferences {
  favoriteIcecream: string;
  favoriteChocolate: string;
}
```

To reduce duplication, `User` could extend `FoodPreferences`, or (possibly better) nest a field for food preferences:

✅ Good:

```ts
interface FoodPreferences { /* as above */ }
interface User extends FoodPreferences {
  shoeSize: number;
  // also includes the preferences.
}
```

Using interfaces here makes the grouping of properties explicit, improves IDE support, allows better optimization, and arguably makes the code easier to understand.
