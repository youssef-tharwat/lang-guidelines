
### What it does

Disallow the use of an object literal as a default value for a parameter.

### Why is this bad?

Default parameters should not be passed to a function through an object literal. The `foo = {a: false}` parameter works fine if only used with one option. As soon as additional options are added, you risk replacing the whole `foo = {a: false, b: true}` object when passing only one option: `{a: true}`. For this reason, object destructuring should be used instead.

### Examples

Examples of **incorrect** code for this rule:

```javascript
function foo(foo = { a: false }) {}
```

Examples of **correct** code for this rule:

```javascript
function foo({ a = false } = {}) {}
```

## How to use

## References
