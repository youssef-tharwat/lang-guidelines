
### What it does

Prefer using `structuredClone` to create a deep clone.

### Why is this bad?

`structuredClone` is the modern way to create a deep clone of a value.

### Examples

Examples of **incorrect** code for this rule:

```js
const clone = JSON.parse(JSON.stringify(foo));

const clone = _.cloneDeep(foo);
```

Examples of **correct** code for this rule:

```js
const clone = structuredClone(foo);
```

## Configuration

This rule accepts a configuration object with the following properties:

### functions

type: `string[]`

default: `["cloneDeep", "utils.clone"]`

List of functions that are allowed to be used for deep cloning instead of structuredClone.

## How to use

## References
