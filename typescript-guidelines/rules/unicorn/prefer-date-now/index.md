
### What it does

Prefers use of `Date.now()` over `new Date().getTime()` or `new Date().valueOf()`.

### Why is this bad?

Using `Date.now()` is shorter and nicer than `new Date().getTime()`, and avoids unnecessary instantiation of `Date` objects.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const ts = new Date().getTime();
const ts = new Date().valueOf();
```

Examples of **correct** code for this rule:

```javascript
const ts = Date.now();
```

## How to use

## References
