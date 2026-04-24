
### What it does

Disallows passing `1` to `Array.prototype.flat`.

### Why is this bad?

Passing `1` is unnecessary.

### Examples

Examples of **incorrect** code for this rule:

```js
foo.flat(1);
```

Examples of **correct** code for this rule:

```js
foo.flat();
```

## How to use

## References
