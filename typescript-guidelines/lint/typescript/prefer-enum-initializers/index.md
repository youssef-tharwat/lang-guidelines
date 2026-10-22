
### What it does

Require each enum member value to be explicitly initialized.

### Why is this bad?

In projects where the value of `enum` members are important, allowing implicit values for enums can cause bugs if enums are modified over time.

### Examples

Examples of **incorrect** code for this rule:

```typescript
// wrong, the value of `Close` is not constant
enum Status {
  Open = 1,
  Close,
}
```

Examples of **correct** code for this rule:

```typescript
enum Status {
  Open = 1,
  Close = 2,
}
```

## How to use

## References
