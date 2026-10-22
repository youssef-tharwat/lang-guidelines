# type-assertions

Avoid `as` casts and `!` non-null assertions; prefer runtime checks (`instanceof`, `if (y)`). When an assertion is truly safe, use `as` (never `<T>x`) with a comment explaining why, cast through `unknown` for a double assertion, and annotate object literals (`const foo: Foo = {...}`) instead of asserting them.

**Why:** Assertions silence the compiler without checking anything.

**Sources:** G:control-structures

---

## Control structures (G:control-structures)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#control-structures), CC BY 3.0.

### Control flow statements and blocks

Control flow statements (`if`, `else`, `for`, `do`, `while`, etc) always use braced blocks for the containing code, even if the body contains only a single statement. The first statement of a non-empty block must begin on its own line.

✅ Good:

```ts
for (let i = 0; i < x; i++) {
  doSomethingWith(i);
}

if (x) {
  doSomethingWithALongMethodNameThatForcesANewLine(x);
}
```

❌ Bad:

```ts
if (x)
  doSomethingWithALongMethodNameThatForcesANewLine(x);

for (let i = 0; i < x; i++) doSomethingWith(i);
```

**Exception:** `if` statements fitting on one line _may_ elide the block.

✅ Good:

```ts
if (x) x.doFoo();
```

#### Assignment in control statements

Prefer to avoid assignment of variables inside control statements. Assignment can be easily mistaken for equality checks inside control statements.

❌ Bad:

```ts
if (x = someFunction()) {
  // Assignment easily mistaken with equality check
  // ...
}
```

✅ Good:

```ts
x = someFunction();
if (x) {
  // ...
}
```

In cases where assignment inside the control statement is preferred, enclose the assignment in additional parenthesis to indicate it is intentional.

```ts
while ((x = someFunction())) {
  // Double parenthesis shows assignment is intentional
  // ...
}
```

#### Iterating containers

Prefer `for (... of someArr)` to iterate over arrays. `Array.prototype.forEach` and vanilla `for` loops are also allowed:

✅ Good:

```ts
for (const x of someArr) {
  // x is a value of someArr.
}

for (let i = 0; i < someArr.length; i++) {
  // Explicitly count if the index is needed, otherwise use the for/of form.
  const x = someArr[i];
  // ...
}
for (const [i, x] of someArr.entries()) {
  // Alternative version of the above.
}
```

`for`-`in` loops may only be used on dict-style objects (see below for more info). Do not use `for (... in ...)` to iterate over arrays as it will counterintuitively give the array's indices (as strings!), not values:

❌ Bad:

```ts
for (const x in someArray) {
  // x is the index!
}
```

`Object.prototype.hasOwnProperty` should be used in `for`-`in` loops to exclude unwanted prototype properties. Prefer `for`-`of` with `Object.keys`, `Object.values`, or `Object.entries` over `for`-`in` when possible.

✅ Good:

```ts
for (const key in obj) {
  if (!obj.hasOwnProperty(key)) continue;
  doWork(key, obj[key]);
}
for (const key of Object.keys(obj)) {
  doWork(key, obj[key]);
}
for (const value of Object.values(obj)) {
  doWorkValOnly(value);
}
for (const [key, value] of Object.entries(obj)) {
  doWork(key, value);
}
```

### Grouping parentheses

Optional grouping parentheses are omitted only when the author and reviewer agree that there is no reasonable chance that the code will be misinterpreted without them, nor would they have made the code easier to read. It is _not_ reasonable to assume that every reader has the entire operator precedence table memorized.

Do not use unnecessary parentheses around the entire expression following `delete`, `typeof`, `void`, `return`, `throw`, `case`, `in`, `of`, or `yield`.

### Exception handling

Exceptions are an important part of the language and should be used whenever exceptional cases occur.

Custom exceptions provide a great way to convey additional error information from functions. They should be defined and used wherever the native `Error` type is insufficient.

Prefer throwing exceptions over ad-hoc error-handling approaches (such as passing an error container reference type, or returning an object with an error property).

#### Instantiate errors using `new`

Always use `new Error()` when instantiating exceptions, instead of just calling `Error()`. Both forms create a new `Error` instance, but using `new` is more consistent with how other objects are instantiated.

✅ Good:

```ts
throw new Error('Foo is not a valid bar.');
```

❌ Bad:

```ts
throw Error('Foo is not a valid bar.');
```

#### Only throw errors

JavaScript (and thus TypeScript) allow throwing or rejecting a Promise with arbitrary values. However if the thrown or rejected value is not an `Error`, it does not populate stack trace information, making debugging hard. This treatment extends to `Promise` rejection values as `Promise.reject(obj)` is equivalent to `throw obj;` in async functions.

❌ Bad:

```ts
// bad: does not get a stack trace.
throw 'oh noes!';
// For promises
new Promise((resolve, reject) => void reject('oh noes!'));
Promise.reject();
Promise.reject('oh noes!');
```

Instead, only throw (subclasses of) `Error`:

✅ Good:

```ts
// Throw only Errors
throw new Error('oh noes!');
// ... or subtypes of Error.
class MyError extends Error {}
throw new MyError('my oh noes!');
// For promises
new Promise((resolve) => resolve()); // No reject is OK.
new Promise((resolve, reject) => void reject(new Error('oh noes!')));
Promise.reject(new Error('oh noes!'));
```

#### Catching and rethrowing

When catching errors, code _should_ assume that all thrown errors are instances of `Error`.

✅ Good:

```ts
function assertIsError(e: unknown): asserts e is Error {
  if (!(e instanceof Error)) throw new Error("e is not an Error");
}

try {
  doSomething();
} catch (e: unknown) {
  // All thrown errors must be Error subtypes. Do not handle
  // other possible values unless you know they are thrown.
  assertIsError(e);
  displayError(e.message);
  // or rethrow:
  throw e;
}
```

Exception handlers _must not_ defensively handle non-`Error` types unless the called API is conclusively known to throw non-`Error`s in violation of the above rule. In that case, a comment should be included to specifically identify where the non-`Error`s originate.

✅ Good:

```ts
try {
  badApiThrowingStrings();
} catch (e: unknown) {
  // Note: bad API throws strings instead of errors.
  if (typeof e === 'string') { ... }
}
```

**Why?**

Avoid [overly defensive programming](https://en.wikipedia.org/wiki/Defensive_programming#Offensive_programming). Repeating the same defenses against a problem that will not exist in most code leads to boiler-plate code that is not useful.

#### Empty catch blocks

It is very rarely correct to do nothing in response to a caught exception. When it truly is appropriate to take no action whatsoever in a catch block, the reason this is justified is explained in a comment.

✅ Good:

```ts
  try {
    return handleNumericResponse(response);
  } catch (e: unknown) {
    // Response is not numeric. Continue to handle as text.
  }
  return handleTextResponse(response);
```

Disallowed:

❌ Bad:

```ts
  try {
    shouldFail();
    fail('expected an error');
  } catch (expected: unknown) {
  }
```

Tip: Unlike in some other languages, patterns like the above simply don’t work since this will catch the error thrown by `fail`. Use `assertThrows()` instead.

### Switch statements

All `switch` statements _must_ contain a `default` statement group, even if it contains no code. The `default` statement group must be last.

✅ Good:

```ts
switch (x) {
  case Y:
    doSomethingElse();
    break;
  default:
    // nothing to do.
}
```

Within a switch block, each statement group either terminates abruptly with a `break`, a `return` statement, or by throwing an exception. Non-empty statement groups (`case ...`) _must not_ fall through (enforced by the compiler):

❌ Bad:

```ts
switch (x) {
  case X:
    doSomething();
    // fall through - not allowed!
  case Y:
    // ...
}
```

Empty statement groups are allowed to fall through:

✅ Good:

```ts
switch (x) {
  case X:
  case Y:
    doSomething();
    break;
  default: // nothing to do.
}
```

### Equality checks

Always use triple equals (`===`) and not equals (`!==`). The double equality operators cause error prone type coercions that are hard to understand and slower to implement for JavaScript Virtual Machines. See also the [JavaScript equality table](https://dorey.github.io/JavaScript-Equality-Table/).

❌ Bad:

```ts
if (foo == 'bar' || baz != bam) {
  // Hard to understand behaviour due to type coercion.
}
```

✅ Good:

```ts
if (foo === 'bar' || baz !== bam) {
  // All good here.
}
```

**Exception:** Comparisons to the literal `null` value _may_ use the `==` and `!=` operators to cover both `null` and `undefined` values.

✅ Good:

```ts
if (foo == null) {
  // Will trigger when foo is null or undefined.
}
```

### Type and non-nullability assertions

Type assertions (`x as SomeType`) and non-nullability assertions (`y!`) are unsafe. Both only silence the TypeScript compiler, but do not insert any runtime checks to match these assertions, so they can cause your program to crash at runtime.

Because of this, you _should not_ use type and non-nullability assertions without an obvious or explicit reason for doing so.

Instead of the following:

❌ Bad:

```ts
(x as Foo).foo();

y!.bar();
```

When you want to assert a type or non-nullability the best answer is to explicitly write a runtime check that performs that check.

✅ Good:

```ts
// assuming Foo is a class.
if (x instanceof Foo) {
  x.foo();
}

if (y) {
  y.bar();
}
```

Sometimes due to some local property of your code you can be sure that the assertion form is safe. In those situations, you _should_ add clarification to explain why you are ok with the unsafe behavior:

✅ Good:

```ts
// x is a Foo, because ...
(x as Foo).foo();

// y cannot be null, because ...
y!.bar();
```

If the reasoning behind a type or non-nullability assertion is obvious, the comments _may_ not be necessary. For example, generated proto code is always nullable, but perhaps it is well-known in the context of the code that certain fields are always provided by the backend. Use your judgement.

#### Type assertion syntax

Type assertions _must_ use the `as` syntax (as opposed to the angle brackets syntax). This enforces parentheses around the assertion when accessing a member.

❌ Bad:

```ts
const x = (<Foo>z).length;
const y = <Foo>z.length;
```

✅ Good:

```ts
// z must be Foo because ...
const x = (z as Foo).length;
```

#### Double assertions

From the [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions), TypeScript only allows type assertions which convert to a _more specific_ or _less specific_ version of a type. Adding a type assertion (`x as Foo`) which does not meet this criteria will give the error: Conversion of type 'X' to type 'Y' may be a mistake because neither type sufficiently overlaps with the other.

If you are sure an assertion is safe, you can perform a _double assertion_. This involves casting through `unknown` since it is less specific than all types.

✅ Good:

```ts
// x is a Foo here, because...
(x as unknown as Foo).fooMethod();
```

Use `unknown` (instead of `any` or `{}`) as the intermediate type.

#### Type assertions and object literals

Use type annotations (`: Foo`) instead of type assertions (`as Foo`) to specify the type of an object literal. This allows detecting refactoring bugs when the fields of an interface change over time.

❌ Bad:

```ts
interface Foo {
  bar: number;
  baz?: string;  // was "bam", but later renamed to "baz".
}

const foo = {
  bar: 123,
  bam: 'abc',  // no error!
} as Foo;

function func() {
  return {
    bar: 123,
    bam: 'abc',  // no error!
  } as Foo;
}
```

✅ Good:

```ts
interface Foo {
  bar: number;
  baz?: string;
}

const foo: Foo = {
  bar: 123,
  bam: 'abc',  // complains about "bam" not being defined on Foo.
};

function func(): Foo {
  return {
    bar: 123,
    bam: 'abc',   // complains about "bam" not being defined on Foo.
  };
}
```

### Keep try blocks focused

Limit the amount of code inside a try block, if this can be done without hurting readability.

❌ Bad:

```ts
try {
  const result = methodThatMayThrow();
  use(result);
} catch (error: unknown) {
  // ...
}
```

✅ Good:

```ts
let result;
try {
  result = methodThatMayThrow();
} catch (error: unknown) {
  // ...
}
use(result);
```

Moving the non-throwable lines out of the try/catch block helps the reader learn which method throws exceptions. Some inline calls that do not throw exceptions could stay inside because they might not be worth the extra complication of a temporary variable.

**Exception:** There may be performance issues if try blocks are inside a loop. Widening try blocks to cover a whole loop is ok.
