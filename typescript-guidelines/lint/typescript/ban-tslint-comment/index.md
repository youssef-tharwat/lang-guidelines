
### What it does

This rule disallows `tslint:<rule-flag>` comments.

### Why is this bad?

Useful when migrating from TSLint to ESLint. Once TSLint has been
removed, this rule helps locate TSLint annotations

### Examples

Examples of **incorrect** code for this rule:

```ts
// tslint:disable-next-line
someCode();
```

Examples of **correct** code for this rule:

```ts
someCode();
```

## How to use

## References
