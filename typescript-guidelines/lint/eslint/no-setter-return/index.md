
### What it does

Setters cannot return values.

This rule can be disabled for TypeScript code, as the TypeScript compiler
enforces this check.

### Why is this bad?

While returning a value from a setter does not produce an error, the returned value is
being ignored. Therefore, returning a value from a setter is either unnecessary or a
possible error, since the returned value cannot be used.

### Examples

Examples of **incorrect** code for this rule:

```javascript
class URL {
  set origin() {
    return true;
  }
}
```

## How to use

## References
