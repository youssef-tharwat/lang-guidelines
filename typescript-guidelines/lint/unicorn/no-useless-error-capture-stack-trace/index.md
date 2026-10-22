
### What it does

Disallows unnecessary `Error.captureStackTrace(…)` in error constructors.

### Why is this bad?

Calling `Error.captureStackTrace(…)` inside the constructor of a built-in `Error` subclass
is unnecessary, since the `Error` constructor calls it automatically.

### Examples

Examples of **incorrect** code for this rule:

```js
class MyError extends Error {
  constructor() {
    Error.captureStackTrace(this, MyError);
  }
}
```

Examples of **correct** code for this rule:

```js
class MyError extends Error {
  constructor() {
    // No need to call Error.captureStackTrace
  }
}
```

## How to use

## References
