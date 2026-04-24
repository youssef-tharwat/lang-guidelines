
### What it does

Requires that `@returns` tag has a type value (in curly brackets).

### Why is this bad?

A `@returns` tag should have a type value.

### Examples

Examples of **incorrect** code for this rule:

```javascript
/** @returns */
function quux(foo) {}
```

Examples of **correct** code for this rule:

```javascript
/** @returns {string} */
function quux(foo) {}
```

## How to use

## References
