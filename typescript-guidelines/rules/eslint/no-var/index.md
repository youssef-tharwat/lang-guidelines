
### What it does

ECMAScript 2015 allows programmers to create variables with block scope
instead of function scope using the `let` and `const` keywords. Block
scope is common in many other programming languages and helps
programmers avoid mistakes.

### Why is this bad?

Using `var` in an ES2015 environment triggers this error

### Examples

Examples of **incorrect** code for this rule:

```javascript
var x = "y";
var CONFIG = {};
```

Examples of **correct** code for this rule:

```javascript
let x = "y";
const CONFIG = {};
```

## How to use

## References
