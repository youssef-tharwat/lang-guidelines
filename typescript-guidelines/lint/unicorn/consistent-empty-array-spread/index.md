
### What it does

When spreading a ternary in an array, we can use both `[]` and `''` as fallbacks,
but it's better to have consistent types in both branches.

### Why is this bad?

Having consistent types in both branches makes the code easier to read and understand.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const array = [a, ...(foo ? [b, c] : "")];

const array = [a, ...(foo ? "bc" : [])];
```

Examples of **correct** code for this rule:

```javascript
const array = [a, ...(foo ? [b, c] : [])];

const array = [a, ...(foo ? "bc" : "")];
```

## How to use

## References
