
### What it does

Disallow duplicate enum member values.

### Why is this bad?

Although TypeScript supports duplicate enum member values, people
usually expect members to have unique values within the same enum.
Duplicate values can lead to bugs that are hard to track down.

### Examples

This rule disallows defining an enum with multiple members initialized
to the same value. Members without initializers will not be checked.

Example of **incorrect** code:

```ts
enum E {
  A = 0,
  B = 0,
}
```

```ts
enum E {
  A = "A",
  B = "A",
}
```

Example of **correct** code:

```ts
enum E {
  A = 0,
  B = 1,
}
```

```ts
enum E {
  A = "A",
  B = "B",
}
```

```ts
enum E {
  A,
  B,
}
```

## How to use

## References
