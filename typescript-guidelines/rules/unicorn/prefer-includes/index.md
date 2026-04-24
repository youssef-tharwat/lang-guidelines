
### What it does

Prefer `includes()` over `indexOf()` when checking for existence or non-existence.
All built-ins have `.includes()` in addition to `.indexOf()`.

### Why is this bad?

The `.includes()` method is more readable and less error-prone than `.indexOf()`.

### Examples

Examples of **incorrect** code for this rule:

```javascript
if (str.indexOf("foo") !== -1) {
}
```

Examples of **correct** code for this rule:

```javascript
if (str.includes("foo")) {
}
```

## How to use

## References
