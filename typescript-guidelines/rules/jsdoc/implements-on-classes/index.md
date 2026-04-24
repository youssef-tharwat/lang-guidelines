
### What it does

Reports an issue with any non-constructor function using `@implements`.

### Why is this bad?

Constructor functions should be
whether marked with `@class`, `@constructs`, or being a class constructor.

### Examples

Examples of **incorrect** code for this rule:

```javascript
/**
 * @implements {SomeClass}
 */
function quux() {}
```

Examples of **correct** code for this rule:

```javascript
class Foo {
  /**
   * @implements {SomeClass}
   */
  constructor() {}
}
/**
 * @implements {SomeClass}
 * @class
 */
function quux() {}
```

## How to use

## References
