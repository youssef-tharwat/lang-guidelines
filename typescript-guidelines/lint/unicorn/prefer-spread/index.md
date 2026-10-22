
### What it does

Enforces the use of [the spread operator (`...`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) over outdated patterns.

### Why is this bad?

Using the spread operator is more concise and readable.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const foo = Array.from(set);
const foo = Array.from(new Set([1, 2]));
```

Examples of **correct** code for this rule:

```javascript
[...set].map(() => {});
Array.from(...argumentsArray);
```

## How to use

## References
