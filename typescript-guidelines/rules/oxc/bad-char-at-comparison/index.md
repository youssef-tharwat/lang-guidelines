
### What it does

This rule warns when the return value of the `charAt` method is used to compare a string of length greater than 1.

### Why is this bad?

The `charAt` method returns a string of length 1. If the return value is compared with a string of length greater than 1, the comparison will always be false.

### Examples

Examples of **incorrect** code for this rule:

```javascript
a.charAt(4) === "a2";
a.charAt(4) === "/n";
```

Examples of **correct** code for this rule:

```javascript
a.charAt(4) === "a";
a.charAt(4) === "\n";
```

## How to use

## References
