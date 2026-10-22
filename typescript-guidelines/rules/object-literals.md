# object-literals

Create objects with literals, never `new Object()`; iterate keys with `for...of` over `Object.keys/values/entries` (or filter `for...in` with `hasOwnProperty`); spread only plain objects into objects; keep destructured parameters one level deep with defaults on the left (`{num = 1}: Options = {}`).

**Why:** `for...in` walks the prototype chain.

**Sources:** G:object-literals

---

## Object literals (G:object-literals)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#object-literals), CC BY 3.0.

### Do not use the `Object` constructor

The `Object` constructor is disallowed. Use an object literal (`{}` or `{a: 0, b: 1, c: 2}`) instead.

### Iterating objects

Iterating objects with `for (... in ...)` is error prone. It will include enumerable properties from the prototype chain.

Do not use unfiltered `for (... in ...)` statements:

❌ Bad:

```ts
for (const x in someObj) {
  // x could come from some parent prototype!
}
```

Either filter values explicitly with an `if` statement, or use `for (... of Object.keys(...))`.

✅ Good:

```ts
for (const x in someObj) {
  if (!someObj.hasOwnProperty(x)) continue;
  // now x was definitely defined on someObj
}
for (const x of Object.keys(someObj)) { // note: for _of_!
  // now x was definitely defined on someObj
}
for (const [key, value] of Object.entries(someObj)) { // note: for _of_!
  // now key was definitely defined on someObj
}
```

### Using spread syntax

Using spread syntax `{...bar}` is a convenient shorthand for creating a shallow copy of an object. When using spread syntax in object initialization, later values replace earlier values at the same key.

✅ Good:

```ts
const foo = {
  num: 1,
};

const foo2 = {
  ...foo,
  num: 5,
};

const foo3 = {
  num: 5,
  ...foo,
}

foo2.num === 5;
foo3.num === 1;
```

When using spread syntax, the value being spread _must_ match what is being created. That is, when creating an object, only objects may be spread; arrays and primitives (including `null` and `undefined`) _must not_ be spread. Avoid spreading objects that have prototypes other than the Object prototype (e.g. class definitions, class instances, functions) as the behavior is unintuitive (only enumerable non-prototype properties are shallow-copied).

❌ Bad:

```ts
const foo = {num: 7};
const bar = {num: 5, ...(shouldUseFoo && foo)}; // might be undefined

// Creates {0: 'a', 1: 'b', 2: 'c'} but has no length
const fooStrings = ['a', 'b', 'c'];
const ids = {...fooStrings};
```

✅ Good:

```ts
const foo = shouldUseFoo ? {num: 7} : {};
const bar = {num: 5, ...foo};
```

### Computed property names

Computed property names (e.g. `{['key' + foo()]: 42}`) are allowed, and are considered dict-style (quoted) keys (i.e., must not be mixed with non-quoted keys) unless the computed property is a [symbol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol) (e.g. `[Symbol.iterator]`).

### Object destructuring

Object destructuring patterns may be used on the left-hand side of an assignment to perform destructuring and unpack multiple values from a single object.

Destructured objects may also be used as function parameters, but should be kept as simple as possible: a single level of unquoted shorthand properties. Deeper levels of nesting and computed properties may not be used in parameter destructuring. Specify any default values in the left-hand-side of the destructured parameter (`{str = 'some default'} = {}`, rather than `{str} = {str: 'some default'}`), and if a destructured object is itself optional, it must default to `{}`.

Example:

✅ Good:

```ts
interface Options {
  /** The number of times to do something. */
  num?: number;

  /** A string to do stuff to. */
  str?: string;
}

function destructured({num, str = 'default'}: Options = {}) {}
```

Disallowed:

❌ Bad:

```ts
function nestedTooDeeply({x: {num, str}}: {x: Options}) {}
function nontrivialDefault({num, str}: Options = {num: 42, str: 'default'}) {}
```
