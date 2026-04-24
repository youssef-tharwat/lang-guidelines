
### What it does

Prefers omitting the catch binding parameter if it is unused.

### Why is this bad?

It is unnecessary to bind the error to a variable if it is not used.

### Examples

Examples of **incorrect** code for this rule:

```javascript
try {
  // ...
} catch (e) {}
```

Examples of **correct** code for this rule:

```javascript
try {
  // ...
} catch {}
```

## How to use

## References
