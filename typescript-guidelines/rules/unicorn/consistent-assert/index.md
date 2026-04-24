
### What it does

Enforces consistent usage of the `assert` module.

### Why is this bad?

Inconsistent usage of the `assert` module can make code
harder to follow and understand.

`assert.ok(...)` is preferred as it makes the intent of
the assertion clearer.

### Examples

Examples of **incorrect** code for this rule:

```js
import assert from "node:assert";

assert(divide(10, 2) === 5);
```

Examples of **correct** code for this rule:

```js
import assert from "node:assert";

assert.ok(divide(10, 2) === 5);
```

## How to use

## References
