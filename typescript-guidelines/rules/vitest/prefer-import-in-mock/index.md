
### What it does

This rule enforces using a dynamic `import()` in `vi.mock()` or `vi.doMock()`, which improves type information and IntelliSense for the mocked module.

### Why is this bad?

A lack of type information and IntelliSense increase the risk of mismatches between the real module and it's mock.

### Examples

Examples of **incorrect** code for this rule:

```js
vi.mock("./path/to/module");
vi.doMock("./path/to/module");
```

Examples of **correct** code for this rule:

```js
vi.mock(import("./path/to/module"));
vi.doMock(import("./path/to/module"));
```

## Configuration

This rule accepts a configuration object with the following properties:

### fixable

type: `boolean`

default: `true`

Whether the rule should generate fixes or not.

## How to use

## References
