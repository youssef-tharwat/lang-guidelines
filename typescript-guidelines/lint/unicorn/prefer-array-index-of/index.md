
### What it does

Enforces using `indexOf` or `lastIndexOf` instead of `findIndex` or `findLastIndex`
when the callback is a simple strict equality comparison.

### Why is this bad?

Using `findIndex(x => x === value)` is unnecessarily verbose when `indexOf(value)`
accomplishes the same thing more concisely and clearly. It also avoids the overhead
of creating a callback function.

### Examples

Examples of **incorrect** code for this rule:

```js
values.findIndex((x) => x === "foo");
values.findLastIndex((x) => x === "bar");
```

Examples of **correct** code for this rule:

```js
values.indexOf("foo");
values.lastIndexOf("bar");
```

## How to use

## References
