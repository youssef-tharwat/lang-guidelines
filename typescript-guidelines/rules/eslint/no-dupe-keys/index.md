
### What it does

Disallow duplicate keys in object literals.

This rule can be disabled for TypeScript code, as the TypeScript compiler
enforces this check.

### Why is this bad?

Multiple properties with the same key in object literals can cause
unexpected behavior in your application.

### Examples

Examples of **incorrect** code for this rule:

```js
var foo = {
  bar: "baz",
  bar: "qux",
};

var foo = {
  bar: "baz",
  bar: "qux",
};

var foo = {
  0x1: "baz",
  1: "qux",
};
```

Examples of **correct** code for this rule:

```js
var foo = {
  bar: "baz",
  qux: "qux",
};
```

## How to use

## References
