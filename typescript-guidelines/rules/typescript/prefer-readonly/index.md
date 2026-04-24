
### What it does

Require class members that are never reassigned to be marked `readonly`.

### Why is this bad?

Members that never change should be declared `readonly` to make class invariants explicit
and prevent accidental mutation.

### Examples

Examples of **incorrect** code for this rule:

```ts
class Counter {
  private value = 0;

  getValue() {
    return this.value;
  }
}
```

Examples of **correct** code for this rule:

```ts
class Counter {
  private readonly value = 0;

  getValue() {
    return this.value;
  }
}
```

## Configuration

This rule accepts a configuration object with the following properties:

### onlyInlineLambdas

type: `boolean`

default: `false`

Restrict checks to members immediately initialized with inline lambda values.

## How to use

## References
