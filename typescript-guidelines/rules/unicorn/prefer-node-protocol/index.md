
### What it does

Prefer using the `node:protocol` when importing Node.js builtin modules.

### Why is this bad?

Node.js builtin modules should be imported using the `node:` protocol to avoid ambiguity with local modules.

### Examples

Examples of **incorrect** code for this rule:

```javascript
import fs from "fs";
```

Examples of **correct** code for this rule:

```javascript
import fs from "node:fs";
```

## How to use

## References
