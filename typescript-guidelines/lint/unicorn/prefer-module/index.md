
### What it does

Prefer JavaScript modules (ESM) over CommonJS.

### Why is this bad?

CommonJS globals and patterns (`require`, `module`, `exports`, `__filename`, `__dirname`)
make code harder to migrate and can block ESM-only features.

### Examples

Examples of **incorrect** code for this rule:

```js
"use strict";
const foo = require("foo");
module.exports = foo;
```

Examples of **correct** code for this rule:

```js
import foo from "foo";
export default foo;
```

## How to use

## References
