
### What it does

Forbids a module from importing itself. This can sometimes happen accidentally,
especially during refactoring.

### Why is this bad?

Importing a module into itself creates a circular dependency, which can cause
runtime issues, including infinite loops, unresolved imports, or `undefined` values.

### Examples

Examples of **incorrect** code for this rule:

```javascript
// foo.js
import foo from "./foo.js"; // Incorrect: module imports itself
const foo = require("./foo"); // Incorrect: module imports itself
```

Examples of **correct** code for this rule:

```javascript
// foo.js
import bar from "./bar.js"; // Correct: module imports another module
```

## How to use

## References
