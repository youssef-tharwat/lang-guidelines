
### What it does

Disallow all usage of `process.exit()`.

### Why is this bad?

`process.exit()` should generally only be used in command-line utilities. In all other
types of applications, the code should throw an error instead.

### Examples

Examples of **incorrect** code for this rule:

```javascript
if (problem) {
  process.exit(1);
}
```

Examples of **correct** code for this rule:

```javascript
if (problem) {
  throw new Error("message");
}
```

```
#!/usr/bin/env node
if (problem) {
  process.exit(1);
}
```

## How to use

## References
