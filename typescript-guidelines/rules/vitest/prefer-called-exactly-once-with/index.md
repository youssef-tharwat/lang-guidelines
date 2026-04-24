
### What it does

It checks when a target is expected with `toHaveBeenCalledOnce` and `toHaveBeenCalledWith` instead of
`toHaveBeenCalledExactlyOnceWith`.

### Why is this bad?

The user must deduct from both expects that the spy function is called once and with a specific arguments.

### Examples

Examples of **incorrect** code for this rule:

```js
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toHaveBeenCalledOnce();
  expect(mock).toHaveBeenCalledWith("foo");
});
```

Examples of **correct** code for this rule:

```js
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toHaveBeenCalledExactlyOnceWith("foo");
});
```

## How to use

## References
