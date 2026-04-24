# TypeScript & JavaScript Guidelines

Every rule below is a hard constraint. Apply when writing or modifying
TypeScript & JavaScript code — not only during review. Rules are grouped by tier:

- **Tier 1 (correctness + security)**: violating these produces bugs or
  vulnerabilities. Never violate.
- **Tier 2 (modernization + performance)**: non-violation keeps code
  current and efficient. Match unless the project's toolchain forbids it.

For framework-specific rules (React, Django, etc.), load the matching
file from `frameworks/`. For Tier 3 style/pedantic rules, load `style.md`.
Full per-rule docs with edge cases: `rules/<slug>/index.md`.

---

## Tier 1 — Correctness & Security
*132 rules*

### Plugin: `eslint`

### eslint/block-scoped-var
Enforce that variables are both **declared** and **used** within the same block scope.
❌ 
```
/* block-scoped-var: "error" */
function doIf() {
  if (true) {
    var build = true;
  }
  console.log(build);
…
```
✅ 
```
/* block-scoped-var: "error" */
function doIf() {
  var build;
  if (true) {
    build = true;
  }
…
```

### eslint/constructor-super
Require `super()` calls in constructors of derived classes and disallows `super()` calls in constructors of non-derived classes.
❌ 
```
// Missing super() call
class A extends B {
    constructor() { }
}
// super() in non-derived class
class A {
…
```
✅ 
```
// Proper super() call in derived class
class A extends B {
  constructor() {
    super();
  }
}
…
```

### eslint/for-direction
Do not use `for` loops where the update clause moves the counter in the wrong direction, preventing the loop from reaching its stop condition.
❌ 
```
/* for-direction: "error" */
for (var i = 0; i < 10; i--) {}
for (var i = 10; i >= 0; i++) {}
for (var i = 0; i > 10; i++) {}
for (var i = 0; 10 > i; i--) {}
const n = -2;
…
```
✅ 
```
/* for-direction: "error" */
for (var i = 0; i < 10; i++) {}
for (var i = 0; 10 > i; i++) {
  // with counter "i" on the right
}
for (let i = 10; i >= 0; i += this.step) {
…
```

### eslint/no-async-promise-executor
Do not use using an async function as a Promise executor.
❌ 
```
const foo = new Promise(async (resolve, reject) => {
  readFile("foo.txt", function (err, result) {
    if (err) {
      reject(err);
    } else {
      resolve(result);
…
```
✅ 
```
const foo = new Promise((resolve, reject) => {
  readFile("foo.txt", function (err, result) {
    if (err) {
      reject(err);
    } else {
      resolve(result);
…
```

### eslint/no-caller
Do not use the use of `arguments.caller` or `arguments.callee`.
❌ 
```
function foo(n) {
  if (n <= 0) {
    return;
  }
  arguments.callee(n - 1);
}
…
```
✅ 
```
function foo(n) {
  if (n <= 0) {
    return;
  }
  foo(n - 1);
}
…
```

### eslint/no-class-assign
Do not use reassigning class variables.
❌ 
```
class A {}
A = 0;
```
✅ 
```
let A = class A {};
A = 0; // A is a variable.
```

### eslint/no-compare-neg-zero
Do not use comparing against `-0`
❌ 
```
if (x === -0) {
  // doSomething()...
}
```
✅ 
```
if (x === 0) {
  // doSomething()...
}
```

### eslint/no-const-assign
Do not use reassigning `const` variables.
❌ 
```
const a = 0;
a = 1;
const b = 0;
b += 1;
```
✅ 
```
const a = 0;
console.log(a);
var b = 0;
b += 1;
```

### eslint/no-constant-binary-expression
Do not use expressions where the operation doesn't affect the value.
❌ 
```
// One might think this would evaluate as `a + (b ?? c)`:
const x = a + b ?? c;
// But it actually evaluates as `(a + b) ?? c`. Since `a + b` can never be null,
// the `?? c` has no effect.
// Programmers coming from a language where objects are compared by value might expect this to work:
const isEmpty = x === [];
…
```
✅ 
```
const x = a + (b ?? c);
const isEmpty = x.length === 0;
```

### eslint/no-constant-condition
Do not use constant expressions in conditions.
❌ 
```
if (false) {
  doSomethingUnfinished();
}
if (new Boolean(x)) {
  doSomethingAlways();
}
…
```
✅ 
```
if (x === 0) {
  doSomething();
}
while (typeof x === "undefined") {
  doSomething();
}
```

### eslint/no-control-regex
Do not use control characters and some escape sequences that match control characters in regular expressions.
❌ 
```
var pattern1 = /\x00/;
var pattern2 = /\x0C/;
var pattern3 = /\x1F/;
var pattern4 = /\u000C/;
var pattern5 = /\u{C}/u;
var pattern6 = new RegExp("\x0C"); // raw U+000C character in the pattern
…
```
✅ 
```
var pattern1 = /\x20/;
var pattern2 = /\u0020/;
var pattern3 = /\u{20}/u;
var pattern4 = /\t/;
var pattern5 = /\n/;
var pattern6 = new RegExp("\x20");
…
```

### eslint/no-debugger
Avoid usage of the `debugger` statement.
❌ 
```
async function main() {
  const data = await getData();
  const result = complexCalculation(data);
  debugger;
}
```
✅ 
```
async function main() {
  const data = await getData();
  const result = complexCalculation(data);
}
```

### eslint/no-delete-var
The purpose of the `delete` operator is to remove a property from an object.
❌ 
```
var x;
delete x;
```
✅ 
```
var x;
var y;
delete y.prop;
```

### eslint/no-dupe-class-members
Do not use duplicate class members.
❌ 
```
class A {
  foo() {
    console.log("foo");
  }
  foo = 123;
}
…
```
✅ 
```
class A {
  foo() {
    console.log("foo");
  }
}
let a = new A();
…
```

### eslint/no-dupe-else-if
Do not use duplicate conditions in if-else-if chains.
❌ 
```
if (a) {
  foo();
} else if (b) {
  bar();
} else if (b) {
  baz();
…
```
✅ 
```
if (a) {
  foo();
} else if (b) {
  bar();
} else if (c) {
  baz();
…
```

### eslint/no-dupe-keys
Do not use duplicate keys in object literals.
❌ 
```
var foo = {
  bar: "baz",
  bar: "qux",
};
var foo = {
  bar: "baz",
…
```
✅ 
```
var foo = {
  bar: "baz",
  qux: "qux",
};
```

### eslint/no-duplicate-case
Do not use duplicate case labels.
❌ 
```
var a = 1,
  one = 1;
switch (a) {
  case 1:
    break;
  case 2:
…
```
✅ 
```
var a = 1,
  one = 1;
switch (a) {
  case 1:
    break;
  case 2:
…
```

### eslint/no-empty-character-class
Do not use empty character classes in regular expressions.
❌ `var foo = /^abc[]/;`
✅ 
```
var foo = /^abc/;
var foo2 = /^abc[123]/;
```

### eslint/no-empty-pattern
Do not use empty destructuring patterns.

### eslint/no-empty-static-block
Do not use the usages of empty static blocks.
❌ 
```
class Foo {
  static {}
}
```
✅ 
```
class Foo {
  static {
    // blocks with comments are allowed
  }
}
class Bar {
…
```

### eslint/no-eval
Do not use referencing the `eval` function.
❌ 
```
const obj = { x: "foo" },
  key = "x",
  value = eval("obj." + key);
(0, eval)("const a = 0");
const foo = eval;
foo("const a = 0");
…
```
✅ 
```
const obj = { x: "foo" },
  key = "x",
  value = obj[key];
class A {
  foo() {
    this.eval("const a = 0");
…
```

### eslint/no-ex-assign
Do not use reassigning exceptions in catch clauses.
❌ 
```
try {
  // code
} catch (e) {
  e = 10;
}
```
✅ 
```
try {
  // code
} catch (e) {
  let val = 10;
}
```

### eslint/no-extend-native
Prevent extending native global objects such as `Object`, `String`, or `Array` with new properties.
❌ 
```
Object.prototype.p = 0;
Object.defineProperty(Array.prototype, "p", { value: 0 });
```
✅ 
```
x.prototype.p = 0;
Object.defineProperty(x.prototype, "p", { value: 0 });
```

### eslint/no-extra-bind
Do not use unnecessary calls to `.bind()`.
❌ 
```
const x = function () {
  foo();
}.bind(bar);
const z = (() => {
  this.foo();
}).bind(this);
```
✅ 
```
const x = function () {
  this.foo();
}.bind(bar);
const y = function (a) {
  return a + 1;
}.bind(foo, bar);
```

### eslint/no-extra-boolean-cast
This rule disallows unnecessary boolean casts.
❌ 
```
var foo = !!!bar;
var foo = Boolean(!!bar);
if (!!foo) {
}
if (Boolean(foo)) {
}
…
```
✅ 
```
var foo = !bar;
var foo = Boolean(bar);
if (foo) {
}
if (foo) {
}
…
```

### eslint/no-func-assign
Do not use reassigning `function` declarations.
❌ 
```
function foo() {}
foo = bar;
```
✅ 
```
let foo = function () {};
foo = bar;
```

### eslint/no-global-assign
Do not use modifications to read-only global variables.
❌ `Object = null;`

### eslint/no-import-assign
Do not use assigning to imported bindings.
❌ 
```
import mod, { named } from "./mod.mjs";
import * as mod_ns from "./mod.mjs";
mod = 1; // ERROR: 'mod' is readonly.
named = 2; // ERROR: 'named' is readonly.
mod_ns.named = 3; // ERROR: The members of 'mod_ns' are readonly.
mod_ns = {}; // ERROR: 'mod_ns' is readonly.
…
```

### eslint/no-invalid-regexp
Do not use invalid regular expression strings in RegExp constructors.
❌ 
```
RegExp("[");
RegExp(".", "z");
new RegExp("\\");
```
✅ 
```
RegExp(".");
new RegExp();
this.RegExp("[");
```

### eslint/no-irregular-whitespace
Do not use the use of irregular whitespace characters in the code.
❌ 
```
// Contains irregular whitespace characters (invisible)
function example() {
  var foo = "bar"; // irregular whitespace before 'bar'
}
```
✅ 
```
function example() {
  var foo = "bar"; // regular spaces only
}
```

### eslint/no-iterator
Do not use the use of the `__iterator__` property.
❌ 
```
Foo.prototype.__iterator__ = function () {
  return new FooIterator(this);
};
foo.__iterator__ = function () {};
foo["__iterator__"] = function () {};
```
✅ 
```
const __iterator__ = 42; // not using the __iterator__ property
Foo.prototype[Symbol.iterator] = function () {
  return new FooIterator(this);
};
```

### eslint/no-loss-of-precision
Do not use precision loss of number literal.
❌ `var x = 2e999;`
✅ `var x = 12345;`

### eslint/no-misleading-character-class
This rule reports regular expressions which include multiple code point characters in character class syntax.

### eslint/no-new
Do not use new operators outside of assignments or comparisons.
❌ 
```
new Person();
() => {
  new Date();
};
```
✅ `var a = new Date()(() => new Date());`

### eslint/no-new-native-nonconstructor
Do not use `new` operators with global non-constructor functions (`Symbol`, `BigInt`).
❌ 
```
// throws a TypeError
let foo = new Symbol("foo");
// throws a TypeError
let result = new BigInt(9007199254740991);
```
✅ 
```
let foo = Symbol("foo");
let result = BigInt(9007199254740991);
```

### eslint/no-nonoctal-decimal-escape
This rule disallows \8 and \9 escape sequences in string literals.
❌ 
```
let x = "\8";
let y = "\9";
```
✅ 
```
let x = "8";
let y = "\\9";
```

### eslint/no-obj-calls
Do not use calling some global objects as functions.
❌ 
```
let math = Math();
let newMath = new Math();
let json = JSON();
let newJson = new JSON();
let atomics = Atomics();
let newAtomics = new Atomics();
…
```
✅ 
```
let area = (r) => 2 * Math.PI * r * r;
let object = JSON.parse("{}");
let first = Atomics.load(sharedArray, 0);
let segmenterFrom = Intl.Segmenter("fr", { granularity: "word" });
```

### eslint/no-self-assign
Do not use assignments where both sides are exactly the same.
❌ 
```
foo = foo;
[a, b] = [a, b];
[a, ...b] = [x, ...b];
({ a, b } = { a, x });
foo &&= foo;
foo ||= foo;
…
```
✅ 
```
foo = bar;
[a, b] = [b, a];
// This pattern is warned by the `no-use-before-define` rule.
let foo = foo;
// The default values have an effect.
[foo = 1] = [foo];
…
```

### eslint/no-setter-return
Setters cannot return values.
❌ 
```
class URL {
  set origin() {
    return true;
  }
}
```

### eslint/no-shadow
Do not use variable declarations from shadowing variables declared in the outer scope.
❌ 
```
var x = 1;
function foo() {
  var x = 2; // x shadows the outer x
}
```
✅ 
```
var x = 1;
function foo() {
  var y = 2; // different name, no shadowing
}
```

### eslint/no-shadow-restricted-names
Do not use the redefining of global variables such as `undefined`, `NaN`, `Infinity`, `eval`, `globalThis` and `arguments`.
❌ 
```
function NaN() {}
!function (Infinity) {};
var undefined = 5;
try {
} catch (eval) {}
const globalThis = "foo";
```
✅ 
```
var Object;
function f(a, b) {}
// Exception: `undefined` may be shadowed if the variable is never assigned a value.
var undefined;
```

### eslint/no-sparse-arrays
Do not use sparse arrays.
❌ `var items = [, ,];`
✅ `var items = [];`

### eslint/no-this-before-super
Require calling `super()` before using `this` or `super`.
❌ 
```
class A1 extends B {
  constructor() {
    // super() needs to be called first
    this.a = 0;
    super();
  }
…
```

### eslint/no-unassigned-vars
Do not use let or var variables that are read but never assigned.
❌ 
```
let status;
if (status === "ready") {
  console.log("Ready!");
}
```
✅ 
```
let message = "hello";
console.log(message);
let user;
user = getUser();
console.log(user.name);
```

### eslint/no-unexpected-multiline
In most cases, semicolons are not required in JavaScript in order for code to be parsed and executed as expected.
❌ 
```
var a = b(x || y).doSomething();
var a = b[(a, b, c)].forEach(doSomething);
let x = (function () {})`hello`;
foo / bar / g.test(baz);
```
✅ 
```
var a = b;
(x || y).doSomething();
var a = b;
[a, b, c].forEach(doSomething);
let x = function () {};
`hello`;
…
```

### eslint/no-unmodified-loop-condition
Do not use references in loop conditions that are never modified within the loop.
❌ 
```
let done = false;
while (!done) {
  work();
}
```
✅ 
```
let done = false;
while (!done) {
  done = checkDone();
}
```

### eslint/no-unneeded-ternary
Do not use ternary operators when simpler alternatives exist.
❌ 
```
const isYes = answer === 1 ? true : false;
const isNo = answer === 1 ? false : true;
foo(bar ? bar : 1);
```
✅ 
```
const isYes = answer === 1;
const isNo = answer !== 1;
foo(bar || 1);
```

### eslint/no-unsafe-finally
Do not use control flow statements in `finally` blocks.
❌ 
```
// We expect this function to return 1;
(() => {
  try {
    return 1; // 1 is returned but suspended until finally block ends
  } catch (err) {
    return 2;
…
```

### eslint/no-unsafe-negation
Do not use negating the left operand of relational operators to prevent logical errors caused by misunderstanding operator precedence or accidental use of negation.
❌ 
```
if (!key in object) {}
if (!obj instanceof Ctor) {}
```
✅ 
```
if (!(key in object)) {}
if (!(obj instanceof Ctor)) {}
```

### eslint/no-unsafe-optional-chaining
Do not use use of optional chaining in contexts where the `undefined` value is not allowed.
❌ 
```
var obj = undefined;
1 in obj?.foo; // TypeError
with (obj?.foo); // TypeError
for (bar of obj?.foo); // TypeError
bar instanceof obj?.foo; // TypeError
const { bar } = obj?.foo; // TypeError
```

### eslint/no-unused-expressions
This rule disallows unused expressions.
❌ 
```
Set<number>;
1 as number;
window!;
```
✅ `const foo = new Set<number>();`

### eslint/no-unused-labels
Do not use unused labels.
❌ 
```
OUTER_LOOP: for (const student of students) {
  if (checkScores(student.scores)) {
    continue;
  }
  doSomething(student);
}
```
✅ 
```
for (const student of students) {
  if (checkScores(student.scores)) {
    continue;
  }
  doSomething(student);
}
```

### eslint/no-unused-private-class-members
Do not use unused private class members.
❌ 
```
class A {
  #unusedMember = 5;
}
class B {
  #usedOnlyInWrite = 5;
  method() {
…
```
✅ 
```
class A {
  #usedMember = 42;
  method() {
    return this.#usedMember;
  }
}
…
```

### eslint/no-unused-vars
Do not use variable declarations, imports, or type declarations that are not used in code.
❌ 
```
/* no-unused-vars: "error" */
/* if you have `some_unused_var` defined as a global in .oxlintrc.json */
// It checks variables you have defined as global
some_unused_var = 42;
var x;
// Write-only variables are not considered as used.
…
```
✅ 
```
/* no-unused-vars: "error" */
var x = 10;
alert(x);
// foo is considered used here
myFunc(
  function foo() {
…
```

### eslint/no-useless-backreference
Do not use backreferences in regular expressions that will always be ignored because the capture group they refer to has not matched and cannot match at the time the backreference is evaluated.
❌ 
```
/\1(a)/; // backreference appears before group
/(a|\1b)/; // group and reference are in different alternatives
/(?<=\1(a))b/; // backreference used before group in lookbehind
/\1(?!(a))/; // group is inside negative lookahead
/(a\1)/; // backreference is inside its own group
```
✅ 
```
/(a)\1/; // valid — backreference follows completed group
/(?<name>a)\k<name>/; // named group used properly
/(?:a|(b))\1/; // backreference only used when group matches
```

### eslint/no-useless-catch
Do not use unnecessary catch clauses.
❌ 
```
try {
  doSomethingThatMightThrow();
} catch (e) {
  throw e;
}
```
✅ `doSomethingThatMightThrow();`

### eslint/no-useless-concat
Do not use unnecessary concatenation of literals or template literals.
❌ `var foo = "a" + "b";`
✅ 
```
var foo = "a" + bar;
// When the string concatenation is multiline
var foo = "a" + "b" + "c";
```

### eslint/no-useless-constructor
Do not use constructors that can be safely removed without changing how the class works.
❌ 
```
class A {
  constructor() {}
}
class B extends A {
  constructor(...args) {
    super(...args);
…
```
✅ 
```
class A {}
class B {
  constructor() {
    doSomething();
  }
}
…
```

### eslint/no-useless-escape
Do not use unnecessary escape characters.
❌ 
```
"\'";
'\"';
"\#";
"\e";
`\"`;
`\"${foo}\"`;
…
```
✅ 
```
"\"";
'\'';
"\x12";
"\u00a9";
"\371";
"xs\u2111";
…
```

### eslint/no-useless-rename
Do not use renaming import, export, and destructured assignments to the same name.
❌ 
```
import { foo as foo } from "foo";
const { bar: bar } = obj;
export { baz as baz };
```
✅ 
```
import { foo } from "foo";
const { bar: renamed } = obj;
export { baz };
```

### eslint/no-with
Do not use `with` statements.
❌ 
```
with (point) {
  r = Math.sqrt(x * x + y * y); // is r a member of point?
}
```

### eslint/preserve-caught-error
Enforce that when re-throwing an error in a catch block, the original error is preserved using the 'cause' property.
❌ 
```
try {
  doSomething();
} catch (err) {
  throw new Error("Something failed");
}
```
✅ 
```
try {
  doSomething();
} catch (err) {
  throw new Error("Something failed", { cause: err });
}
```

### eslint/require-yield
This rule generates warnings for generator functions that do not have the yield keyword.
❌ 
```
function* foo() {
  return 10;
}
```

### eslint/use-isnan
Do not use checking against `NaN` without using `isNaN()` call.
❌ 
```
foo == NaN;
foo === NaN;
foo <= NaN;
foo > NaN;
```

### eslint/valid-typeof
Enforce comparing `typeof` expressions against valid strings.
❌ 
```
typeof foo === "strnig";
typeof foo == "undefimed";
typeof bar != "nunber"; // spellchecker:disable-line
typeof bar !== "fucntion"; // spellchecker:disable-line
```
✅ 
```
typeof foo === "string";
typeof bar == "undefined";
typeof foo === baz;
typeof bar === typeof qux;
```

### Plugin: `import`

### import/default
If a default import is requested, this rule will report if there is no default export in the imported module.
❌ 
```
// ./bar.js
export function bar() {
  return null;
}
// ./foo.js
import bar from "./bar"; // no default export found in ./bar
```
✅ 
```
// ./bar.js
export default function bar() {
  return null;
}
// ./foo.js
import { bar } from "./bar"; // correct usage of named import
```

### import/namespace
Enforce names exist at the time they are dereferenced, when imported as a full namespace (i.e.
❌ 
```
// ./qux.js
import * as foo from "./foo";
foo.notExported(); // Error: notExported is not exported
// Assignment to a member of an imported namespace
foo.bar = "new value"; // Error: bar cannot be reassigned
// Computed reference to a non-existent export
…
```
✅ 
```
// ./baz.js
import * as foo from "./foo";
console.log(foo.bar); // Valid: bar is exported
// Computed reference
const method = "bar";
foo[method](); // Valid: method refers to an exported function
```

### import/no-absolute-path
This rule forbids the import of modules using absolute paths.
❌ 
```
import f from "/foo";
import f from "/some/path";
var f = require("/foo");
var f = require("/some/path");
```
✅ 
```
import _ from "lodash";
import foo from "foo";
import foo from "./foo";
var _ = require("lodash");
var foo = require("foo");
var foo = require("./foo");
```

### import/no-empty-named-blocks
Enforce that named import blocks are not empty.
❌ 
```
import {} from "mod";
import Default from "mod";
```
✅ 
```
import { mod } from "mod";
import Default, { mod } from "mod";
```

### import/no-named-as-default
Avoid use of an exported name as the locally imported name of a default export.
❌ 
```
// Invalid: using exported name 'bar' as the identifier for default export.
import bar from "./foo.js";
```
✅ 
```
// Valid: correctly importing default export with a non-conflicting name.
import foo from "./foo.js";
```

### import/no-named-as-default-member
Avoid the use of an exported name (named export) as a property on the default export.
❌ 
```
// ./foo.js
import foo from "./bar";
const bar = foo.bar; // Incorrect: trying to access named export via default
```
✅ 
```
// ./foo.js
import { bar } from "./bar"; // Correct: accessing named export directly
```

### import/no-self-import
Do not use a module from importing itself.
❌ 
```
// foo.js
import foo from "./foo.js"; // Incorrect: module imports itself
const foo = require("./foo"); // Incorrect: module imports itself
```
✅ 
```
// foo.js
import bar from "./bar.js"; // Correct: module imports another module
```

### import/no-unassigned-import
This rule aims to remove modules with side-effects by reporting when a module is imported but not assigned.
❌ 
```
import "should";
require("should");
```
✅ 
```
import _ from "foo";
import _, { foo } from "foo";
import _, { foo as bar } from "foo";
const _ = require("foo");
const { foo } = require("foo");
const { foo: bar } = require("foo");
…
```

### Plugin: `oxc`

### oxc/approx-constant
Do not use the use of approximate constants, instead preferring the use of the constants in the `Math` object.
❌ `let log10e = 0.434294;`
✅ `let log10e = Math.LOG10E;`

### oxc/bad-array-method-on-arguments
This rule applies when an array method is called on the arguments object itself.
❌ 
```
function add(x, y) {
  return x + y;
}
function sum() {
  return arguments.reduce(add, 0);
}
```
✅ 
```
function add(x, y) {
  return x + y;
}
function sum(...args) {
  return args.reduce(add, 0);
}
```

### oxc/bad-char-at-comparison
This rule warns when the return value of the `charAt` method is used to compare a string of length greater than 1.
❌ 
```
a.charAt(4) === "a2";
a.charAt(4) === "/n";
```
✅ 
```
a.charAt(4) === "a";
a.charAt(4) === "\n";
```

### oxc/bad-comparison-sequence
This rule applies when the comparison operator is applied two or more times in a row.
❌ 
```
if ((a == b) == c) {
  console.log("a, b, and c are the same");
}
```
✅ 
```
if (a == b && b == c) {
  console.log("a, b, and c are the same");
}
```

### oxc/bad-min-max-func
Whether the clamp function `Math.min(Math.max(x, y), z)` always evaluate to a constant result because the arguments are in the wrong order.
❌ 
```
Math.min(Math.max(100, x), 0);
Math.max(1000, Math.min(0, z));
```
✅ 
```
Math.max(0, Math.min(100, x));
Math.min(1000, Math.max(0, z));
```

### oxc/bad-object-literal-comparison
Avoid comparisons between object and array literals.
❌ 
```
if (x === {}) {
}
if (arr !== []) {
}
```
✅ 
```
if (typeof x === "object" && Object.keys(x).length === 0) {
}
if (Array.isArray(x) && x.length === 0) {
}
```

### oxc/bad-replace-all-arg
This rule warns when the `replaceAll` method is called with a regular expression that does not have the global flag (g).
❌ `withSpaces.replaceAll(/\s+/, ",");`
✅ `withSpaces.replaceAll(/\s+/g, ",");`

### oxc/const-comparisons
Avoid redundant or logically impossible comparisons.
❌ 
```
status_code <= 400 && status_code > 500;
status_code < 200 && status_code <= 299;
status_code > 500 && status_code >= 500;
a < a; // Always false
a >= a; // Always true
```
✅ 
```
status_code >= 400 && status_code < 500;
500 <= status_code && 600 > status_code;
500 <= status_code && status_code <= 600;
a < b;
a <= b;
```

### oxc/double-comparisons
This rule checks for double comparisons in logical expressions.
❌ 
```
x === y || x < y;
x < y || x === y;
```
✅ 
```
x <= y;
x >= y;
```

### oxc/erasing-op
Avoid erasing operations, e.g., `x * 0`.
❌ 
```
let x = 1;
let y = x * 0;
```
✅ 
```
let x = 1;
let y = 0;
```

### oxc/misrefactored-assign-op
Https://rust-lang.github.io/rust-clippy/master/#/misrefactored\_assign\_op Checks for `a op= a op b` or `a op= b op a` patterns.
❌ 
```
a += a + b;
a -= a - b;
```
✅ 
```
a += b;
a -= b;
```

### oxc/missing-throw
Whether the `throw` keyword is missing in front of a `new` expression.
❌ 
```
function foo() {
  throw Error();
}
const foo = () => {
  new Error();
};
```
✅ 
```
function foo() {
  throw new Error();
}
const foo = () => {
  throw new Error();
};
```

### oxc/no-async-endpoint-handlers
Do not use the use of `async` functions as Express endpoint handlers.
❌ 
```
const app = express();
app.get("/", async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});
const router = express.Router();
…
```
✅ 
```
const app = express();
// not async
app.use((req, res, next) => {
  req.receivedAt = Date.now();
});
app.get("/", (req, res, next) => {
…
```

### oxc/no-this-in-exported-function
Do not use the use of `this` in exported functions.
❌ 
```
export function foo() {
  console.log(this);
}
export default function bar() {
  this.something();
}
…
```
✅ 
```
function foo() {
  console.log(this);
}
export const bar = () => {
  console.log(this);
};
```

### oxc/number-arg-out-of-range
Whether the radix or precision arguments of number-related functions exceeds the limit.
❌ 
```
var x = 42;
var s_radix_64 = x.toString(64);
var s = x.toString(1);
```
✅ 
```
var x = 42;
var s_radix_16 = x.toString(16);
```

### oxc/only-used-in-recursion
Avoid arguments that are only used in recursion with no side-effects.
❌ 
```
function test(onlyUsedInRecursion) {
  return test(onlyUsedInRecursion);
}
```
✅ 
```
function f(a: number): number {
  if (a == 0) {
    return 1;
  } else {
    return f(a - 1);
  }
…
```

### oxc/uninvoked-array-callback
This rule applies when an Array function has a callback argument used for an array with empty slots.
❌ `const list = new Array(5).map((_) => createElement());`
✅ `const list = new Array(5).fill().map((_) => createElement());`

### Plugin: `promise`

### promise/always-return
Require returning inside each `then()` to create readable and reusable Promise chains.
❌ 
```
myPromise.then(function (val) {});
myPromise.then(() => {
  doSomething();
});
myPromise.then((b) => {
  if (b) {
…
```
✅ 
```
myPromise.then((val) => val * 2);
myPromise.then(function (val) {
  return val * 2;
});
myPromise.then(doSomething); // could be either
myPromise.then((b) => {
…
```

### promise/no-callback-in-promise
Do not use calling a callback function (`cb()`) inside a `Promise.prototype.then()` or `Promise.prototype.catch()`.
❌ 
```
function callback(err, data) {
  console.log("Callback got called with:", err, data);
  throw new Error("My error");
}
Promise.resolve()
  .then(() => callback(null, "data"))
…
```
✅ 
```
Promise.resolve()
  .then((data) => {
    console.log(data);
  })
  .catch((err) => {
    console.error(err);
…
```

### promise/no-multiple-resolved
This rule warns of paths that resolve multiple times in executor functions that Promise constructors.
❌ 
```
new Promise((resolve, reject) => {
  fn((error, value) => {
    if (error) {
      reject(error);
    }
    resolve(value); // Both `reject` and `resolve` may be called.
…
```
✅ 
```
new Promise((resolve, reject) => {
  fn((error, value) => {
    if (error) {
      reject(error);
    } else {
      resolve(value);
…
```

### promise/no-new-statics
Do not use calling new on static `Promise` methods.
❌ `const x = new Promise.resolve(value);`
✅ `const x = Promise.resolve(value);`

### promise/no-promise-in-callback
Do not use the use of Promises within error-first callback functions.
❌ 
```
doSomething((err, val) => {
  if (err) console.error(err);
  else doSomethingElse(val).then(console.log);
});
```
✅ `promisify(doSomething)().then(doSomethingElse).then(console.log).catch(console.error);`

### promise/valid-params
Enforce the proper number of arguments are passed to Promise functions.
❌ `Promise.resolve(1, 2);`
✅ `Promise.resolve(1);`

### Plugin: `typescript`

### typescript/no-confusing-non-null-assertion
Do not use non-null assertion in locations that may be confusing.
❌ 
```
a! == b; // a non-null assertions(`!`) and an equals test(`==`)
a !== b; // not equals test(`!==`)
a! === b; // a non-null assertions(`!`) and an triple equals test(`===`)
```
✅ 
```
a == b;
a !== b;
a === b;
```

### typescript/no-duplicate-enum-values
Do not use duplicate enum member values.
❌ 
```
enum E {
  A = 0,
  B = 0,
}
```
✅ 
```
enum E {
  A = 0,
  B = 1,
}
```

### typescript/no-extra-non-null-assertion
Do not use extra non-null assertions.
❌ 
```
const foo: { bar: number } | null = null;
const bar = foo!!!.bar;
```
✅ 
```
const foo: { bar: number } | null = null;
const bar = foo!.bar;
```

### typescript/no-extraneous-class
This rule reports when a class has no non-static members, such as for a class used exclusively as a static namespace.
❌ 
```
class StaticConstants {
  static readonly version = 42;
  static isProduction() {
    return process.env.NODE_ENV === "production";
  }
}
…
```
✅ 
```
const version = 42;
const isProduction = () => process.env.NODE_ENV === "production";
```

### typescript/no-misused-new
Enforce valid definition of new and constructor.
❌ 
```
declare class C {
  new(): C;
}
```
✅ 
```
declare class C {
  constructor();
}
```

### typescript/no-non-null-asserted-optional-chain
Do not use non-null assertions after an optional chain expression.
❌ 
```
foo?.bar!;
foo?.bar()!;
```
✅ 
```
foo?.bar;
foo.bar!;
```

### typescript/no-this-alias
Do not use aliasing of `this`.
❌ 
```
const self = this;
setTimeout(function () {
  self.doWork();
});
```
✅ 
```
setTimeout(() => {
  this.doWork();
});
```

### typescript/no-unnecessary-parameter-property-assignment
Prevent unnecessary assignment of parameter properties.
❌ 
```
class Foo {
  constructor(public name: unknown) {
    this.name = name;
  }
}
```
✅ 
```
class Foo {
  constructor(public name: unknown) {}
}
```

### typescript/no-unnecessary-type-constraint
Do not use unnecessary constraints on generic types.
❌ 
```
interface FooAny<T extends any> {}
interface FooUnknown<T extends unknown> {}
type BarAny<T extends any> = {};
type BarUnknown<T extends unknown> = {};
const QuuxAny = <T extends any>() => {};
function QuuzAny<T extends any>() {}
```
✅ 
```
interface Foo<T> {}
type Bar<T> = {};
const Quux = <T>() => {};
function Quuz<T>() {}
```

### typescript/no-unsafe-declaration-merging
Do not use unsafe declaration merging.
❌ 
```
interface Foo {}
class Foo {}
```
✅ 
```
interface Foo {}
class Bar {}
```

### typescript/no-useless-empty-export
Do not use empty exports that don't change anything in a module file.
❌ 
```
export const value = "Hello, world!";
export {};
```
✅ `export const value = "Hello, world!";`

### typescript/no-wrapper-object-types
Do not use the use of wrapper object types.
❌ 
```
let myBigInt: BigInt;
let myBoolean: Boolean;
let myNumber: Number;
let myString: String;
let mySymbol: Symbol;
let myObject: Object = "allowed by TypeScript";
```
✅ 
```
let myBigint: bigint;
let myBoolean: boolean;
let myNumber: number;
let myString: string;
let mySymbol: symbol;
let myObject: object = "Type 'string' is not assignable to type 'object'.";
```

### typescript/prefer-as-const
Enforce the use of `as const` over literal type.
❌ 
```
let bar: 2 = 2;
let foo = { bar: "baz" as "baz" };
```
✅ 
```
let foo = "bar";
let foo = "bar" as const;
let foo: "bar" = "bar" as const;
let bar = "bar" as string;
let foo = { bar: "baz" };
```

### typescript/prefer-namespace-keyword
This rule reports when the module keyword is used instead of namespace.
❌ `module Example {}`
✅ `namespace Example {}`

### typescript/triple-slash-reference
Do not use certain triple slash directives in favor of ES module import declarations.
❌ 
```
/// <reference lib="code" />
globalThis.value;
```

### Plugin: `unicorn`

### unicorn/consistent-function-scoping
Do not use functions that are declared in a scope which does not capture any variables from the outer scope.
❌ 
```
export function doFoo(foo) {
  // Does not capture anything from the scope, can be moved to the outer scope
  function doBar(bar) {
    return bar === "bar";
  }
  return doBar;
…
```
✅ 
```
function doBar(bar) {
  return bar === "bar";
}
export function doFoo(foo) {
  return doBar;
}
…
```

### unicorn/no-accessor-recursion
Do not use recursive access to `this` within getters and setters.
❌ 
```
const foo = {
  get bar() {
    return this.bar;
  },
};
const baz = {
…
```
✅ 
```
const foo = {
  get bar() {
    return this.qux;
  },
};
const baz = {
…
```

### unicorn/no-array-reverse
Prefer using `Array#toReversed()` over `Array#reverse()`.
❌ `const reversed = [...array].reverse();`
✅ `const reversed = [...array].toReversed();`

### unicorn/no-array-sort
Prefer using `Array#toSorted()` over `Array#sort()`.
❌ `const sorted = [...array].sort();`
✅ `const sorted = [...array].toSorted();`

### unicorn/no-await-in-promise-methods
Do not use using `await` in `Promise` method parameters.
❌ 
```
async function foo() {
  Promise.all([await promise, anotherPromise]);
  Promise.allSettled([await promise, anotherPromise]);
  Promise.any([await promise, anotherPromise]);
  Promise.race([await promise, anotherPromise]);
}
```
✅ 
```
async function foo() {
  Promise.all([promise, anotherPromise]);
  Promise.allSettled([promise, anotherPromise]);
  Promise.any([promise, anotherPromise]);
  Promise.race([promise, anotherPromise]);
}
```

### unicorn/no-empty-file
Do not use files that do not contain any meaningful code.
❌ `````
✅ `const x = 0;`

### unicorn/no-instanceof-builtins
Do not use the use of `instanceof` with ECMAScript built-in constructors because: * it breaks across execution contexts (`iframe`, Web Worker, Node VM, etc.); * it is often misleading (e.g.
❌ 
```
if (arr instanceof Array) { … }
if (el instanceof HTMLElement) { … }
```
✅ 
```
if (Array.isArray(arr)) { … }
if (el?.nodeType === 1) { … }
```

### unicorn/no-invalid-fetch-options
Do not use invalid options in `fetch()` and `new Request()`.
❌ 
```
const response = await fetch("/", { method: "GET", body: "foo=bar" });
const request = new Request("/", { method: "GET", body: "foo=bar" });
```
✅ 
```
const response = await fetch("/", { method: "POST", body: "foo=bar" });
const request = new Request("/", { method: "POST", body: "foo=bar" });
```

### unicorn/no-invalid-remove-event-listener
It warns when you use a non-function value as the second argument of `removeEventListener`.
❌ 
```
el.removeEventListener("click", () => {});
el.removeEventListener("click", function () {});
```
✅ 
```
el.removeEventListener("click", handler);
el.removeEventListener("click", handler.bind(this));
```

### unicorn/no-new-array
Do not use `new Array()`.
❌ 
```
const array = new Array(1);
const array = new Array(42);
const array = new Array(foo);
```
✅ 
```
const array = Array.from({ length: 42 });
const array = [42];
```

### unicorn/no-single-promise-in-promise-methods
Do not use passing single-element arrays to `Promise` methods.
❌ 
```
async function bad() {
  const foo = await Promise.all([promise]);
  const foo = await Promise.any([promise]);
  const foo = await Promise.race([promise]);
  const promise = Promise.all([nonPromise]);
}
```
✅ 
```
async function good() {
  const foo = await promise;
  const promise = Promise.resolve(nonPromise);
  const foo = await Promise.all(promises);
  const foo = await Promise.any([promise, anotherPromise]);
  const [{ value: foo, reason: error }] = await Promise.allSettled([promise]);
…
```

### unicorn/no-thenable
Do not use defining a `then` property.
❌ 
```
async function example() {
  const foo = {
    unicorn: 1,
    then() {},
  };
  const { unicorn } = await foo;
…
```
✅ 
```
async function example() {
  const foo = {
    unicorn: 1,
    bar() {},
  };
  const { unicorn } = await foo;
…
```

### unicorn/no-unnecessary-await
Do not use awaiting on non-promise values.
❌ 
```
async function bad() {
  await await promise;
}
```
✅ 
```
async function bad() {
  await promise;
}
```

### unicorn/no-useless-fallback-in-spread
Do not use useless fallback when spreading in object literals.
❌ `const object = { ...(foo || {}) };`
✅ 
```
const object = { ...foo };
const object = { ...(foo || { not: "empty" }) };
```

### unicorn/no-useless-length-check
It checks for an unnecessary array length check in a logical expression.
❌ 
```
if (array.length === 0 || array.every(Boolean)) {
  // do something!
}
```
✅ 
```
if (array.every(Boolean)) {
  // do something!
}
```

### unicorn/no-useless-spread
Do not use using spread syntax in following, unnecessary cases: * Spread an array literal as elements of an array literal * Spread an array literal as arguments of a call or a `new` call * Spread an object literal as properties of an object…
❌ 
```
const array = [firstElement, ...[secondElement], thirdElement];
await Promise.all([...iterable]);
for (const foo of [...set]);
function* foo() {
  yield* [...anotherGenerator()];
}
…
```
✅ 
```
const array = [firstElement, secondElement, thirdElement];
await Promise.all(iterable);
for (const foo of set);
function* foo() {
  yield* anotherGenerator();
}
…
```

### unicorn/prefer-add-event-listener
Enforce the use of `.addEventListener()` and `.removeEventListener()` over their `on`-function counterparts.
❌ `foo.onclick = () => {};`
✅ `foo.addEventListener("click", () => {});`

### unicorn/prefer-set-size
Prefer `Set#size` over `Set#length` when the `Set` is converted to an array.
❌ `const length = [...new Set([1, 2, 3])].length;`
✅ `const size = new Set([1, 2, 3]).size;`

### unicorn/prefer-string-starts-ends-with
Prefer `String#startsWith()` and `String#endsWith()` over using a regex with `/^foo/` or `/foo$/`.
❌ 
```
const foo = "hello";
/^abc/.test(foo);
```
✅ 
```
const foo = "hello";
foo.startsWith("abc");
```

### unicorn/require-module-specifiers
Enforce non-empty specifier list in `import` and `export` statements.
❌ 
```
import {} from "foo";
import foo from "foo";
export {} from "foo";
export {};
```
✅ 
```
import "foo";
import foo from "foo";
```

### unicorn/require-post-message-target-origin
Enforce using the `targetOrigin` argument with `window.postMessage()`.
❌ `window.postMessage(message);`
✅ 
```
window.postMessage(message, "https://example.com");
window.postMessage(message, "*");
```


## Tier 2 — Modernization & Performance
*78 rules*

### Plugin: `eslint`

### eslint/class-methods-use-this
Enforce that class methods utilize `this`.
❌ 
```
class A {
  foo() {
    console.log("Hello World");
  }
}
```
✅ 
```
class A {
  foo() {
    this.bar = "Hello World"; // OK, this is used
  }
}
class B {
…
```

### eslint/complexity
Enforce a maximum cyclomatic complexity in a program, which is the number of linearly independent paths in a program.
❌ 
```
function foo() {
  if (foo1) {
    return x1; // 1st path
  } else if (foo2) {
    return x2; // 2nd path
  } else {
…
```
✅ 
```
// This example is taken directly from ESLint documentation
function foo() {
  // this function has complexity = 1
  class C {
    x = a + b; // this initializer has complexity = 1
    y = c || d; // this initializer has complexity = 2
…
```

### eslint/default-case
Enforce that all `switch` statements include a `default` case, unless explicitly marked with a configured comment.
❌ 
```
switch (foo) {
  case 1:
    break;
}
```
✅ 
```
switch (a) {
  case 1:
    break;
  default:
    break;
}
…
```

### eslint/no-alert
Do not use the use of `alert`, `confirm`, and `prompt`.
❌ 
```
alert("here!");
confirm("Are you sure?");
prompt("What's your name?", "John Doe");
```
✅ 
```
customAlert("Something happened!");
customConfirm("Are you sure?");
customPrompt("Who are you?");
function foo() {
  var alert = myCustomLib.customAlert;
  alert();
…
```

### eslint/no-await-in-loop
This rule disallows the use of `await` within loop bodies.
❌ 
```
async function bad() {
  for (const user of users) {
    const userRecord = await getUserRecord(user);
  }
}
```
✅ 
```
async function good() {
  await Promise.all(users.map((user) => getUserRecord(user)));
}
```

### eslint/no-bitwise
Do not use bitwise operators.
❌ `var x = y | z;`
✅ `var x = y || z;`

### eslint/no-console
Do not use the use of console.
❌ 
```
console.log("Log a debug level message.");
console.warn("Log a warn level message.");
console.error("Log an error level message.");
console.log = foo();
```
✅ 
```
// custom console
Console.log("Hello world!");
```

### eslint/no-div-regex
Do not use equal signs explicitly at the beginning of regular expressions.
❌ 
```
function bar() {
  return /=foo/;
}
```
✅ 
```
function bar() {
  return /[=]foo/;
}
```

### eslint/no-empty
Do not use empty block statements.
❌ 
```
if (condition) {
}
```
✅ 
```
if (condition) {
  throw new Error("condition should be false");
}
```

### eslint/no-empty-function
Do not use the usage of empty functions.
❌ 
```
function foo() {}
const bar = () => {};
class Foo {
  constructor();
  someMethod() {}
  set bar(value) {}
…
```
✅ 
```
function foo() {
  // do nothing
}
function foo() {
  return;
}
…
```

### eslint/no-eq-null
Do not use `null` comparisons without type-checking operators.
❌ 
```
if (foo == null) {
  bar();
}
if (baz != null) {
  bar();
}
```
✅ 
```
if (foo === null) {
  bar();
}
if (baz !== null) {
  bar();
}
…
```

### eslint/no-param-reassign
Do not use reassigning function parameters or, optionally, their properties.

### eslint/no-plusplus
Do not use the unary operators `++` and `--`.
❌ 
```
var x = 0;
x++;
var y = 0;
y--;
for (let i = 0; i < l; i++) {
  doSomething(i);
…
```
✅ 
```
var x = 0;
x += 1;
var y = 0;
y -= 1;
for (let i = 0; i < l; i += 1) {
  doSomething(i);
…
```

### eslint/no-proto
Do not use the use of the `__proto__` property.
❌ 
```
var a = obj.__proto__;
var a = obj["__proto__"];
obj.__proto__ = b;
obj["__proto__"] = b;
```

### eslint/no-regex-spaces
Do not use 2+ consecutive spaces in regular expressions.
❌ `var re = /foo   bar/;`

### eslint/no-restricted-globals
This rule allows you to specify global variable names that you don't want to use in your application.

### eslint/no-restricted-imports
This rule allows you to specify imports that you don’t want to use in your application.
❌ 
```
/* no-restricted-imports: ["error", "disallowed-import"] */
import foo from "disallowed-import";
export * from "disallowed-import";
```
✅ 
```
/* no-restricted-imports: ["error", "fs"] */
import crypto from "crypto";
export * from "bar";
```

### eslint/no-sequences
Do not use the use of the comma operator.
❌ 
```
((foo = doSomething()), val);
(0, eval("doSomething();"));
// Arrow function body needs double parentheses
const fn = () => (doSomething(), val);
// with allowInParentheses: false
foo = (doSomething(), val);
```
✅ 
```
foo = (doSomething(), val);
(0, eval)("doSomething();");
// Single extra parentheses is enough for conditions
do {} while ((doSomething(), !!test));
for (i = 0, j = 10; i < j; i++, j--) {}
// Arrow function body needs double parentheses
…
```

### eslint/no-undefined
Do not use the use of `undefined` as an identifier.
❌ 
```
var foo = undefined;
var undefined = "foo";
if (foo === undefined) {
  // ...
}
function baz(undefined) {
…
```
✅ 
```
var foo = void 0;
var Undefined = "foo";
if (typeof foo === "undefined") {
  // ...
}
global.undefined = "foo";
…
```

### eslint/no-use-before-define
Do not use using variables before they are defined.
❌ 
```
new A();
var A = class {};
```
✅ 
```
var A = class {};
new A();
```

### eslint/no-useless-call
Do not use unnecessary calls to `.call()` and `.apply()`
❌ 
```
// These are the same as `foo(1, 2, 3);`
foo.call(undefined, 1, 2, 3);
foo.apply(undefined, [1, 2, 3]);
foo.call(null, 1, 2, 3);
foo.apply(null, [1, 2, 3]);
// These are the same as `obj.foo(1, 2, 3);`
…
```
✅ 
```
// The `this` binding is different.
foo.call(obj, 1, 2, 3);
foo.apply(obj, [1, 2, 3]);
obj.foo.call(null, 1, 2, 3);
obj.foo.apply(null, [1, 2, 3]);
obj.foo.call(otherObj, 1, 2, 3);
…
```

### eslint/no-var
ECMAScript 2015 allows programmers to create variables with block scope instead of function scope using the `let` and `const` keywords.
❌ 
```
var x = "y";
var CONFIG = {};
```
✅ 
```
let x = "y";
const CONFIG = {};
```

### eslint/no-void
Do not use the use of the `void` operator.
❌ 
```
void 0;
var foo = void 0;
```
✅ 
```
"var foo = bar()";
"foo.void()";
"foo.void = bar";
```

### eslint/unicode-bom
Require or disallow Unicode byte order mark (BOM)
❌ `var a = 123;`

### Plugin: `import`

### import/extensions
Some file resolve algorithms allow you to omit the file extension within the import source path.

### import/no-amd
Do not use the use of AMD `require` and `define` calls.
❌ `require([a, b], function () {});`
✅ 
```
require("../name");
require(`../name`);
```

### import/no-commonjs
Do not use the use of CommonJS `require` calls.
❌ 
```
var mod = require("fs");
var exports = (module.exports = {});
exports.sayHello = function () {
  return "Hello";
};
module.exports = "Hola";
```
✅ 
```
var a = b && require("c");
if (typeof window !== "undefined") {
  require("somelib");
}
var fs = null;
try {
…
```

### import/no-cycle
Ensures that there is no resolvable path back to this module via its dependencies.
❌ 
```
// dep-b.js
import "./dep-a.js";
export function b() {
  /* ... */
}
```
✅ 
```
// dep-b.js
export function b() {
  /* ... */
}
```

### import/no-default-export
Do not use a module from having default exports.
❌ 
```
export default 'bar';
const foo = 'foo';
export { foo as default }
```
✅ 
```
export const foo = "foo";
export const bar = "bar";
```

### import/no-dynamic-require
Do not use imports that use an expression for the module argument.
❌ 
```
require(name);
require(`../${name}`);
```
✅ 
```
require("../name");
require(`../name`);
```

### import/no-relative-parent-imports
Do not use importing modules from parent directories using relative paths.
❌ 
```
import foo from "../bar";
import foo from "../../utils/helper";
const baz = require("../config");
export { qux } from "../shared";
```
✅ 
```
import foo from "lodash";
import a from "./lib/a";
import b from "./b";
```

### import/no-webpack-loader-syntax
Do not use using Webpack loader syntax directly in import or require statements.
❌ 
```
import myModule from "my-loader!my-module";
import theme from "style!css!./theme.css";
var myModule = require("my-loader!./my-module");
var theme = require("style!css!./theme.css");
```
✅ 
```
import myModule from "./my-module";
import theme from "./theme.css";
var myModule = require("./my-module");
var theme = require("./theme.css");
```

### import/unambiguous
Warn if a `module` could be mistakenly parsed as a `script` instead of as a pure ES module.
❌ 
```
function x() {}
(function x() {
  return 42;
})();
```
✅ 
```
import "foo";
function x() {
  return 42;
}
export function x() {
  return 42;
…
```

### Plugin: `node`

### node/handle-callback-err
This rule expects that when you're using the callback pattern in Node.js you'll handle the error.
❌ 
```
function loadData(err, data) {
  doSomething();
}
```
✅ 
```
function loadData(err, data) {
  if (err) {
    console.log(err.stack);
  }
  doSomething();
}
…
```

### node/no-new-require
Avoid calling `new` on `require`.
❌ `var appHeader = new require("app-header");`
✅ 
```
var AppHeader = require("app-header");
var appHeader = new AppHeader();
```

### node/no-path-concat
Do not use string concatenation with `__dirname` and `__filename`.
❌ 
```
const fullPath1 = __dirname + "/foo.js";
const fullPath2 = __filename + "/foo.js";
const fullPath3 = `${__dirname}/foo.js`;
const fullPath4 = `${__filename}/foo.js`;
```
✅ 
```
const fullPath1 = path.join(__dirname, "foo.js");
const fullPath2 = path.join(__filename, "foo.js");
const fullPath3 = __dirname + ".js";
const fullPath4 = __filename + ".map";
const fullPath5 = `${__dirname}_foo.js`;
const fullPath6 = `${__filename}.test.js`;
```

### node/no-process-env
Do not use use of `process.env`.
❌ 
```
if (process.env.NODE_ENV === "development") {
  // ...
}
```
✅ 
```
import config from "./config";
if (config.env === "development") {
  //...
}
```

### Plugin: `oxc`

### oxc/bad-bitwise-operator
This rule applies when bitwise operators are used where logical operators are expected.
❌ 
```
if (obj & obj.prop) {
  console.log(obj.prop);
}
options = options | {};
input |= "";
```
✅ 
```
if (obj && obj.prop) {
  console.log(obj.prop);
}
options = options || {};
input ||= "";
```

### oxc/no-accumulating-spread
Prevent using object or array spreads on accumulators in `Array.prototype.reduce()` and in loops.
❌ 
```
arr.reduce((acc, x) => ({ ...acc, [x]: fn(x) }), {});
Object.keys(obj).reduce((acc, el) => ({ ...acc, [el]: fn(el) }), {});
let foo = [];
for (let i = 0; i < 10; i++) {
  foo = [...foo, i];
}
```
✅ 
```
function fn(x) {
  // ...
}
arr.reduce((acc, x) => acc.push(fn(x)), []);
Object.keys(obj).reduce((acc, el) => {
  acc[el] = fn(el);
…
```

### oxc/no-async-await
Do not use the use of `async`/`await`.
❌ 
```
async function foo() {
  await bar();
  return baz();
}
```

### oxc/no-barrel-file
Do not use the use of barrel files where the file contains `export *` statements, and the total number of modules exceed a threshold.

### oxc/no-const-enum
Do not use TypeScript `const enum`
❌ 
```
const enum Color {
  Red,
  Green,
  Blue,
}
```

### oxc/no-map-spread
Do not use the use of object or array spreads in `Array.prototype.map` and `Array.prototype.flatMap` to add properties/elements to array items.
❌ 
```
const arr = [{ a: 1 }, { a: 2 }, { a: 3 }];
const arr2 = arr.map((obj) => ({ ...obj, b: obj.a * 2 }));
```
✅ 
```
const arr = [{ a: 1 }, { a: 2 }, { a: 3 }];
arr.map((obj) => Object.assign(obj, { b: obj.a * 2 }));
// instance properties are ignored
class UsersDb {
  #users = [];
  public get users() {
…
```

### oxc/no-optional-chaining
Do not use optional chaining.
❌ 
```
const foo = obj?.foo;
obj.fn?.();
```

### oxc/no-rest-spread-properties
Do not use Object Rest/Spread Properties.
❌ 
```
let { x, ...y } = z;
let z = { x, ...y };
```

### Plugin: `promise`

### promise/catch-or-return
Ensure that each time a `then()` is applied to a promise, a `catch()` must be applied as well.
❌ 
```
myPromise.then(doSomething);
myPromise.then(doSomething, catchErrors); // catch() may be a little better
```
✅ 
```
myPromise.then(doSomething).catch(errors);
function doSomethingElse() {
  return myPromise.then(doSomething);
}
const arrowFunc = () => myPromise.then(doSomething);
```

### promise/spec-only
Do not use use of non-standard Promise static methods.
❌ `Promise.done();`
✅ `Promise.resolve();`

### Plugin: `typescript`

### typescript/explicit-function-return-type
This rule enforces that functions have an explicit return type annotation.
❌ 
```
// Should indicate that no value is returned (void)
function test() {
  return;
}
// Should indicate that a number is returned
var fn = function () {
…
```
✅ 
```
// No return value should be expected (void)
function test(): void {
  return;
}
// A return value of type number
var fn = function (): number {
…
```

### typescript/explicit-member-accessibility
Require explicit accessibility modifiers on class properties and methods.

### typescript/explicit-module-boundary-types
Require explicit return and argument types on exported functions' and classes' public class methods.
❌ 
```
// Should indicate that no value is returned (void)
export function test() {
  return;
}
// Should indicate that a string is returned
export var arrowFn = () => "test";
…
```
✅ 
```
// A function with no return value (void)
export function test(): void {
  return;
}
// A return value of type string
export var arrowFn = (): string => "test";
…
```

### typescript/no-dynamic-delete
Do not use using the delete operator on computed key expressions.
❌ 
```
const container: { [i: string]: 0 } = {};
delete container["aa" + "b"];
```
✅ 
```
const container: { [i: string]: 0 } = {};
delete container.aab;
```

### typescript/no-empty-object-type
To avoid confusion around the `{}` type allowing any non-nullish value, this rule bans usage of the `{}` type.
❌ 
```
let anyObject: {};
let anyValue: {};
interface AnyObjectA {}
interface AnyValueA {}
type AnyObjectB = {};
type AnyValueB = {};
```
✅ 
```
let anyObject: object;
let anyValue: unknown;
type AnyObjectA = object;
type AnyValueA = unknown;
type AnyObjectB = object;
type AnyValueB = unknown;
…
```

### typescript/no-explicit-any
Do not use explicit use of the `any` type.
❌ 
```
const age: any = "seventeen";
const ages: any[] = ["seventeen"];
const ages: Array<any> = ["seventeen"];
function greet(): any {}
function greet(): any[] {}
function greet(): Array<any> {}
…
```
✅ 
```
const age: number = 17;
const ages: number[] = [17];
const ages: Array<number> = [17];
function greet(): string {}
function greet(): string[] {}
function greet(): Array<string> {}
…
```

### typescript/no-import-type-side-effects
Enforce the use of top-level `import type` qualifier when an import only has specifiers with inline type qualifiers.
❌ 
```
import { type A } from "mod";
import { type A as AA } from "mod";
import { type A, type B } from "mod";
import { type A as AA, type B as BB } from "mod";
```
✅ 
```
import type { A } from "mod";
import type { A as AA } from "mod";
import type { A, B } from "mod";
import type { A as AA, B as BB } from "mod";
```

### typescript/no-invalid-void-type
Do not use `void` type usage outside return types and configured generic contexts.
❌ 
```
function takeVoid(arg: void) {}
type Alias = void;
type Union = string | void;
```
✅ 
```
function f(): void {}
type P = Promise<void>;
type U = void | never;
```

### typescript/no-namespace
Do not use TypeScript namespaces.
❌ 
```
module foo {}
namespace foo {}
declare module foo {}
declare namespace foo {}
```
✅ 
```
declare module "foo" {}
// anything inside a d.ts file
```

### typescript/no-non-null-asserted-nullish-coalescing
Do not use non-null assertions in the left operand of a nullish coalescing operator.
❌ 
```
foo! ?? bar;
foo.bazz! ?? bar;
foo!.bazz! ?? bar;
foo()! ?? bar;
let x!: string;
x! ?? "";
…
```
✅ 
```
foo ?? bar;
foo ?? bar!;
foo!.bazz ?? bar;
foo!.bazz ?? bar!;
foo() ?? bar;
```

### typescript/no-non-null-assertion
Do not use non-null assertions using the `!` postfix operator.
❌ 
```
x!;
x!.y;
x.y!;
```
✅ 
```
x;
x?.y;
x.y;
```

### typescript/no-require-imports
Do not use the use of CommonJS `require` calls.
❌ 
```
const lib1 = require("lib1");
const { lib2 } = require("lib2");
import lib3 = require("lib3");
```
✅ 
```
import * as lib1 from "lib1";
import { lib2 } from "lib2";
import * as lib3 from "lib3";
```

### typescript/no-restricted-types
Do not use certain types from being used.
❌ `let value: Foo;`
✅ `let value: Bar;`

### typescript/no-var-requires
Do not use `require` statements except in import statements.

### typescript/prefer-literal-enum-member
Explicit enum value must only be a literal value (string, number, boolean, etc).
❌ 
```
const imOutside = 2;
const b = 2;
enum Foo {
  outer = imOutside,
  a = 1,
  b = a,
…
```

### Plugin: `unicorn`

### unicorn/no-abusive-eslint-disable
Do not use `oxlint-disable` or `eslint-disable` comments without specifying rules.
❌ 
```
/* eslint-disable */
console.log(message);
console.log(message); // eslint-disable-line
// eslint-disable-next-line
console.log(message);
```
✅ 
```
/* eslint-disable no-console */
console.log(message);
console.log(message); // eslint-disable-line no-console
// eslint-disable-next-line no-console
console.log(message);
```

### unicorn/no-anonymous-default-export
Do not use anonymous functions and classes as default exports.
❌ 
```
export default class {}
export default function () {}
export default () => {};
module.exports = class {};
module.exports = function () {};
module.exports = () => {};
```
✅ 
```
export default class Foo {}
export default function foo () {}
const foo = () => {};
export default foo;
module.exports = class Foo {};
module.exports = function foo () {};
…
```

### unicorn/no-array-for-each
Do not use the use of `Array#forEach` in favor of a for loop.
❌ 
```
const foo = [1, 2, 3];
foo.forEach((element) => {
  /* ... */
});
```
✅ 
```
const foo = [1, 2, 3];
for (const element of foo) {
  /* ... */
}
```

### unicorn/no-array-reduce
Do not use `Array#reduce()` and `Array#reduceRight()`.
❌ 
```
array.reduce(reducer, initialValue);
array.reduceRight(reducer, initialValue);
```

### unicorn/no-document-cookie
Do not use direct use of `document.cookie`.
❌ 
```
document.cookie =
  "foo=bar" +
  "; Path=/" +
  "; Domain=example.com" +
  "; expires=Fri, 31 Dec 9999 23:59:59 GMT" +
  "; Secure";
```
✅ 
```
async function storeCookies() {
  await cookieStore.set({
    name: "foo",
    value: "bar",
    expires: Date.now() + 24 * 60 * 60 * 1000,
    domain: "example.com",
…
```

### unicorn/no-length-as-slice-end
Do not use using `length` as the end argument of a `slice` call.
❌ `foo.slice(1, foo.length);`
✅ `foo.slice(1);`

### unicorn/no-magic-array-flat-depth
Do not use magic numbers for `Array.prototype.flat` depth.
❌ 
```
array.flat(2);
array.flat(20);
```
✅ 
```
array.flat(2 /* explanation */);
array.flat(1);
array.flat();
array.flat(Infinity);
```

### unicorn/no-process-exit
Do not use all usage of `process.exit()`.
❌ 
```
if (problem) {
  process.exit(1);
}
```
✅ 
```
if (problem) {
  throw new Error("message");
}
```

### unicorn/no-useless-error-capture-stack-trace
Do not use unnecessary `Error.captureStackTrace(…)` in error constructors.
❌ 
```
class MyError extends Error {
  constructor() {
    Error.captureStackTrace(this, MyError);
  }
}
```
✅ 
```
class MyError extends Error {
  constructor() {
    // No need to call Error.captureStackTrace
  }
}
```

### unicorn/prefer-array-find
Encourages using `Array.prototype.find` instead of `filter(...)[0]` or similar patterns when only the first matching element is needed.
❌ 
```
const match = users.filter((u) => u.id === id)[0];
const match = users.filter(fn).shift();
```
✅ 
```
const match = users.find((u) => u.id === id);
const match = users.find(fn);
```

### unicorn/prefer-array-flat-map
Prefer the use of `.flatMap()` when `map().flat()` are used together.
❌ `const bar = [1, 2, 3].map((i) => [i]).flat();`
✅ `const bar = [1, 2, 3].flatMap((i) => [i]);`

### unicorn/prefer-modern-math-apis
Avoid usage of legacy patterns for mathematical operations.
❌ 
```
Math.log(x) * Math.LOG10E;
Math.sqrt(a * a + b * b);
```
✅ 
```
Math.log10(x);
Math.hypot(a, b);
```

### unicorn/prefer-module
Prefer JavaScript modules (ESM) over CommonJS.
❌ 
```
"use strict";
const foo = require("foo");
module.exports = foo;
```
✅ 
```
import foo from "foo";
export default foo;
```

### unicorn/prefer-node-protocol
Prefer using the `node:protocol` when importing Node.js builtin modules.
❌ `import fs from "fs";`
✅ `import fs from "node:fs";`

### unicorn/prefer-number-properties
Do not use use of `parseInt()`, `parseFloat()`, `isNan()`, `isFinite()`, `Nan`, `Infinity` and `-Infinity` as global variables.
❌ 
```
const foo = parseInt("10", 2);
const bar = parseFloat("10.5");
```
✅ 
```
const foo = Number.parseInt("10", 2);
const bar = Number.parseFloat("10.5");
```

### unicorn/prefer-set-has
Prefer `Set#has()` over `Array#includes()` when checking for existence or non-existence.
❌ 
```
const array = [1, 2, 3];
const hasValue = (value) => array.includes(value);
```
✅ 
```
const set = new Set([1, 2, 3]);
const hasValue = (value) => set.has(value);
```
