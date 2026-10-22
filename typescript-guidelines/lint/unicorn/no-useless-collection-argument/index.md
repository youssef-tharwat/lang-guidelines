
### What it does

Disallow useless values or fallbacks in `Set`, `Map`, `WeakSet`, or `WeakMap`.

### Why is this bad?

It is unnecessary to pass an empty array or empty string when
constructing a `Set`, `Map`, `WeakSet`, or `WeakMap`, since
they accept nullish values.

It is also unnecessary to provide a fallback for possible nullish values.

### Examples

Examples of **incorrect** code for this rule:

```js
const set = new Set([]);
const set = new Set("");
```

Examples of **correct** code for this rule:

```js
const set = new Set();
```

Examples of **incorrect** code for this rule:

```js
const set = new Set(foo ?? []);
const set = new Set(foo ?? "");
```

Examples of **correct** code for this rule:

```js
const set = new Set(foo);
```

## How to use

## References
