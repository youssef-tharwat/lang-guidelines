
### What it does

Enforce consistent return behavior in functions.

### Why is this bad?

Mixing value-returning and non-value-returning code paths makes control flow harder to
reason about and frequently indicates a bug.

### Examples

Examples of **incorrect** code for this rule:

```ts
function maybe(flag: boolean): number {
  if (flag) {
    return 1;
  }
  return;
}
```

Examples of **correct** code for this rule:

```ts
function maybe(flag: boolean): number {
  if (flag) {
    return 1;
  }
  return 0;
}
```

## Configuration

This rule accepts a configuration object with the following properties:

### treatUndefinedAsUnspecified

type: `boolean`

default: `false`

Treat explicit `return undefined` as equivalent to an unspecified return.

## How to use

## References
