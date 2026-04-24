
### What it does

Requires that all `@param` tags have names.

### Why is this bad?

The name of a param should be documented.

### Examples

Examples of **incorrect** code for this rule:

```javascript
/** @param {SomeType} */
function quux(foo) {}
```

Examples of **correct** code for this rule:

```javascript
/** @param {SomeType} foo */
function quux(foo) {}
```

## How to use

## References
