
### What it does

This rule generates warnings for generator functions that do not have the yield keyword.

### Why is this bad?

Probably a mistake.

### Examples

Examples of **incorrect** code for this rule:

```javascript
function* foo() {
  return 10;
}
```

## How to use

## References
