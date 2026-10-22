
### What it does

Enforces a consistent style for exposing literal values on classes.

### Why is this bad?

Mixing readonly fields and trivial literal getters for the same kind of value
makes class APIs inconsistent and harder to scan.

### Examples

Examples of **incorrect** code for this rule (default `"fields"`):

```ts
class C {
  get name() {
    return "oxc";
  }
}
```

Examples of **correct** code for this rule:

```ts
class C {
  readonly name = "oxc";
}
```

## Configuration

This rule accepts one of the following string values:

### `"fields"`

Enforce using readonly fields for literal values.

Examples of **incorrect** code with this option:

```ts
class C {
  get name() {
    return "oxc";
  }
}
```

Examples of **correct** code with this option:

```ts
class C {
  readonly name = "oxc";
}
```

### `"getters"`

Enforce using getters for literal values.

Examples of **incorrect** code with this option:

```ts
class C {
  readonly name = "oxc";
}
```

Examples of **correct** code with this option:

```ts
class C {
  get name() {
    return "oxc";
  }
}
```

## How to use

## References
