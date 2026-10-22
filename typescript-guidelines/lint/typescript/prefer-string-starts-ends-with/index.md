
### What it does

Prefer `startsWith` and `endsWith` over manual string boundary checks.

### Why is this bad?

Boundary checks written with `slice`, `indexOf`, regex anchors, or manual indexing are
harder to read and maintain than `startsWith`/`endsWith`.

### Examples

Examples of **incorrect** code for this rule:

```ts
value.slice(0, 3) === "foo";
value.slice(-3) === "bar";
```

Examples of **correct** code for this rule:

```ts
value.startsWith("foo");
value.endsWith("bar");
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowSingleElementEquality

type: `"always" | "never"`

default: `"never"`

Whether equality checks against the first/last character are allowed.

#### `"always"`

Always allow equality checks against the first or last character.

#### `"never"`

Never allow equality checks against the first or last character.

## How to use

## References
