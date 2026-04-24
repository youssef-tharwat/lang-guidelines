
### What it does

Disallow returning value from constructor.

### Why is this bad?

In JavaScript, returning a value in the constructor of a class may be a mistake.
Forbidding this pattern prevents mistakes resulting from unfamiliarity with the language or a copy-paste error.

### Examples

Examples of **incorrect** code for this rule:

```js
class C {
  constructor() {
    return 42;
  }
}
```

Examples of **correct** code for this rule:

```js
class C {
  constructor() {
    this.value = 42;
  }
}
```

## How to use

## References
