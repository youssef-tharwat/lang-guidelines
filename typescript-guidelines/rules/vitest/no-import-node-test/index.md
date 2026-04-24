
### What it does

This rule warns when `node:test` is imported (usually accidentally).
With `--fix`, it will replace the import with `vitest`.

### Why is this bad?

Using `node:test` instead of `vitest` can lead to inconsistent test results
and missing features. `vitest` should be used for all testing to ensure
compatibility and access to its full functionality.

### Examples

Examples of **incorrect** code for this rule:

```javascript
import { test } from "node:test";
import { expect } from "vitest";

test("foo", () => {
  expect(1).toBe(1);
});
```

Examples of **correct** code for this rule:

```javascript
import { test, expect } from "vitest";

test("foo", () => {
  expect(1).toBe(1);
});
```

## How to use

## References
