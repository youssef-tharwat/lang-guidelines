
### What it does

Disallow assigning `this` to a variable.

### Why is this bad?

Assigning `this` to a variable is unnecessary and confusing.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const foo = this;
class Bar {
  method() {
    foo.baz();
  }
}

new Bar().method();
```

Examples of **correct** code for this rule:

```javascript
class Bar {
  constructor(fooInstance) {
    this.fooInstance = fooInstance;
  }
  method() {
    this.fooInstance.baz();
  }
}

new Bar(this).method();
```

## How to use

## References
