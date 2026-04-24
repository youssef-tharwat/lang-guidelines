
### What it does

Prevents unnecessary assignment of parameter properties.

### Why is this bad?

Constructor parameters marked with one of the visibility modifiers
public, private, protected, or readonly are automatically initialized.
Providing an explicit assignment is unnecessary and can be removed.

### Examples

Examples of **incorrect** code for this rule:

```js
class Foo {
  constructor(public name: unknown) {
    this.name = name;
  }
}
```

Examples of **correct** code for this rule:

```js
class Foo {
  constructor(public name: unknown) {}
}
```

## How to use

## References
