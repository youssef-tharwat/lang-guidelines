
### What it does

Requires that each `@param` tag has a type value (within curly brackets).

### Why is this bad?

The type of a parameter should be documented.

### Examples

Examples of **incorrect** code for this rule:

```javascript
/** @param foo */
function quux(foo) {}
```

Examples of **correct** code for this rule:

```javascript
/** @param {SomeType} foo */
function quux(foo) {}
```

## How to use

## References
