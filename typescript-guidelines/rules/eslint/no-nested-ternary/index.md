
### What it does

Disallows nested ternary expressions to improve code readability and maintainability.

### Why is this bad?

Nested ternary expressions make code harder to read and understand. They can lead to complex, difficult-to-debug logic.

### Examples

Examples of **incorrect** code for this rule:

```js
const result = condition1 ? (condition2 ? "a" : "b") : "c";
```

Examples of **correct** code for this rule:

```js
let result;
if (condition1) {
  result = condition2 ? "a" : "b";
} else {
  result = "c";
}
```

## How to use

## References
