# Vitest Rules (TypeScript & JavaScript)

23 rules that apply when the project uses **vitest**.
Load this file only if the project's manifest imports or depends on
`vitest`.

---

### vitest/consistent-each-for
This rule ensure consistency on which method used to create parameterized test.
❌ 
```
// { test: 'for' }
test.each([[1, 1, 2]])("test", (a, b, expected) => {
  expect(a + b).toBe(expected);
});
// { describe: 'for' }
describe.each([[1], [2]])("suite %s", (n) => {
…
```
✅ 
```
// { test: 'for' }
test.for([[1, 1, 2]])("test", ([a, b, expected]) => {
  expect(a + b).toBe(expected);
});
// { describe: 'for' }
describe.for([[1], [2]])("suite %s", ([n]) => {
…
```

### vitest/consistent-test-filename
This rule triggers an error when a file is considered a test file, but its name does not match an expected filename format.

### vitest/consistent-vitest-vi
This rule triggers an error when an unexpected vitest accessor is used.
❌ 
```
vitest.mock("./src/calculator.ts", { spy: true });
vi.stubEnv("NODE_ENV", "production");
```
✅ 
```
vi.mock("./src/calculator.ts", { spy: true });
vi.stubEnv("NODE_ENV", "production");
```

### vitest/hoisted-apis-on-top
Enforce hoisted APIs to be on top of the file.
❌ 
```
if (condition) {
  vi.mock("some-module", () => {});
}
```
✅ 
```
if (condition) {
  vi.doMock("some-module", () => {});
}
```

### vitest/no-conditional-tests
The rule disallows the use of conditional statements within test cases to ensure that tests are deterministic and clearly readable.
❌ 
```
describe("my tests", () => {
  if (true) {
    it("is awesome", () => {
      doTheThing();
    });
  }
…
```
✅ 
```
describe("my tests", () => {
  it("is awesome", () => {
    doTheThing();
  });
});
```

### vitest/no-import-node-test
This rule warns when `node:test` is imported (usually accidentally).
❌ 
```
import { test } from "node:test";
import { expect } from "vitest";
test("foo", () => {
  expect(1).toBe(1);
});
```
✅ 
```
import { test, expect } from "vitest";
test("foo", () => {
  expect(1).toBe(1);
});
```

### vitest/no-importing-vitest-globals
The rule disallows importing any vitest global functions.
❌ 
```
import { test, expect } from "vitest";
test("foo", () => {
  expect(1).toBe(1);
});
```
✅ 
```
test("foo", () => {
  expect(1).toBe(1);
});
```

### vitest/prefer-called-exactly-once-with
It checks when a target is expected with `toHaveBeenCalledOnce` and `toHaveBeenCalledWith` instead of `toHaveBeenCalledExactlyOnceWith`.
❌ 
```
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toHaveBeenCalledOnce();
  expect(mock).toHaveBeenCalledWith("foo");
});
```
✅ 
```
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toHaveBeenCalledExactlyOnceWith("foo");
});
```

### vitest/prefer-called-once
Substitute `toBeCalledTimes(1)` and `toHaveBeenCalledTimes(1)` with `toBeCalledOnce()` and `toHaveBeenCalledOnce()` respectively.
❌ 
```
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toBeCalledTimes(1);
  expect(mock).toHaveBeenCalledTimes(1);
});
```
✅ 
```
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toBeCalledOnce();
  expect(mock).toHaveBeenCalledOnce();
});
```

### vitest/prefer-called-times
This rule aims to enforce the use of `toBeCalledTimes(1)` or `toHaveBeenCalledTimes(1)` over `toBeCalledOnce()` or `toHaveBeenCalledOnce()`.
❌ 
```
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toBeCalledOnce();
  expect(mock).toHaveBeenCalledOnce();
});
```
✅ 
```
test("foo", () => {
  const mock = vi.fn();
  mock("foo");
  expect(mock).toBeCalledTimes(1);
  expect(mock).toHaveBeenCalledTimes(1);
});
```

### vitest/prefer-describe-function-title
When testing a specific function, this rule aims to enforce passing a named function to `describe()` instead of an equivalent hardcoded string.
❌ 
```
// myFunction.test.js
import { myFunction } from "./myFunction";
describe("myFunction", () => {
  // ...
});
```
✅ 
```
// myFunction.test.js
import { myFunction } from "./myFunction";
describe(myFunction, () => {
  // ...
});
```

### vitest/prefer-expect-type-of
Enforce using `expectTypeOf` instead of `expect(typeof ...)`
❌ 
```
test('type checking', () => {
  expect(typeof 'hello').toBe('string')
  expect(typeof 42).toBe('number')
  expect(typeof true).toBe('boolean')
  expect(typeof {}).toBe('object')
  expect(typeof () => {}).toBe('function')
…
```
✅ 
```
test("type checking", () => {
  expectTypeOf("hello").toBeString();
  expectTypeOf(42).toBeNumber();
  expectTypeOf(true).toBeBoolean();
  expectTypeOf({}).toBeObject();
  expectTypeOf(() => {}).toBeFunction();
…
```

### vitest/prefer-import-in-mock
This rule enforces using a dynamic `import()` in `vi.mock()` or `vi.doMock()`, which improves type information and IntelliSense for the mocked module.
❌ 
```
vi.mock("./path/to/module");
vi.doMock("./path/to/module");
```
✅ 
```
vi.mock(import("./path/to/module"));
vi.doMock(import("./path/to/module"));
```

### vitest/prefer-importing-vitest-globals
Enforce explicit imports from 'vitest' instead of using vitest globals.
❌ 
```
describe("suite", () => {
  it("test", () => {
    expect(true).toBe(true);
  });
});
```
✅ 
```
import { describe, it, expect } from "vitest";
describe("suite", () => {
  it("test", () => {
    expect(true).toBe(true);
  });
});
```

### vitest/prefer-strict-boolean-matchers
Enforce using `toBe(true)` and `toBe(false)` over matchers that coerce types to boolean.
❌ 
```
expect(foo).toBeTruthy();
expectTypeOf(foo).toBeTruthy();
expect(foo).toBeFalsy();
expectTypeOf(foo).toBeFalsy();
```
✅ 
```
expect(foo).toBe(true);
expectTypeOf(foo).toBe(true);
expect(foo).toBe(false);
expectTypeOf(foo).toBe(false);
```

### vitest/prefer-to-be-falsy
This rule warns when `toBe(false)` is used with `expect` or `expectTypeOf`.
❌ 
```
expect(foo).toBe(false);
expectTypeOf(foo).toBe(false);
```
✅ 
```
expect(foo).toBeFalsy();
expectTypeOf(foo).toBeFalsy();
```

### vitest/prefer-to-be-object
This rule enforces using `toBeObject()` to check if a value is of type `Object`.
❌ 
```
expectTypeOf({}).toBeInstanceOf(Object);
expectTypeOf({} instanceof Object).toBeTruthy();
```
✅ 
```
expectTypeOf({}).toBeObject();
expectTypeOf({}).toBeObject();
```

### vitest/prefer-to-be-truthy
This rule warns when `toBe(true)` is used with `expect` or `expectTypeOf`.
❌ 
```
expect(foo).toBe(true);
expectTypeOf(foo).toBe(true);
```
✅ 
```
expect(foo).toBeTruthy();
expectTypeOf(foo).toBeTruthy();
```

### vitest/require-awaited-expect-poll
This rule ensures that promises returned by `expect.poll` and `expect.element` calls are handled properly.
❌ 
```
test("element exists", () => {
  asyncInjectElement();
  expect.poll(() => document.querySelector(".element")).toBeInTheDocument();
});
```
✅ 
```
test("element exists", () => {
  asyncInjectElement();
  return expect.poll(() => document.querySelector(".element")).toBeInTheDocument();
});
test("element exists", async () => {
  asyncInjectElement();
…
```

### vitest/require-local-test-context-for-concurrent-snapshots
The rule is intended to ensure that concurrent snapshot tests are executed within a properly configured local test context.
❌ 
```
test.concurrent("myLogic", () => {
  expect(true).toMatchSnapshot();
});
describe.concurrent("something", () => {
  test("myLogic", () => {
    expect(true).toMatchInlineSnapshot();
…
```
✅ 
```
test.concurrent("myLogic", ({ expect }) => {
  expect(true).toMatchSnapshot();
});
test.concurrent("myLogic", (context) => {
  context.expect(true).toMatchSnapshot();
});
```

### vitest/require-mock-type-parameters
Enforce the use of type parameters on vi.fn(), and optionally on vi.importActual() and vi.importMock().
❌ 
```
import { vi } from "vitest";
test("foo", () => {
  const myMockedFn = vi.fn();
});
```
✅ 
```
import { vi } from 'vitest'
 test('foo', () => {
   const myMockedFnOne = vi.fn<(arg1: string, arg2: boolean) => number>()
   const myMockedFnTwo = vi.fn<() => void>()
   const myMockedFnThree = vi.fn<any>()
 })
```

### vitest/require-test-timeout
Require every test to have a timeout specified, either as a numeric third argument, a `{ timeout }` option, or via `vi.setConfig({ testTimeout: ...
❌ 
```
it("slow test", async () => {
  await doSomethingSlow();
});
```
✅ 
```
// good (numeric timeout)
test("slow test", async () => {
  await doSomethingSlow();
}, 1000);
// good (options object)
test("slow test", { timeout: 1000 }, async () => {
…
```

### vitest/warn-todo
This rule triggers warnings when `.todo` is used in `describe`, `it`, or `test` functions.
❌ 
```
describe.todo("foo", () => {});
it.todo("foo", () => {});
test.todo("foo", () => {});
```
✅ 
```
describe([])("foo", () => {});
it([])("foo", () => {});
test([])("foo", () => {});
```
