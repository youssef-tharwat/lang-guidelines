
### What it does

Disallows unnecessarily passing a second argument to `slice(...)`, for
cases where it would not change the result.

### Why is this bad?

When using `.slice(...)` without a second argument, the second argument
defaults to the object's length. As such, passing the length explicitly

* or using `Infinity` - is unnecessary.

### Examples

Examples of **incorrect** code for this rule:

```js
const foo = string.slice(1, string.length);
const foo = string.slice(1, Infinity);
const foo = string.slice(1, Number.POSITIVE_INFINITY);
```

Examples of **correct** code for this rule:

```js
const foo = string.slice(1);
```

## How to use

## References
