# structural-types

Declare structural types with interfaces, not classes, and annotate structural values where they are declared (`const foo: Foo = {...}`) so type errors appear there.

**Why:** Errors point at the declaration, not a distant call site.

**Sources:** G:use-structural-types

---

## Use structural types (G:use-structural-types)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#use-structural-types), CC BY 3.0.

TypeScript's type system is structural, not nominal. That is, a value matches a type if it has at least all the properties the type requires and the properties' types match, recursively.

When providing a structural-based implementation, explicitly include the type at the declaration of the symbol (this allows more precise type checking and error reporting).

✅ Good:

```ts
const foo: Foo = {
  a: 123,
  b: 'abc',
}
```

❌ Bad:

```ts
const badFoo = {
  a: 123,
  b: 'abc',
}
```

Use interfaces to define structural types, not classes

✅ Good:

```ts
interface Foo {
  a: number;
  b: string;
}

const foo: Foo = {
  a: 123,
  b: 'abc',
}
```

❌ Bad:

```ts
class Foo {
  readonly a: number;
  readonly b: number;
}

const foo: Foo = {
  a: 123,
  b: 'abc',
}
```

**Why?**

The badFoo object above relies on type inference. Additional fields could be added to badFoo and the type is inferred based on the object itself.

When passing a badFoo to a function that takes a Foo, the error will be at the function call site, rather than at the object declaration site. This is also useful when changing the surface of an interface across broad codebases.

```ts
interface Animal {
  sound: string;
  name: string;
}

function makeSound(animal: Animal) {}

/**
 * 'cat' has an inferred type of '{sound: string}'
 */
const cat = {
  sound: 'meow',
};

/**
 * 'cat' does not meet the type contract required for the function, so the
 * TypeScript compiler errors here, which may be very far from where 'cat' is
 * defined.
 */
makeSound(cat);

/**
 * Horse has a structural type and the type error shows here rather than the
 * function call.  'horse' does not meet the type contract of 'Animal'.
 */
const horse: Animal = {
  sound: 'niegh',
};

const dog: Animal = {
  sound: 'bark',
  name: 'MrPickles',
};

makeSound(dog);
makeSound(horse);
```
