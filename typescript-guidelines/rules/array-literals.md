# array-literals

Create arrays with literals (`[]`, or `Array.from({length: n})`), never the `Array()` constructor; never put non-index properties on an array (use a `Map`); spread only iterables into arrays, never possibly-undefined values; default an optional destructured array parameter to `[]`.

**Why:** The constructor's behavior depends on its argument count.

**Sources:** G:array-literals

---

## Array literals (G:array-literals)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#array-literals), CC BY 3.0.

### Do not use the `Array` constructor

_Do not_ use the `Array()` constructor, with or without `new`. It has confusing and contradictory usage:

❌ Bad:

```ts
const a = new Array(2); // [undefined, undefined]
const b = new Array(2, 3); // [2, 3];
```

Instead, always use bracket notation to initialize arrays, or `from` to initialize an `Array` with a certain size:

✅ Good:

```ts
const a = [2];
const b = [2, 3];

// Equivalent to Array(2):
const c = [];
c.length = 2;

// [0, 0, 0, 0, 0]
Array.from<number>({length: 5}).fill(0);
```

### Do not define properties on arrays

Do not define or use non-numeric properties on an array (other than `length`). Use a `Map` (or `Object`) instead.

### Using spread syntax

Using spread syntax `[...foo];` is a convenient shorthand for shallow-copying or concatenating iterables.

✅ Good:

```ts
const foo = [
  1,
];

const foo2 = [
  ...foo,
  6,
  7,
];

const foo3 = [
  5,
  ...foo,
];

foo2[1] === 6;
foo3[1] === 1;
```

When using spread syntax, the value being spread _must_ match what is being created. When creating an array, only spread iterables. Primitives (including `null` and `undefined`) _must not_ be spread.

❌ Bad:

```ts
const foo = [7];
const bar = [5, ...(shouldUseFoo && foo)]; // might be undefined

// Creates {0: 'a', 1: 'b', 2: 'c'} but has no length
const fooStrings = ['a', 'b', 'c'];
const ids = {...fooStrings};
```

✅ Good:

```ts
const foo = shouldUseFoo ? [7] : [];
const bar = [5, ...foo];
const fooStrings = ['a', 'b', 'c'];
const ids = [...fooStrings, 'd', 'e'];
```

### Array destructuring

Array literals may be used on the left-hand side of an assignment to perform destructuring (such as when unpacking multiple values from a single array or iterable). A final rest element may be included (with no space between the `...` and the variable name). Elements should be omitted if they are unused.

✅ Good:

```ts
const [a, b, c, ...rest] = generateResults();
let [, b,, d] = someArray;
```

Destructuring may also be used for function parameters. Always specify `[]` as the default value if a destructured array parameter is optional, and provide default values on the left hand side:

✅ Good:

```ts
function destructured([a = 4, b = 2] = []) { … }
```

Disallowed:

❌ Bad:

```ts
function badDestructuring([a, b] = [4, 2]) { … }
```

Tip: For (un)packing multiple values into a function’s parameter or return, prefer object destructuring to array destructuring when possible, as it allows naming the individual elements and specifying a different type for each.
