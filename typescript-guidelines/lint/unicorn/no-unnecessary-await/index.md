
### What it does

Disallow awaiting on non-promise values.

### Why is this bad?

The `await` operator should only be used on `Promise` values.

### Examples

Examples of **incorrect** code for this rule:

```javascript
async function bad() {
  await await promise;
}
```

Examples of **correct** code for this rule:

```javascript
async function bad() {
  await promise;
}
```

## How to use

## References
