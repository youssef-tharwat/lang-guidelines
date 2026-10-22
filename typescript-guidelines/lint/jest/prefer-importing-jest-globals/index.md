
### What it does

Prefer importing Jest globals (`describe`, `test`, `expect`, etc.) from
`@jest/globals` rather than relying on ambient globals.

### Why is this bad?

Using global Jest functions without explicit imports makes dependencies
implicit and can cause issues with type checking, editor tooling, and
when migrating between test runners.

### Examples

Examples of **incorrect** code for this rule:

```javascript
describe("suite", () => {
  test("foo");
  expect(true).toBeDefined();
});
```

Examples of **correct** code for this rule:

```javascript
import { describe, expect, test } from "@jest/globals";
describe("suite", () => {
  test("foo");
  expect(true).toBeDefined();
});
```

## Configuration

This rule accepts a configuration object with the following properties:

### types

type: `array`

default: `["hook", "describe", "test", "expect", "jest", "unknown"]`

Jest function types to enforce importing for.

#### types\[n]

type: `"hook" | "describe" | "test" | "expect" | "jest" | "unknown"`

## How to use

## References
