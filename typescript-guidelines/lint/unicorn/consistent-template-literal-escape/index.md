
### What it does

Enforce consistent style for escaping ${ in template literals.

### Why is this bad?

Using `\${` instead of `${` can improve readability and prevent confusion.

### Examples

Examples of **incorrect** code for this rule:

```js
const foo = `$\{a}`;
```

```js
const foo = `\$\{a}`;
```

Examples of **correct** code for this rule:

```js
const foo = `\${a}`;
```

## How to use

## References
