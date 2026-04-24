
### What it does

Disallow namespace qualifiers when the referenced name is already in scope.

### Why is this bad?

Redundant qualifiers add noise and make type references harder to read.

### Examples

Examples of **incorrect** code for this rule:

```ts
namespace A {
  export type B = number;
  const value: A.B = 1;
}
```

Examples of **correct** code for this rule:

```ts
namespace A {
  export type B = number;
  const value: B = 1;
}
```

## How to use

## References
