
### What it does

Disallows the use of approximate constants, instead preferring the use
of the constants in the `Math` object.

### Why is this bad?

Approximate constants are not as accurate as the constants in the `Math` object.
Using the `Math` constants improves code readability and accuracy.
See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global\_Objects/Math
for more information.

### Examples

Examples of **incorrect** code for this rule:

```javascript
let log10e = 0.434294;
```

Examples of **correct** code for this rule:

```javascript
let log10e = Math.LOG10E;
```

## How to use

## References
