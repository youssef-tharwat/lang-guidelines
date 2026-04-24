
### What it does

This rule finds ternary expressions that can be simplified to a logical operator.

### Why is this bad?

Using a logical operator is shorter and simpler than a ternary expression.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const foo = bar ? bar : baz;
console.log(foo ? foo : bar);
```

Examples of **correct** code for this rule:

```javascript
const foo = bar || baz;
console.log(foo ?? bar);
```

## How to use

## References
