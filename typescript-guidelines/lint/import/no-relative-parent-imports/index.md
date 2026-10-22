
### What it does

Forbids importing modules from parent directories using relative paths.

### Why is this bad?

This restriction enforces tree-like folder structures instead of complex
graph-like structures, making large codebases easier to maintain.
Dependencies flow in one direction (parent to child), which clarifies
module relationships.

### Examples

Examples of **incorrect** code for this rule:

```javascript
import foo from "../bar";
import foo from "../../utils/helper";
const baz = require("../config");
export { qux } from "../shared";
```

Examples of **correct** code for this rule:

```javascript
import foo from "lodash";
import a from "./lib/a";
import b from "./b";
```

## How to use

## References
