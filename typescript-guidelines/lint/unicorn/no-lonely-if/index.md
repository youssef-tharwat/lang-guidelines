
### What it does

Disallow `if` statements as the only statement in `if` blocks without `else`.

### Why is this bad?

It can be confusing to have an `if` statement without an `else` clause as the only statement in an `if` block.

### Examples

Examples of **incorrect** code for this rule:

```javascript
if (foo) {
  if (bar) {
  }
}
if (foo) if (bar) baz();
```

Examples of **correct** code for this rule:

```javascript
if (foo && bar) {
}
if (foo && bar) baz();
```

## How to use

## References
