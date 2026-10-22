
### What it does

Disallow `require` statements except in import statements.

**NOTE**: This rule is intentionally missing the `allow` option from the original typescript-eslint rule.
This rule is deprecated in the upstream plugin and the `typescript/no-require-imports` rule should be
used instead.

### Why is this bad?

In other words, the use of forms such as var foo = require("foo") are banned. Instead use ES module imports or import foo = require("foo") imports.

```typescript
var foo = require("foo");
const foo = require("foo");
let foo = require("foo");
```

## How to use

## References
