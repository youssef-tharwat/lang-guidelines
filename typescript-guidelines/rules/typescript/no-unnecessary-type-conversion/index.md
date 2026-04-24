
### What it does

Disallow unnecessary type conversion expressions.

### Why is this bad?

Type conversions that do not change a value's type or runtime behavior
add noise and can obscure intent.

### Examples

Examples of **incorrect** code for this rule:

```ts
const value = String("asdf");
```

Examples of **correct** code for this rule:

```ts
const value = "asdf";
```

## How to use

## References
