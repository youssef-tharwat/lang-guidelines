
### What it does

Disallows useless `default` cases in `switch` statements.

### Why is this bad?

An empty case before the last `default` case is useless, as the
`default` case will catch it regardless.

### Examples

Examples of **incorrect** code for this rule:

```javascript
switch (foo) {
  case 1:
  default:
    handleDefaultCase();
    break;
}
```

Examples of **correct** code for this rule:

```javascript
switch (foo) {
  case 1:
  case 2:
    handleCase1And2();
    break;
}
```

## How to use

## References
