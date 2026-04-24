
### What it does

Disallow `class` declarations that exclusively contain `static` members.

### Why is this bad?

A `class` with only `static` members should just be defined as an object instead.

### Examples

Examples of **incorrect** code for this rule:

```javascript
class A {
  static a() {}
}
```

Examples of **correct** code for this rule:

```javascript
class A {
  static a() {}

  constructor() {}
}
```

```javascript
const X = {
  foo: false,
  bar() {},
};
```

```javascript
class X {
  static #foo = false; // private field
  static bar() {}
}
```

## How to use

## References
