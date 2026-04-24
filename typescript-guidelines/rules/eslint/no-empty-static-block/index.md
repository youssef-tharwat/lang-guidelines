
### What it does

Disallows the usages of empty static blocks.

### Why is this bad?

Empty block statements, while not technically errors, usually occur due
to refactoring that wasn’t completed. They can cause confusion when
reading code.

### Examples

Examples of **incorrect** code for this rule:

```js
class Foo {
  static {}
}
```

Examples of **correct** code for this rule:

```js
class Foo {
  static {
    // blocks with comments are allowed
  }
}
class Bar {
  static {
    doSomething();
  }
}
```

## How to use

## References
