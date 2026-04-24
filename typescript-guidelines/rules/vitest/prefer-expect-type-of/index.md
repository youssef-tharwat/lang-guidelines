
### What it does

Enforce using `expectTypeOf` instead of `expect(typeof ...)`

### Why is this bad?

Vitest provide a more expressive type-safe way to test type than using `expect(typeof ...)`

### Examples

Examples of **incorrect** code for this rule:

```js
test('type checking', () => {
  expect(typeof 'hello').toBe('string')
  expect(typeof 42).toBe('number')
  expect(typeof true).toBe('boolean')
  expect(typeof {}).toBe('object')
  expect(typeof () => {}).toBe('function')
  expect(typeof Symbol()).toBe('symbol')
  expect(typeof 123n).toBe('bigint')
  expect(typeof undefined).toBe('undefined')
})
```

Examples of **correct** code for this rule:

```js
test("type checking", () => {
  expectTypeOf("hello").toBeString();
  expectTypeOf(42).toBeNumber();
  expectTypeOf(true).toBeBoolean();
  expectTypeOf({}).toBeObject();
  expectTypeOf(() => {}).toBeFunction();
  expectTypeOf(Symbol()).toBeSymbol();
  expectTypeOf(123n).toBeBigInt();
  expectTypeOf(undefined).toBeUndefined();
});
```

## How to use

## References
