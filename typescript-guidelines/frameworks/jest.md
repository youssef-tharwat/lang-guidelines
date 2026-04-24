# Jest Rules (TypeScript & JavaScript)

59 rules that apply when the project uses **jest**.
Load this file only if the project's manifest imports or depends on
`jest`.

---

### jest/consistent-test-it
Jest allows you to choose how you want to define your tests, using the `it` or the `test` keywords, with multiple permutations for each: * **it:** `it`, `xit`, `fit`, `it.only`, `it.skip`.

### jest/expect-expect
This rule triggers when there is no call made to `expect` in a test, ensure that there is at least one `expect` call made in a test.
❌ 
```
it("should be a test", () => {
  console.log("no assertion");
});
test("should assert something", () => {});
```

### jest/max-expects
This rule enforces a maximum number of `expect()` calls in a single test.
❌ 
```
test("should not pass", () => {
  expect(true).toBeDefined();
  expect(true).toBeDefined();
  expect(true).toBeDefined();
  expect(true).toBeDefined();
  expect(true).toBeDefined();
…
```

### jest/max-nested-describe
This rule enforces a maximum depth to nested `describe()` calls.
❌ 
```
describe("foo", () => {
  describe("bar", () => {
    describe("baz", () => {
      describe("qux", () => {
        describe("quxx", () => {
          describe("too many", () => {
…
```
✅ 
```
describe("foo", () => {
  describe("bar", () => {
    it("should get something", () => {
      expect(getSomething()).toBe("Something");
    });
  });
…
```

### jest/no-alias-methods
This rule ensures that only the canonical name as used in the Jest documentation is used in the code.
❌ 
```
expect(a).toBeCalled();
expect(a).toBeCalledTimes();
expect(a).toBeCalledWith();
expect(a).lastCalledWith();
expect(a).nthCalledWith();
expect(a).toReturn();
…
```
✅ 
```
expect(a).toHaveBeenCalled();
expect(a).toHaveBeenCalledTimes();
expect(a).toHaveBeenCalledWith();
expect(a).toHaveBeenLastCalledWith();
expect(a).toHaveBeenNthCalledWith();
expect(a).toHaveReturned();
…
```

### jest/no-commented-out-tests
This rule raises a warning about commented out tests.
❌ 
```
// describe('foo', () => {});
// it('foo', () => {});
// test('foo', () => {});
// describe.skip('foo', () => {});
// it.skip('foo', () => {});
// test.skip('foo', () => {});
```

### jest/no-conditional-expect
This rule prevents the use of expect in conditional blocks, such as ifs & catch(s).
❌ 
```
it("foo", () => {
  doTest && expect(1).toBe(2);
});
it("bar", () => {
  if (!skipTest) {
    expect(1).toEqual(2);
…
```
✅ 
```
it("foo", () => {
  expect(!value).toBe(false);
});
function getValue() {
  if (process.env.FAIL) {
    return 1;
…
```

### jest/no-conditional-in-test
Do not use conditional statements in tests.
❌ 
```
it("foo", () => {
  if (true) {
    doTheThing();
  }
});
it("bar", () => {
…
```
✅ 
```
describe("my tests", () => {
  if (true) {
    it("foo", () => {
      doTheThing();
    });
  }
…
```

### jest/no-confusing-set-timeout
Do not use confusing usages of `jest.setTimeout`.

### jest/no-deprecated-functions
Over the years Jest has accrued some debt in the form of functions that have either been renamed for clarity, or replaced with more powerful APIs.
❌ 
```
jest.resetModuleRegistry; // since Jest 15
jest.addMatchers; // since Jest 17
```

### jest/no-disabled-tests
This rule raises a warning about disabled tests.

### jest/no-done-callback
This rule checks the function parameter of hooks & tests for use of the done argument, suggesting you return a promise instead.
❌ 
```
beforeEach((done) => {
  // ...
});
test("myFunction()", (done) => {
  // ...
});
…
```

### jest/no-duplicate-hooks
Do not use duplicate hooks in describe blocks.
❌ 
```
describe("foo", () => {
  beforeEach(() => {
    // some setup
  });
  beforeEach(() => {
    // some setup
…
```
✅ 
```
describe("foo", () => {
  beforeEach(() => {
    // some setup
  });
  test("foo_test", () => {
    // some test
…
```

### jest/no-export
Prevent using exports if a file has one or more tests in it.
❌ 
```
export function myHelper() {}
describe("a test", () => {
  expect(1).toBe(1);
});
```

### jest/no-focused-tests
This rule reminds you to remove `.only` from your tests by raising a warning whenever you are using the exclusivity feature.
❌ 
```
describe.only("foo", () => {});
it.only("foo", () => {});
describe["only"]("bar", () => {});
it["only"]("bar", () => {});
test.only("foo", () => {});
test["only"]("bar", () => {});
…
```

### jest/no-hooks
Do not use Jest setup and teardown hooks, such as `beforeAll`.
❌ 
```
function setupFoo(options) {
  /* ... */
}
function setupBar(options) {
  /* ... */
}
…
```

### jest/no-identical-title
This rule looks at the title of every test and test suite.
❌ 
```
describe("baz", () => {
  //...
});
describe("baz", () => {
  // Has the same title as a previous test suite
  // ...
…
```

### jest/no-interpolation-in-snapshots
Prevent the use of string interpolations in snapshots.
❌ 
```
expect(something).toMatchInlineSnapshot(
  `Object {
    property: ${interpolated}
  }`,
);
expect(something).toMatchInlineSnapshot(
…
```

### jest/no-jasmine-globals
This rule reports on any usage of Jasmine globals, which is not ported to Jest, and suggests alternatives from Jest's own API.
❌ 
```
jasmine.DEFAULT_TIMEOUT_INTERVAL = 5000;
test("my test", () => {
  pending();
});
test("my test", () => {
  jasmine.createSpy();
…
```
✅ 
```
jest.setTimeout(5000);
test("my test", () => {
  // Use test.skip() instead of pending()
});
test.skip("my test", () => {
  // Skipped test
…
```

### jest/no-large-snapshots
Do not use large snapshots.
❌ 
```
exports[`a large snapshot 1`] = `
line 1
line 2
line 3
line 4
line 5
…
```

### jest/no-mocks-import
This rule reports imports from a path containing a **mocks** component.
❌ 
```
import thing from "./__mocks__/index";
require("./__mocks__/index");
```
✅ 
```
import thing from "thing";
require("thing");
```

### jest/no-restricted-jest-methods
Restrict the use of specific `jest` and `vi` methods.
❌ 
```
jest.useFakeTimers();
it("calls the callback after 1 second via advanceTimersByTime", () => {
  // ...
  jest.advanceTimersByTime(1000);
  // ...
});
…
```

### jest/no-restricted-matchers
Do not use specific matchers & modifiers from being used, and can suggest alternatives.
❌ 
```
it("is false", () => {
  // if this has a modifier (i.e. `not.toBeFalsy`), it would be considered fine
  expect(a).toBeFalsy();
});
it("resolves", async () => {
  // all uses of this modifier are disallowed, regardless of matcher
…
```

### jest/no-standalone-expect
Prevent `expect` statements outside of a `test` or `it` block.
❌ 
```
describe("a test", () => {
  expect(1).toBe(1);
});
```

### jest/no-test-prefixes
Require using `.only` and `.skip` over `f` and `x`.
❌ 
```
fit("foo"); // invalid
fdescribe("foo"); // invalid
xit("foo"); // invalid
xtest("foo"); // invalid
xdescribe("foo"); // invalid
```

### jest/no-test-return-statement
Do not use explicitly returning from tests.
❌ 
```
test("one", () => {
  return expect(1).toBe(1);
});
```
✅ 
```
test("one", () => {
  expect(1).toBe(1);
});
```

### jest/no-unneeded-async-expect-function
Do not use unnecessary async function wrapper for expected promises.
❌ 
```
await expect(async () => {
  await doSomethingAsync();
}).rejects.toThrow();
await expect(async () => await doSomethingAsync()).rejects.toThrow();
```
✅ `await expect(doSomethingAsync()).rejects.toThrow();`

### jest/no-untyped-mock-factory
This rule triggers a warning if `mock()` or `doMock()` is used without a generic type parameter or return type.
❌ 
```
jest.mock("../moduleName", () => {
  return jest.fn(() => 42);
});
jest.mock("./module", () => ({
  ...jest.requireActual("./module"),
  foo: jest.fn(),
…
```
✅ 
```
// Uses typeof import()
jest.mock<typeof import("../moduleName")>("../moduleName", () => {
  return jest.fn(() => 42);
});
jest.mock<typeof import("./module")>("./module", () => ({
  ...jest.requireActual("./module"),
…
```

### jest/padding-around-after-all-blocks
This rule enforces a line of padding before and after 1 or more `afterAll` statements.
❌ 
```
const thing = 123;
afterAll(() => {});
```
✅ 
```
const thing = 123;
afterAll(() => {});
```

### jest/padding-around-test-blocks
This rule enforces a line of padding before and after 1 or more `test`/`it` statements.
❌ 
```
const thing = 123;
test("foo", () => {});
test("bar", () => {});
```
✅ 
```
const thing = 123;
test("foo", () => {});
test("bar", () => {});
```

### jest/prefer-called-with
Suggest using `toBeCalledWith()` or `toHaveBeenCalledWith()`
❌ 
```
expect(someFunction).toBeCalled();
expect(someFunction).toHaveBeenCalled();
```
✅ 
```
expect(noArgsFunction).toBeCalledWith();
expect(roughArgsFunction).toBeCalledWith(expect.anything(), expect.any(Date));
expect(anyArgsFunction).toBeCalledTimes(1);
expect(uncalledFunction).not.toBeCalled();
```

### jest/prefer-comparison-matcher
This rule checks for comparisons in tests that could be replaced with one of the following built-in comparison matchers: * `toBeGreaterThan` * `toBeGreaterThanOrEqual` * `toBeLessThan` * `toBeLessThanOrEqual`
❌ 
```
expect(x > 5).toBe(true);
expect(x < 7).not.toEqual(true);
expect(x <= y).toStrictEqual(true);
```
✅ 
```
expect(x).toBeGreaterThan(5);
expect(x).not.toBeLessThanOrEqual(7);
expect(x).toBeLessThanOrEqual(y);
// special case - see below
expect(x < "Carl").toBe(true);
```

### jest/prefer-each
This rule enforces using `each` rather than manual loops.
❌ 
```
for (const item of items) {
  describe(item, () => {
    expect(item).toBe("foo");
  });
}
```
✅ 
```
describe.each(items)("item", (item) => {
  expect(item).toBe("foo");
});
```

### jest/prefer-ending-with-an-expect
Enforce that test blocks end with an assertion (`expect` or a configured assertion function).
❌ 
```
it("lets me change the selected option", () => {
  const container = render(MySelect, {
    props: { options: [1, 2, 3], selected: 1 },
  });
  expect(container).toBeDefined();
  expect(container.toHTML()).toContain('<option value="1" selected>');
…
```
✅ 
```
it("lets me change the selected option", () => {
  const container = render(MySelect, {
    props: { options: [1, 2, 3], selected: 1 },
  });
  expect(container).toBeDefined();
  expect(container.toHTML()).toContain('<option value="1" selected>');
…
```

### jest/prefer-equality-matcher
Jest has built-in matchers for expecting equality, which allow for more readable tests and error messages if an expectation fails.
❌ 
```
expect(x === 5).toBe(true);
expect(name === "Carl").not.toEqual(true);
expect(myObj !== thatObj).toStrictEqual(true);
```
✅ 
```
expect(x).toBe(5);
expect(name).not.toEqual("Carl");
expect(myObj).toStrictEqual(thatObj);
```

### jest/prefer-expect-resolves
Prefer `await expect(...).resolves` over `expect(await ...)` when testing promises.
❌ 
```
it("passes", async () => {
  expect(await someValue()).toBe(true);
});
it("is true", async () => {
  const myPromise = Promise.resolve(true);
  expect(await myPromise).toBe(true);
…
```
✅ 
```
it("passes", async () => {
  await expect(someValue()).resolves.toBe(true);
});
it("is true", async () => {
  const myPromise = Promise.resolve(true);
  await expect(myPromise).resolves.toBe(true);
…
```

### jest/prefer-hooks-in-order
Ensures that hooks are in the order that they are called in.
❌ 
```
describe("foo", () => {
  beforeEach(() => {
    seedMyDatabase();
  });
  beforeAll(() => {
    createMyDatabase();
…
```
✅ 
```
describe("foo", () => {
  beforeAll(() => {
    createMyDatabase();
  });
  beforeEach(() => {
    seedMyDatabase();
…
```

### jest/prefer-hooks-on-top
While hooks can be setup anywhere in a test file, they are always called in a specific order, which means it can be confusing if they're intermixed with test cases.
❌ 
```
describe("foo", () => {
  beforeEach(() => {
    seedMyDatabase();
  });
  it("accepts this input", () => {
    // ...
…
```
✅ 
```
describe("foo", () => {
  beforeAll(() => {
    createMyDatabase();
  });
  beforeEach(() => {
    seedMyDatabase();
…
```

### jest/prefer-importing-jest-globals
Prefer importing Jest globals (`describe`, `test`, `expect`, etc.) from `@jest/globals` rather than relying on ambient globals.
❌ 
```
describe("suite", () => {
  test("foo");
  expect(true).toBeDefined();
});
```
✅ 
```
import { describe, expect, test } from "@jest/globals";
describe("suite", () => {
  test("foo");
  expect(true).toBeDefined();
});
```

### jest/prefer-jest-mocked
When working with mocks of functions using Jest, it's recommended to use the `jest.mocked()` helper function to properly type the mocked functions.
❌ 
```
(foo as jest.Mock).mockReturnValue(1);
const mock = (foo as jest.Mock).mockReturnValue(1);
(foo as unknown as jest.Mock).mockReturnValue(1);
(Obj.foo as jest.Mock).mockReturnValue(1);
([].foo as jest.Mock).mockReturnValue(1);
```
✅ 
```
jest.mocked(foo).mockReturnValue(1);
const mock = jest.mocked(foo).mockReturnValue(1);
jest.mocked(Obj.foo).mockReturnValue(1);
jest.mocked([].foo).mockReturnValue(1);
```

### jest/prefer-lowercase-title
Enforce `it`, `test`, `describe`, and `bench` to have descriptions that begin with a lowercase letter.
❌ 
```
it("Adds 1 + 2 to equal 3", () => {
  expect(sum(1, 2)).toBe(3);
});
```
✅ 
```
it("adds 1 + 2 to equal 3", () => {
  expect(sum(1, 2)).toBe(3);
});
```

### jest/prefer-mock-promise-shorthand
When working with mocks of functions that return promises, Jest provides some API sugar functions to reduce the amount of boilerplate you have to write.
❌ 
```
jest.fn().mockImplementation(() => Promise.resolve(123));
jest.spyOn(fs.promises, "readFile").mockReturnValue(Promise.reject(new Error("oh noes!")));
myFunction
  .mockReturnValueOnce(Promise.resolve(42))
  .mockImplementationOnce(() => Promise.resolve(42))
  .mockReturnValue(Promise.reject(new Error("too many calls!")));
```
✅ 
```
jest.fn().mockResolvedValue(123);
jest.spyOn(fs.promises, "readFile").mockRejectedValue(new Error("oh noes!"));
myFunction
  .mockResolvedValueOnce(42)
  .mockResolvedValueOnce(42)
  .mockRejectedValue(new Error("too many calls!"));
```

### jest/prefer-mock-return-shorthand
When working with mocks of functions that return simple values, Jest provides some API sugar functions to reduce the amount of boilerplate you have to write.
❌ 
```
jest.fn().mockImplementation(() => "hello world");
jest
  .spyOn(fs.promises, "readFile")
  .mockImplementationOnce(() => Promise.reject(new Error("oh noes!")));
myFunction
  .mockImplementationOnce(() => 42)
…
```
✅ 
```
jest.fn().mockResolvedValue(123);
jest.spyOn(fs.promises, "readFile").mockReturnValue(Promise.reject(new Error("oh noes!")));
jest.spyOn(fs.promises, "readFile").mockRejectedValue(new Error("oh noes!"));
jest.spyOn(fs, "readFileSync").mockImplementationOnce(() => {
  throw new Error("oh noes!");
});
…
```

### jest/prefer-snapshot-hint
Enforce including a hint string with snapshot matchers (toMatchSnapshot and toThrowErrorMatchingSnapshot).
❌ 
```
const snapshotOutput = ({ stdout, stderr }) => {
  expect(stdout).toMatchSnapshot();
  expect(stderr).toMatchSnapshot();
};
describe("cli", () => {
  describe("--version flag", () => {
…
```
✅ 
```
const snapshotOutput = ({ stdout, stderr }, hints) => {
  expect(stdout).toMatchSnapshot({}, `stdout: ${hints.stdout}`);
  expect(stderr).toMatchSnapshot({}, `stderr: ${hints.stderr}`);
};
describe("cli", () => {
  describe("--version flag", () => {
…
```

### jest/prefer-spy-on
When mocking a function by overwriting a property you have to manually restore the original implementation when cleaning up.
❌ 
```
Date.now = jest.fn();
Date.now = jest.fn(() => 10);
```
✅ 
```
jest.spyOn(Date, "now");
jest.spyOn(Date, "now").mockImplementation(() => 10);
```

### jest/prefer-strict-equal
This rule triggers a warning if `toEqual()` is used to assert equality.
❌ `expect({ a: "a", b: undefined }).toEqual({ a: "a" });`
✅ `expect({ a: "a", b: undefined }).toStrictEqual({ a: "a" });`

### jest/prefer-to-be
Recommends using `toBe` matcher for primitive literals and specific matchers for `null`, `undefined`, and `NaN`.
❌ 
```
expect(value).not.toEqual(5);
expect(getMessage()).toStrictEqual("hello world");
expect(loadMessage()).resolves.toEqual("hello world");
```
✅ 
```
expect(value).not.toBe(5);
expect(getMessage()).toBe("hello world");
expect(loadMessage()).resolves.toBe("hello world");
expect(didError).not.toBe(true);
expect(catchError()).toStrictEqual({ message: "oh noes!" });
```

### jest/prefer-to-contain
In order to have a better failure message, `toContain()` should be used upon asserting expectations on an array containing an object.
❌ 
```
expect(a.includes(b)).toBe(true);
expect(a.includes(b)).not.toBe(true);
expect(a.includes(b)).toBe(false);
expect(a.includes(b)).toEqual(true);
expect(a.includes(b)).toStrictEqual(true);
```
✅ 
```
expect(a).toContain(b);
expect(a).not.toContain(b);
```

### jest/prefer-to-have-been-called
Suggests using `toHaveBeenCalled()` or `not.toHaveBeenCalled()` over `toHaveBeenCalledTimes(0)` or `toBeCalledTimes(0)`.
❌ 
```
expect(mock).toHaveBeenCalledTimes(0);
expect(mock).toBeCalledTimes(0);
expect(mock).not.toHaveBeenCalledTimes(0);
```
✅ 
```
expect(mock).not.toHaveBeenCalled();
expect(mock).toHaveBeenCalled();
expect(mock).toHaveBeenCalledTimes(1);
```

### jest/prefer-to-have-been-called-times
In order to have a better failure message, `toHaveBeenCalledTimes` should be used instead of directly checking the length of `mock.calls`.
❌ 
```
expect(someFunction.mock.calls).toHaveLength(1);
expect(someFunction.mock.calls).toHaveLength(0);
expect(someFunction.mock.calls).not.toHaveLength(1);
```
✅ 
```
expect(someFunction).toHaveBeenCalledTimes(1);
expect(someFunction).toHaveBeenCalledTimes(0);
expect(someFunction).not.toHaveBeenCalledTimes(0);
expect(uncalledFunction).not.toBeCalled();
expect(method.mock.calls[0][0]).toStrictEqual(value);
```

### jest/prefer-to-have-length
In order to have a better failure message, `toHaveLength()` should be used upon asserting expectations on objects length property.
❌ 
```
expect(files["length"]).toBe(1);
expect(files["length"]).toBe(1);
expect(files["length"])["not"].toBe(1);
```
✅ `expect(files).toHaveLength(1);`

### jest/prefer-todo
When test cases are empty then it is better to mark them as `test.todo` as it will be highlighted in the summary output.
❌ 
```
test("i need to write this test"); // invalid
test("i need to write this test", () => {}); // invalid
test.skip("i need to write this test", () => {}); // invalid
```
✅ `test.todo("i need to write this test");`

### jest/require-hook
This rule flags any expression that is either at the toplevel of a test file or directly within the body of a `describe`, *except* for the following: * `import` statements * `const` variables * `let` *declarations*, and initializations to…
❌ 
```
import { database, isCity } from "../database";
import { Logger } from "../../../src/Logger";
import { loadCities } from "../api";
jest.mock("../api");
const initializeCityDatabase = () => {
  database.addCity("Vienna");
…
```
✅ 
```
import { database, isCity } from "../database";
import { Logger } from "../../../src/Logger";
import { loadCities } from "../api";
jest.mock("../api");
const initializeCityDatabase = () => {
  database.addCity("Vienna");
…
```

### jest/require-to-throw-message
This rule triggers a warning if `toThrow()` or `toThrowError()` is used without an error message.
❌ 
```
test("all the things", async () => {
  expect(() => a()).toThrow();
  expect(() => a()).toThrowError();
  await expect(a()).rejects.toThrow();
  await expect(a()).rejects.toThrowError();
});
```
✅ 
```
test("all the things", async () => {
  expect(() => a()).toThrow("a");
  expect(() => a()).toThrowError("a");
  await expect(a()).rejects.toThrow("a");
  await expect(a()).rejects.toThrowError("a");
});
```

### jest/require-top-level-describe
Require test cases and hooks to be inside a top-level `describe` block.
❌ 
```
// Above a describe block
test("my test", () => {});
describe("test suite", () => {
  it("test", () => {});
});
// Below a describe block
…
```
✅ 
```
// Above a describe block
// In a describe block
describe("test suite", () => {
  test("my test", () => {});
});
// In a nested describe block
…
```

### jest/valid-describe-callback
This rule validates that the second parameter of a `describe()` function is a callback function.
❌ 
```
// Async callback functions are not allowed
describe("myFunction()", async () => {
  // ...
});
// Callback function parameters are not allowed
describe("myFunction()", (done) => {
…
```

### jest/valid-expect
Ensure `expect()` is called correctly.
❌ 
```
expect();
expect("something");
expect(true).toBeDefined;
expect(Promise.resolve("Hi!")).resolves.toBe("Hi!");
```
✅ 
```
expect("something").toEqual("something");
expect(true).toBeDefined();
expect(Promise.resolve("Hi!")).resolves.toBe("Hi!");
```

### jest/valid-expect-in-promise
Ensures that `expect` calls inside promise chains (`.then()`, `.catch()`, `.finally()`) are properly awaited or returned from the test.
❌ 
```
test("promise test", async () => {
  something().then((value) => {
    expect(value).toBe("red");
  });
});
test("promises test", () => {
…
```
✅ 
```
test("promise test", async () => {
  await something().then((value) => {
    expect(value).toBe("red");
  });
});
test("promises test", () => {
…
```

### jest/valid-title
Ensure the titles of Jest and Vitest blocks are valid.
❌ 
```
describe("", () => {});
describe("foo", () => {
  it("", () => {});
});
it("", () => {});
test("", () => {});
…
```
✅ 
```
describe("foo", () => {});
it("bar", () => {});
test("baz", () => {});
```
