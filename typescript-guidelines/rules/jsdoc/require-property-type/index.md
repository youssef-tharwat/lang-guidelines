
### What it does

Requires that each `@property` tag has a type value (within curly brackets).

### Why is this bad?

The type of a property should be documented.

### Examples

Examples of **incorrect** code for this rule:

```javascript
/**
 * @typedef {SomeType} SomeTypedef
 * @property foo
 */
```

Examples of **correct** code for this rule:

```javascript
/**
 * @typedef {SomeType} SomeTypedef
 * @property {number} foo
 */
```

## How to use

## References
