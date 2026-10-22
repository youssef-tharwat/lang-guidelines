
### What it does

This rule ensures that promises returned by `expect.poll` and `expect.element` calls are handled properly.

### Why is this bad?

`expect.poll` and `expect.element` return promises. If not awaited or returned,
the test completes before the assertion resolves, meaning the test will pass
regardless of whether the assertion succeeds or fails.

### Examples

Examples of **incorrect** code for this rule:

```js
test("element exists", () => {
  asyncInjectElement();

  expect.poll(() => document.querySelector(".element")).toBeInTheDocument();
});
```

Examples of **correct** code for this rule:

```js
test("element exists", () => {
  asyncInjectElement();

  return expect.poll(() => document.querySelector(".element")).toBeInTheDocument();
});
test("element exists", async () => {
  asyncInjectElement();

  await expect.poll(() => document.querySelector(".element")).toBeInTheDocument();
});
```

## How to use

## References
