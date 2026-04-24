
### What it does

This rule applies when the comparison operator is applied two or more times in a row.

### Why is this bad?

Because comparison operator is a binary operator, it is impossible to compare three or more operands at once.
If comparison operator is used to compare three or more operands, only the first two operands are compared and the rest is compared with its result of boolean type.

### Examples

Examples of **incorrect** code for this rule:

```javascript
if ((a == b) == c) {
  console.log("a, b, and c are the same");
}
```

Examples of **correct** code for this rule:

```javascript
if (a == b && b == c) {
  console.log("a, b, and c are the same");
}
```

## How to use

## References
