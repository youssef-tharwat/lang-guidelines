
### What it does

Requires that each `@param` tag has a description value.

### Why is this bad?

The description of a param should be documented.

### Examples

Examples of **incorrect** code for this rule:

```javascript
/** @param foo */
function quux(foo) {}
```

Examples of **correct** code for this rule:

```javascript
/** @param foo Foo. */
function quux(foo) {}
```

## How to use

## References
