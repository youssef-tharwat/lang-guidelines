
### What it does

Enforces providing a `message` when creating built-in `Error` objects to
improve readability and debugging.

### Why is this bad?

Throwing an `Error` without a message, like `throw new Error()`, provides no context
on what went wrong, making debugging harder. A clear error message improves
code clarity and helps developers quickly identify issues.

### Examples

Examples of **incorrect** code for this rule:

```javascript
throw Error();
throw new TypeError();
```

Examples of **correct** code for this rule:

```javascript
throw new Error("Unexpected token");
throw new TypeError("Number expected");
```

## How to use

## References
