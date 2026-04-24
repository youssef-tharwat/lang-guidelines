
### What it does

Prefers ternary expressions over simple `if`/`else` statements.

### Why is this bad?

Simple `if`/`else` branches for the same operation are often shorter and
clearer when expressed as a ternary.

### Examples

Examples of **incorrect** code for this rule:

```js
if (test) {
  return a;
} else {
  return b;
}
```

Examples of **correct** code for this rule:

```js
return test ? a : b;
```

## Configuration

This rule accepts one of the following string values:

### `"always"`

Always enforce ternary usage when the branches can be safely merged.

### `"only-single-line"`

Only enforce ternary usage when the condition and both branches are single-line.

## How to use

## References
