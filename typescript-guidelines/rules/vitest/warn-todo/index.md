
### What it does

This rule triggers warnings when `.todo` is used in `describe`, `it`, or `test` functions.
It is recommended to use this with your CI pipeline to annotate PR diffs.

### Why is this bad?

The test that you push should be completed, any pending/"TODO" code should not be committed.

### Examples

Examples of **incorrect** code for this rule:

```js
describe.todo("foo", () => {});
it.todo("foo", () => {});
test.todo("foo", () => {});
```

Examples of **correct** code for this rule:

```js
describe([])("foo", () => {});
it([])("foo", () => {});
test([])("foo", () => {});
```

## How to use

## References
