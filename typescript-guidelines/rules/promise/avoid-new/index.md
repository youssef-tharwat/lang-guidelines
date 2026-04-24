
### What it does

Disallow creating promises with `new Promise()`.

### Why is this bad?

Many cases that use `new Promise()` could be refactored to use an
`async` function. `async` is considered more idiomatic in modern JavaScript.

### Examples

Examples of **incorrect** code for this rule:

```javascript
function foo() {
  return new Promise((resolve, reject) => {
    /* ... */
  });
}
```

Examples of **correct** code for this rule:

```javascript
async function foo() {
  // ...
}
const bar = await Promise.all([baz(), bang()]);
```

## How to use

## References
