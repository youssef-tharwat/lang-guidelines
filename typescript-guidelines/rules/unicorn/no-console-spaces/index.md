
### What it does

Disallows leading/trailing space inside `console.log()` and similar methods.

### Why is this bad?

The `console.log()` method and similar methods join the parameters
with a space so adding a leading/trailing space to a parameter,
results in two spaces being added.

### Examples

Examples of **incorrect** code for this rule:

```javascript
console.log("abc ", "def");
```

Examples of **correct** code for this rule:

```javascript
console.log("abc", "def");
```

## How to use

## References
