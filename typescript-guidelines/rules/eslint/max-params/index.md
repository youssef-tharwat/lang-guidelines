
### What it does

Enforce a maximum number of parameters in function definitions which by
default is three.

### Why is this bad?

Functions that take numerous parameters can be difficult to read and
write because it requires the memorization of what each parameter is,
its type, and the order they should appear in. As a result, many coders
adhere to a convention that caps the number of parameters a function
can take.

### Examples

Examples of **incorrect** code for this rule:

```javascript
function foo(bar, baz, qux, qxx) {
  doSomething();
}
```

```javascript
let foo = (bar, baz, qux, qxx) => {
  doSomething();
};
```

Examples of **correct** code for this rule:

```javascript
function foo(bar, baz, qux) {
  doSomething();
}
```

```javascript
let foo = (bar, baz, qux) => {
  doSomething();
};
```

## Configuration

This rule accepts a configuration object with the following properties:

### countThis

type: `"always" | "never" | "except-void"`

This option controls when to count a `this` parameter.

* "always": always count `this`
* "never": never count `this`
* "except-void": count `this` only when it is not type `void`

### countVoidThis

type: `boolean`

default: `false`

Deprecated alias for `countThis`.

For example `{ "countVoidThis": true }` would mean that having a function
take a `this` parameter of type `void` is counted towards the maximum number of parameters.

### max

type: `integer`

default: `3`

Maximum number of parameters allowed in function definitions.

## How to use

## References
