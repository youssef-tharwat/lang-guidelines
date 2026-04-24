
### What it does

Disallows passing `.length` or `Infinity` as the `deleteCount` or `skipCount` argument of `Array#splice()` or `Array#toSpliced()`.

### Why is this bad?

When calling `Array#splice(start, deleteCount)` or `Array#toSpliced(start, skipCount)`,
omitting the `deleteCount` or `skipCount` argument will delete or skip all elements after `start`.
Using `.length` or `Infinity` is unnecessary and makes the code more verbose.

### Examples

Examples of **incorrect** code for this rule:

```js
array.splice(1, array.length);
array.splice(1, Infinity);
array.splice(1, Number.POSITIVE_INFINITY);
array.toSpliced(1, array.length);
```

Examples of **correct** code for this rule:

```js
array.splice(1);
array.toSpliced(1);
```

## How to use

## References
