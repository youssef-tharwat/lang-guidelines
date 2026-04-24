
### What it does

Forbids the use of AMD `require` and `define` calls.

### Why is this bad?

AMD (Asynchronous Module Definition) is an older module format
that is less common in modern JavaScript development, especially
with the widespread use of ES modules and CommonJS in Node.js.
AMD introduces unnecessary complexity and is often considered outdated.
This rule enforces the use of more modern module systems to improve
maintainability and consistency across the codebase.

### Examples

Examples of **incorrect** code for this rule:

```javascript
require([a, b], function () {});
```

Examples of **correct** code for this rule:

```javascript
require("../name");
require(`../name`);
```

## How to use

## References
