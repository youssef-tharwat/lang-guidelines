
### What it does

Prefer using a negative index over `.length - index` when possible.

### Why is this bad?

Using a negative index with `at` or `slice` is generally more readable
and concise than using `.length - index`.

### Examples

Examples of **incorrect** code for this rule:

```js
foo.slice(foo.length - 2, foo.length - 1);
foo.at(foo.length - 1);
```

Examples of **correct** code for this rule:

```js
foo.slice(-2, -1);
foo.at(-1);
```

## How to use

## References
