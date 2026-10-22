
### What it does

Disallow useless fallback when spreading in object literals.

### Why is this bad?

Spreading [falsy values](https://developer.mozilla.org/en-US/docs/Glossary/Falsy) in object literals won't add any unexpected properties, so it's unnecessary to add an empty object as fallback.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const object = { ...(foo || {}) };
```

Examples of **correct** code for this rule:

```javascript
const object = { ...foo };
const object = { ...(foo || { not: "empty" }) };
```

## How to use

## References
