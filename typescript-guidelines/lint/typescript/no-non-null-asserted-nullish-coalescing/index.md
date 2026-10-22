
### What it does

Disallow non-null assertions in the left operand of a nullish coalescing operator.

### Why is this bad?

The ?? nullish coalescing runtime operator allows providing a default value when dealing
with `null` or `undefined`. Using a ! non-null assertion type operator in the left operand of
a nullish coalescing operator is redundant, and likely a sign of programmer error or
confusion over the two operators.

### Examples

Examples of **incorrect** code for this rule:

```ts
foo! ?? bar;
foo.bazz! ?? bar;
foo!.bazz! ?? bar;
foo()! ?? bar;

let x!: string;
x! ?? "";

let x: string;
x = foo();
x! ?? "";
```

Examples of **correct** code for this rule:

```ts
foo ?? bar;
foo ?? bar!;
foo!.bazz ?? bar;
foo!.bazz ?? bar!;
foo() ?? bar;
```

```ts
// This is considered correct code because there's no way for the user to satisfy it.
let x: string;
x! ?? "";
```

## How to use

## References
