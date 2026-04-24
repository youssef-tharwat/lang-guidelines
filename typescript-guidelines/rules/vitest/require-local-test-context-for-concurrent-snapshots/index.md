
### What it does

The rule is intended to ensure that concurrent snapshot tests are executed
within a properly configured local test context.

### Why is this bad?

Running snapshot tests concurrently without a proper context can lead to
unreliable or inconsistent snapshots. Ensuring that concurrent tests are
correctly configured with the appropriate context helps maintain accurate
and stable snapshots, avoiding potential conflicts or failures.

### Examples

Examples of **incorrect** code for this rule:

```javascript
test.concurrent("myLogic", () => {
  expect(true).toMatchSnapshot();
});

describe.concurrent("something", () => {
  test("myLogic", () => {
    expect(true).toMatchInlineSnapshot();
  });
});
```

Examples of **correct** code for this rule:

```javascript
test.concurrent("myLogic", ({ expect }) => {
  expect(true).toMatchSnapshot();
});

test.concurrent("myLogic", (context) => {
  context.expect(true).toMatchSnapshot();
});
```

## How to use

## References
