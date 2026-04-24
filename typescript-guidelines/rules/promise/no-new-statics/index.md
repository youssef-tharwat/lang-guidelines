
### What it does

Disallows calling new on static `Promise` methods.

### Why is this bad?

Calling a static `Promise` method with `new` is invalid and will result
in a `TypeError` at runtime.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const x = new Promise.resolve(value);
```

Examples of **correct** code for this rule:

```javascript
const x = Promise.resolve(value);
```

## How to use

## References
