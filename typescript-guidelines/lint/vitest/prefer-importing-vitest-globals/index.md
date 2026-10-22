
### What it does

Enforces explicit imports from 'vitest' instead of using vitest globals.

### Why is this bad?

Using vitest globals without importing them relies on implicit global configuration
(`globals: true` in vitest config). Explicit imports make dependencies clear,
improve IDE support, and ensure compatibility across different setups.

### Examples

Examples of **incorrect** code for this rule:

```js
describe("suite", () => {
  it("test", () => {
    expect(true).toBe(true);
  });
});
```

Examples of **correct** code for this rule:

```js
import { describe, it, expect } from "vitest";

describe("suite", () => {
  it("test", () => {
    expect(true).toBe(true);
  });
});
```

## How to use

## References
