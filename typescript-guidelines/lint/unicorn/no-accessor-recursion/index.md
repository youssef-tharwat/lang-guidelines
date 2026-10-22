
### What it does

Disallow recursive access to `this` within getters and setters.

### Why is this bad?

This rule prevents recursive access to `this` within getter and
setter methods in objects and classes, avoiding infinite recursion
and stack overflow errors.

### Examples

Examples of **incorrect** code for this rule:

```js
const foo = {
  get bar() {
    return this.bar;
  },
};

const baz = {
  set bar(value) {
    this.bar = value;
  },
};
```

Examples of **correct** code for this rule:

```js
const foo = {
  get bar() {
    return this.qux;
  },
};

const baz = {
  set bar(value) {
    this._bar = value;
  },
};
```

## How to use

## References
