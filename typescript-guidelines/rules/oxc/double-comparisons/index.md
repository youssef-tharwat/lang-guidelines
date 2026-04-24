
### What it does

This rule checks for double comparisons in logical expressions.

### Why is this bad?

Redundant comparisons can be confusing and make code harder to understand.

### Examples

Examples of **incorrect** code for this rule:

```javascript
x === y || x < y;
x < y || x === y;
```

Examples of **correct** code for this rule:

```javascript
x <= y;
x >= y;
```

## How to use

## References
