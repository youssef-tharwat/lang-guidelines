# TypeScript & JavaScript Style & Pedantic Rules

280 opinionated style rules. Load this file only when:

- Reviewing existing code, or
- Matching an explicit project style guide, or
- The project has a lint config pinning these.

Do **not** load preemptively when writing new code.

---

## Plugin: `eslint`

### eslint/accessor-pairs
Enforce getter/setter pairs in objects and classes.
❌ 
```
var o = {
  set a(value) {
    this.val = value;
  },
};
class C {
…
```
✅ 
```
var o = {
  set a(value) {
    this.val = value;
  },
  get a() {
    return this.val;
…
```

### eslint/array-callback-return
Enforce return statements in callbacks of array methods.
❌ 
```
let foo = [1, 2, 3, 4];
foo.map((a) => {
  console.log(a);
});
```
✅ 
```
let foo = [1, 2, 3, 4];
foo.map((a) => {
  console.log(a);
  return a;
});
```

### eslint/arrow-body-style
This rule can enforce or disallow the use of braces around arrow function body.

### eslint/capitalized-comments
Enforce or disallows capitalization of the first letter of a comment.
❌ 
```
// lowercase comment
/* lowercase block comment */
```
✅ 
```
// Capitalized comment
/* Capitalized block comment */
// 123 - comments starting with non-letters are ignored
```

### eslint/curly
This rule enforces the use of curly braces `{}` for all control statements (`if`, `else`, `for`, `while`, `do`, `with`).

### eslint/default-case-last
Require the `default` clause in `switch` statements to be the last one.
❌ 
```
/* default-case-last: "error" */
switch (foo) {
  default:
    bar();
    break;
  case "a":
…
```
✅ 
```
/* default-case-last: "error" */
switch (foo) {
  case 1:
    bar();
    break;
  case 2:
…
```

### eslint/default-param-last
Require default parameters in functions to be the last ones.
❌ 
```
/* default-param-last: "error" */
function f(a = 0, b) {}
function f(a, b = 0, c) {}
function createUser(isAdmin = false, id) {}
createUser(undefined, "tabby");
```
✅ 
```
/* default-param-last: "error" */
function f(a, b = 0) {}
function f(a = 0, b = 0) {}
function createUser(id, isAdmin = false) {}
createUser("tabby");
```

### eslint/eqeqeq
Require the use of the `===` and `!==` operators, disallowing the use of `==` and `!=`.

### eslint/func-names
Require or disallow named function expressions.
❌ 
```
/* func-names: ["error", "always"] */
Foo.prototype.bar = function () {};
const cat = { meow: function () {} };
(function () {
  /* ... */
})();
…
```
✅ 
```
/* func-names: ["error", "always"] */
Foo.prototype.bar = function bar() {};
const cat = { meow() {} };
(function bar() {
  /* ... */
})();
…
```

### eslint/func-style
Enforce the consistent use of either function declarations or expressions assigned to variables.
❌ 
```
/* func-style: ["error", "expression"] */
function foo() {
  // ...
}
```
✅ 
```
/* func-style: ["error", "expression"] */
var foo = function () {
  // ...
};
```

### eslint/getter-return
Require all getters to have a `return` statement.
❌ 
```
class Person {
  get name() {
    // no return
  }
}
const obj = {
…
```
✅ 
```
class Person {
  get name() {
    return this._name;
  }
}
```

### eslint/grouped-accessor-pairs
Require grouped accessor pairs in object literals and classes.
❌ 
```
const foo = {
  get a() {
    return this.val;
  },
  b: 1,
  set a(value) {
…
```
✅ 
```
const foo = {
  get a() {
    return this.val;
  },
  set a(value) {
    this.val = value;
…
```

### eslint/guard-for-in
Require for-in loops to include an if statement.
❌ 
```
for (key in foo) {
  doSomething(key);
}
```
✅ 
```
for (key in foo) {
  if (Object.hasOwn(foo, key)) {
    doSomething(key);
  }
}
```

### eslint/id-length
This rule enforces a minimum and/or maximum identifier length convention by counting the graphemes for a given identifier.
❌ 
```
/* id-length: "error" */ // default is minimum 2-chars ({ "min": 2 })
const x = 5;
obj.e = document.body;
const foo = function (e) {};
try {
  dangerousStuff();
…
```
✅ 
```
/* id-length: "error" */ // default is minimum 2-chars ({ "min": 2 })
const num = 5;
function _f() {
  return 42;
}
function _func() {
…
```

### eslint/init-declarations
Require or disallow initialization in variable declarations.

### eslint/max-classes-per-file
Enforce a maximum number of classes per file.
❌ 
```
class Foo {}
class Bar {}
```
✅ 
```
function foo() {
  var bar = 1;
  let baz = 2;
  const qux = 3;
}
```

### eslint/max-depth
Enforce a maximum depth that blocks can be nested.
❌ 
```
function foo() {
  for (;;) { // Nested 1 deep
    while (true) { // Nested 2 deep
      if (true) { // Nested 3 deep
        if (true) { // Nested 4 deep }
      }
…
```
✅ 
```
function foo() {
  for (;;) { // Nested 1 deep
    while (true) { // Nested 2 deep
      if (true) { // Nested 3 deep }
    }
  }
…
```

### eslint/max-lines
Enforce a maximum number of lines per file.

### eslint/max-lines-per-function
Enforce a maximum number of lines of code in a function.
❌ 
```
/* { "eslint/max-lines-per-function": ["error", 2] } */
function foo() {
  const x = 0;
}
/* { "eslint/max-lines-per-function": ["error", 4] } */
function foo() {
…
```
✅ 
```
/* { "eslint/max-lines-per-function": ["error", 3] } */
function foo() {
  const x = 0;
}
/* { "eslint/max-lines-per-function": ["error", 5] } */
function foo() {
…
```

### eslint/max-nested-callbacks
Enforce a maximum depth that callbacks can be nested.
❌ 
```
foo1(function () {
  foo2(function () {
    foo3(function () {
      foo4(function () {
        // ...
      });
…
```
✅ 
```
foo1(handleFoo1);
function handleFoo1() {
  foo2(handleFoo2);
}
function handleFoo2() {
  foo3(handleFoo3);
…
```

### eslint/max-params
Enforce a maximum number of parameters in function definitions which by default is three.
❌ 
```
function foo(bar, baz, qux, qxx) {
  doSomething();
}
```
✅ 
```
function foo(bar, baz, qux) {
  doSomething();
}
```

### eslint/max-statements
Enforce a maximum number of statements in a function.
❌ 
```
function foo() {
  const foo1 = 1;
  const foo2 = 2;
  const foo3 = 3;
  const foo4 = 4;
  const foo5 = 5;
…
```
✅ 
```
function foo() {
  const foo1 = 1;
  const foo2 = 2;
  const foo3 = 3;
  const foo4 = 4;
  const foo5 = 5;
…
```

### eslint/new-cap
This rule requires constructor names to begin with a capital letter.
❌ 
```
function foo(arg) {
  return Boolean(arg);
}
```
✅ 
```
/* new-cap: ["error", { "newIsCap": true }] */
var friend = new Person();
```

### eslint/no-array-constructor
Do not use creating arrays with the `Array` constructor.
❌ `let arr = new Array();`
✅ 
```
let arr = [];
let arr2 = Array.from(iterable);
let arr3 = new Array(9);
```

### eslint/no-case-declarations
Do not use lexical declarations in case clauses.
❌ 
```
switch (foo) {
  case 1:
    let x = 1;
    break;
  case 2:
    const y = 2;
…
```
✅ 
```
switch (foo) {
  case 1: {
    let x = 1;
    break;
  }
  case 2: {
…
```

### eslint/no-constructor-return
Do not use returning value from constructor.
❌ 
```
class C {
  constructor() {
    return 42;
  }
}
```
✅ 
```
class C {
  constructor() {
    this.value = 42;
  }
}
```

### eslint/no-continue
Do not use `continue` statements.
❌ 
```
var sum = 0,
  i;
for (i = 0; i < 10; i++) {
  if (i >= 5) {
    continue;
  }
…
```
✅ 
```
var sum = 0,
  i;
for (i = 0; i < 10; i++) {
  if (i < 5) {
    sum += i;
  }
…
```

### eslint/no-duplicate-imports
Do not use duplicate module imports.
✅ 
```
import { merge, find } from "module";
import something from "another-module";
```

### eslint/no-else-return
Do not use `else` blocks after `return` statements in `if` statements.

### eslint/no-extra-label
Do not use unnecessary labels.
❌ 
```
A: while (a) {
  break A;
}
B: for (let i = 0; i < 10; ++i) {
  break B;
}
…
```
✅ 
```
while (a) {
  break;
}
for (let i = 0; i < 10; ++i) {
  break;
}
…
```

### eslint/no-fallthrough
Do not use fallthrough of `case` statements This rule is aimed at eliminating unintentional fallthrough of one case to the other.
❌ 
```
switch (foo) {
  case 1:
    doSomething();
  case 2:
    doSomething();
}
```
✅ 
```
switch (foo) {
  case 1:
    doSomething();
    break;
  case 2:
    doSomething();
…
```

### eslint/no-implicit-coercion
Do not use shorthand type conversions using operators like `!!`, `+`, `""+ `, etc.
❌ 
```
var b = !!foo;
var n = +foo;
var s = "" + foo;
```
✅ 
```
var b = Boolean(foo);
var n = Number(foo);
var s = String(foo);
```

### eslint/no-inline-comments
Do not use comments on the same line as code.
❌ 
```
var a = 1; // inline comment
var b = 2; /* another inline comment */
```
✅ 
```
// comment on its own line
var a = 1;
/* block comment on its own line */
var b = 2;
```

### eslint/no-inner-declarations
Do not use variable or function declarations in nested blocks.
❌ 
```
if (test) {
  function doSomethingElse() {}
}
```
✅ 
```
function doSomethingElse() {}
if (test) {
  // your code here
}
```

### eslint/no-label-var
Do not use labels that share a name with a variable.
❌ 
```
var x = foo;
function bar() {
  x: for (;;) {
    break x;
  }
}
```
✅ 
```
// The variable that has the same name as the label is not in scope.
function foo() {
  var q = t;
}
function bar() {
  q: for (;;) {
…
```

### eslint/no-labels
Do not use labeled statements.
❌ 
```
label: while (true) {
  // ...
}
label: while (true) {
  break label;
}
…
```
✅ 
```
var f = {
  label: "foo",
};
while (true) {
  break;
}
…
```

### eslint/no-lone-blocks
Do not use unnecessary standalone block statements.
❌ 
```
{
  var x = 1;
}
```
✅ 
```
if (condition) {
  var x = 1;
}
{
  let x = 1; // Used to create a valid block scope.
}
```

### eslint/no-lonely-if
Do not use `if` statements as the only statement in `else` blocks.
❌ 
```
if (condition) {
  // ...
} else {
  if (anotherCondition) {
    // ...
  }
…
```
✅ 
```
if (condition) {
  // ...
} else if (anotherCondition) {
  // ...
}
```

### eslint/no-loop-func
Do not use function declarations and expressions inside loop statements when they reference variables declared in the outer scope that may change across iterations.
❌ 
```
for (var i = 0; i < 10; i++) {
  funcs[i] = function () {
    return i;
  };
}
```
✅ 
```
for (let i = 0; i < 10; i++) {
  funcs[i] = function () {
    return i;
  };
}
```

### eslint/no-magic-numbers
This rule aims to make code more readable and refactoring easier by ensuring that special numbers are declared as constants to make their meaning explicit.
❌ 
```
var dutyFreePrice = 100;
var finalPrice = dutyFreePrice + dutyFreePrice * 0.25;
```
✅ 
```
/*typescript no-magic-numbers: ["error", { "ignore": [1] }]*/
var data = ["foo", "bar", "baz"];
var dataLast = data.length && data[data.length - 1];
```

### eslint/no-multi-assign
Do not use use of chained assignment expressions.
❌ 
```
var a = (b = c = 5);
const foo = (bar = "baz");
let d = (e = f);
class Foo {
  a = (b = 10);
}
…
```
✅ 
```
var a = 5;
var b = 5;
var c = 5;
const foo = "baz";
const bar = "baz";
let d = c;
…
```

### eslint/no-multi-str
Do not use multiline strings.
❌ 
```
var x =
  "Line 1 \
 Line 2";
```

### eslint/no-negated-condition
Do not use negated conditions.
❌ 
```
if (!a) {
  doSomethingC();
} else {
  doSomethingB();
}
!a ? doSomethingC() : doSomethingB();
```
✅ 
```
if (a) {
  doSomethingB();
} else {
  doSomethingC();
}
a ? doSomethingB() : doSomethingC();
```

### eslint/no-nested-ternary
Do not use nested ternary expressions to improve code readability and maintainability.
❌ `const result = condition1 ? (condition2 ? "a" : "b") : "c";`
✅ 
```
let result;
if (condition1) {
  result = condition2 ? "a" : "b";
} else {
  result = "c";
}
```

### eslint/no-new-func
The rule disallow `new` operators with the `Function` object.
❌ 
```
var x = new Function("a", "b", "return a + b");
var x = Function("a", "b", "return a + b");
var x = Function.call(null, "a", "b", "return a + b");
var x = Function.apply(null, ["a", "b", "return a + b"]);
var x = Function.bind(null, "a", "b", "return a + b")();
var f = Function.bind(null, "a", "b", "return a + b");
```
✅ 
```
let x = function (a, b) {
  return a + b;
};
```

### eslint/no-new-wrappers
Do not use `new` operators with the `String`, `Number`, and `Boolean` objects.
❌ 
```
var stringObject = new String("Hello world");
var numberObject = new Number(33);
var booleanObject = new Boolean(false);
var symbolObject = new Symbol("foo"); // symbol is not a constructor
```
✅ 
```
var stringObject = "Hello world";
var stringObject2 = String(value);
var numberObject = Number(value);
var booleanObject = Boolean(value);
var symbolObject = Symbol("foo");
```

### eslint/no-object-constructor
Do not use calls to the Object constructor without an argument.
❌ 
```
Object();
new Object();
```
✅ 
```
Object("foo");
const obj = { a: 1, b: 2 };
const isObject = (value) => value === Object(value);
const createObject = (Object) => new Object();
```

### eslint/no-promise-executor-return
Do not use returning values from Promise executor functions.
❌ 
```
new Promise((resolve, reject) => {
  if (someCondition) {
    return defaultResult;
  }
  getSomething((err, result) => {
    if (err) {
…
```
✅ 
```
new Promise((resolve, reject) => {
  if (someCondition) {
    resolve(defaultResult);
    return;
  }
  getSomething((err, result) => {
…
```

### eslint/no-prototype-builtins
Do not use calling some `Object.prototype` methods directly on objects.
❌ 
```
var hasBarProperty = foo.hasOwnProperty("bar");
var isPrototypeOfBar = foo.isPrototypeOf(bar);
var barIsEnumerable = foo.propertyIsEnumerable("bar");
```

### eslint/no-redeclare
This rule disallows redeclaring variables within the same scope, ensuring that each variable is declared only once.
❌ 
```
var a = 3;
var a = 10;
```
✅ 
```
var a = 3;
a = 10;
```

### eslint/no-restricted-exports
This rule disallows specified names from being used as exported names.

### eslint/no-return-assign
Do not use assignment operators in return statements.
❌ 
```
() => (a = b);
function x() {
  return (a = b);
}
```
✅ 
```
() => (a = b);
function x() {
  var result = (a = b);
  return result;
}
```

### eslint/no-script-url
Do not use `javascript:` URLs.
❌ 
```
location.href = "javascript:void(0)";
location.href = `javascript:void(0)`;
```

### eslint/no-self-compare
Do not use comparisons where both sides are exactly the same.
❌ 
```
var x = 10;
if (x === x) {
  x = 20;
}
```

### eslint/no-template-curly-in-string
Do not use template literal placeholder syntax in regular strings.
❌ 
```
"Hello ${name}!";
"Hello ${name}!";
"Time: ${12 * 60 * 60 * 1000}";
```
✅ 
```
`Hello ${name}!`;
`Time: ${12 * 60 * 60 * 1000}`;
templateFunction`Hello ${name}`;
```

### eslint/no-ternary
Do not use ternary operators.
❌ `var foo = isBar ? baz : qux;`
✅ 
```
let foo;
if (isBar) {
  foo = baz;
} else {
  foo = qux;
}
```

### eslint/no-throw-literal
Do not use throwing literals or non-Error objects as exceptions.
❌ 
```
throw "error";
throw 0;
throw undefined;
throw null;
var err = new Error();
throw "an " + err;
…
```
✅ 
```
throw new Error();
throw new Error("error");
var e = new Error("error");
throw e;
try {
  throw new Error("error");
…
```

### eslint/no-undef
Do not use the use of undeclared variables.
❌ 
```
var foo = someFunction();
var bar = a + 1;
```

### eslint/no-unreachable
Do not use unreachable code after `return`, `throw`, `continue`, and `break` statements.
❌ 
```
function foo() {
  return 2;
  console.log("this will never be executed");
}
```
✅ 
```
function foo() {
  console.log("this will be executed");
  return 2;
}
```

### eslint/no-useless-assignment
Avoid assignments where the newly assigned value is never read afterward (a "dead store").
❌ 
```
/* eslint no-useless-assignment: "error" */
function fn1() {
  let v = "used";
  doSomething(v);
  v = "unused"; // assigned but never read
}
…
```
✅ 
```
function fn1() {
  let v = "used";
  doSomething(v);
  v = "used-2";
  doSomething(v); // the reassigned value is read
}
…
```

### eslint/no-useless-computed-key
Do not use unnecessary computed property keys in objects and classes.
❌ 
```
const a = { ["0"]: 0 };
const b = { ["0+1,234"]: 0 };
const c = { [0]: 0 };
const e = { ["x"]() {} };
class Foo {
  ["foo"] = "bar";
…
```
✅ 
```
const a = { a: 0 };
const b = { 0: 0 };
const c = { x() {} };
const e = { "0+1,234": 0 };
class Foo {
  foo = "bar";
…
```

### eslint/no-useless-return
Do not use redundant return statements.
❌ 
```
function foo() {
  return;
}
function bar() {
  doSomething();
  return;
…
```
✅ 
```
function foo() {
  return 5;
}
function bar() {
  if (condition) {
    return;
…
```

### eslint/no-warning-comments
Do not use warning comments such as TODO, FIXME, XXX in code.
❌ 
```
// TODO: implement this feature
function doSomething() {}
// FIXME: this is broken
const x = 1;
/* XXX: hack */
let y = 2;
```
✅ 
```
// This is a regular comment
function doSomething() {}
// Note: This explains something
const x = 1;
```

### eslint/object-shorthand
Require or disallow method and property shorthand syntax for object literals

### eslint/operator-assignment
This rule requires or disallows assignment operator shorthand where possible.
❌ 
```
x = x + y;
x = y * x;
x[0] = x[0] / y;
x.y = x.y << z;
```
✅ 
```
x = y;
x += y;
x = y * z;
x = x * y * z;
x[0] /= y;
x[foo()] = x[foo()] % 2;
…
```

### eslint/prefer-const
Require `const` declarations for variables that are never reassigned after their initial declaration.
❌ 
```
let a = 3;
console.log(a);
let b;
b = 0;
console.log(b);
for (let i in [1, 2, 3]) {
…
```
✅ 
```
const a = 0;
let a;
a = 0;
a = 1;
let a;
if (true) {
…
```

### eslint/prefer-destructuring
Require destructuring from arrays and/or objects.
❌ 
```
// With `array` enabled
const foo = array[0];
bar.baz = array[0];
// With `object` enabled
const qux = object.qux;
const quux = object["quux"];
```
✅ 
```
// With `array` enabled
const [foo] = array;
const arr = array[someIndex];
[bar.baz] = array;
// With `object` enabled
const { baz } = object;
…
```

### eslint/prefer-exponentiation-operator
Do not use the use of `Math.pow` in favor of the `**` operator.
❌ `Math.pow(a, b);`
✅ `a ** b;`

### eslint/prefer-numeric-literals
Do not use `parseInt()` and `Number.parseInt()` in favor of binary, octal, and hexadecimal literals.
❌ 
```
parseInt("111110111", 2) === 503;
parseInt(`111110111`, 2) === 503;
parseInt("767", 8) === 503;
parseInt("1F7", 16) === 503;
Number.parseInt("111110111", 2) === 503;
Number.parseInt("767", 8) === 503;
…
```

### eslint/prefer-object-has-own
Do not use use of `Object.prototype.hasOwnProperty.call()` and prefer use of `Object.hasOwn()`
❌ 
```
Object.prototype.hasOwnProperty.call(obj, "a");
Object.hasOwnProperty.call(obj, "a");
({}).hasOwnProperty.call(obj, "a");
const hasProperty = Object.prototype.hasOwnProperty.call(object, property);
```
✅ 
```
Object.hasOwn(obj, "a");
const hasProperty = Object.hasOwn(object, property);
```

### eslint/prefer-object-spread
Do not use using `Object.assign` with an object literal as the first argument and prefer the use of object spread instead.
❌ 
```
Object.assign({}, foo);
Object.assign({}, { foo: "bar" });
Object.assign({ foo: "bar" }, baz);
Object.assign({}, baz, { foo: "bar" });
Object.assign({}, { ...baz });
// Object.assign with a single argument that is an object literal
…
```
✅ 
```
({ ...foo });
({ ...baz, foo: "bar" });
// Any Object.assign call without an object literal as the first argument
Object.assign(foo, { bar: baz });
Object.assign(foo, bar);
Object.assign(foo, { bar, baz });
…
```

### eslint/prefer-promise-reject-errors
Require using Error objects as Promise rejection reasons.
❌ 
```
Promise.reject("something bad happened");
Promise.reject(5);
Promise.reject();
new Promise(function (resolve, reject) {
  reject("something bad happened");
});
…
```
✅ 
```
Promise.reject(new Error("something bad happened"));
Promise.reject(new TypeError("something bad happened"));
new Promise(function (resolve, reject) {
  reject(new Error("something bad happened"));
});
var foo = getUnknownValue();
…
```

### eslint/prefer-rest-params
Do not use the use of the `arguments` object and instead enforces the use of rest parameters.
❌ 
```
function foo() {
  console.log(arguments);
}
function foo(action) {
  var args = Array.prototype.slice.call(arguments, 1);
  action.apply(null, args);
…
```
✅ 
```
function foo(...args) {
  console.log(args);
}
function foo(action, ...args) {
  action.apply(null, args); // Or use `action(...args)` (related to `prefer-spread` rule).
}
…
```

### eslint/prefer-spread
Require spread operators instead of `.apply()`
❌ 
```
foo.apply(undefined, args);
foo.apply(null, args);
obj.foo.apply(obj, args);
```
✅ 
```
// Using spread syntax
foo(...args);
obj.foo(...args);
// The `this` binding is different.
foo.apply(obj, args);
obj.foo.apply(null, args);
…
```

### eslint/prefer-template
Require template literals instead of string concatenation.
❌ 
```
const str = "Hello, " + name + "!";
const str1 = "Time: " + 12 * 60 * 60 * 1000;
```
✅ 
```
const str = "Hello World!";
const str2 = `Time: ${12 * 60 * 60 * 1000}`;
const str4 = "Hello, " + "World!";
```

### eslint/radix
Enforce the consistent use of the radix argument when using `parseInt()`, which specifies what base to use for parsing the number.
❌ `let num = parseInt("071"); // 57`
✅ `let num = parseInt("071", 10); // 71`

### eslint/require-await
Do not use async functions which have no `await` expression.
❌ 
```
async function foo() {
  doSomething();
}
```
✅ 
```
async function foo() {
  await doSomething();
}
```

### eslint/sort-imports
This rule checks all import declarations and verifies that all imports are first sorted by the used member syntax and then alphabetically by the first member or alias name.
❌ 
```
import { b, a, c } from "foo.js";
import d from "foo.js";
import e from "bar.js";
```

### eslint/sort-keys
When declaring multiple properties, sorting property names alphabetically makes it easier to find and/or diff necessary properties at a later time.
❌ 
```
let myObj = {
  c: 1,
  a: 2,
};
```
✅ 
```
let myObj = {
  a: 2,
  c: 1,
};
```

### eslint/sort-vars
When declaring multiple variables within the same block, sorting variable names make it easier to find necessary variable easier at a later time.
❌ 
```
var b, a;
var a, B, c;
```
✅ 
```
var a, b, c, d;
var B, a, c;
```

### eslint/symbol-description
Require symbol descriptions.
❌ `var foo = Symbol();`
✅ `var foo = Symbol("some description");`

### eslint/vars-on-top
Enforce that all `var` declarations are placed at the top of their containing scope.
❌ 
```
function doSomething() {
  if (true) {
    var first = true;
  }
  var second;
}
…
```
✅ 
```
function doSomething() {
  var first;
  var second;
  if (true) {
    first = true;
  }
…
```

### eslint/yoda
Require or disallow "Yoda" conditions.


## Plugin: `import`

### import/consistent-type-specifier-style
This rule either enforces or bans the use of inline type-only markers for named imports.

### import/export
Avoid funny business with exports, like repeated exports of names or defaults.
❌ 
```
let foo;
export { foo }; // Multiple exports of name 'foo'.
export * from "./export-all"; // Conflicts if export-all.js also exports foo
```
✅ 
```
let foo;
export { foo as foo1 }; // Renamed export to avoid conflict
export * from "./export-all"; // No conflict if export-all.js also exports foo
```

### import/exports-last
This rule enforces that all exports are declared at the bottom of the file.
❌ 
```
const bool = true;
export const foo = "bar";
const str = "foo";
```
✅ 
```
const arr = ["bar"];
export const bool = true;
export const str = "foo";
export function func() {
  console.log("Hello World");
}
```

### import/first
Do not use any non-import statements before imports except directives.
❌ 
```
import { x } from "./foo";
export { x };
import { y } from "./bar";
```
✅ 
```
import { x } from "./foo";
import { y } from "./bar";
export { x, y };
```

### import/group-exports
Avoid when named exports are not grouped together in a single export declaration or when multiple assignments to CommonJS module.exports or exports object are present in a single file.
❌ 
```
export const first = true;
export const second = true;
```
✅ 
```
const first = true;
const second = true;
export { first, second };
```

### import/max-dependencies
Do not use modules to have too many dependencies (`import` statements only).
❌ 
```
import a from "./a";
import b from "./b";
import c from "./c"; // Too many dependencies: 3 (max: 2)
```
✅ 
```
import a from "./a";
import b from "./b"; // Allowed: 2 dependencies (max: 2)
```

### import/named
Verifies that all named imports are part of the set of named exports in the referenced module.
❌ 
```
// ./baz.js
import { notFoo } from "./foo";
// re-export
export { notFoo as defNotBar } from "./foo";
// will follow 'jsnext:main', if available
import { dontCreateStore } from "redux";
```
✅ 
```
// ./bar.js
import { foo } from "./foo";
// re-export
export { foo as bar } from "./foo";
// node_modules without jsnext:main are not analyzed by default
// (import/ignore setting)
…
```

### import/no-anonymous-default-export
Avoid if a module's default export is unnamed.
❌ 
```
export default [];
export default () => {};
export default class {};
export default function() {};
export default foo(bar);
export default 123;
…
```
✅ 
```
const foo = 123;
export default foo;
export default function foo() {};
export default class MyClass {};
export default function foo() {};
export default foo(bar);
…
```

### import/no-duplicates
Avoid if a resolved path is imported more than once in the same module.
❌ 
```
import { foo } from "./module";
import { bar } from "./module";
import a from "./module";
import { b } from "./module";
```
✅ 
```
import { foo, bar } from "./module";
import * as a from "foo"; // separate statements for namespace imports
import { b } from "foo";
import { c } from "foo"; // separate type imports, unless
import type { d } from "foo"; // `prefer-inline` is true
```

### import/no-mutable-exports
Do not use the use of mutable exports with var or let.
❌ 
```
export let count = 2;
export var count = 3;
let count = 4;
export { count };
```
✅ 
```
export const count = 1;
export function getCount() {}
export class Counter {}
```

### import/no-named-default
Avoid use of a default export as a locally named import.
❌ 
```
// message: Using exported name 'bar' as identifier for default export.
import { default as foo } from "./foo.js";
import { default as foo, bar } from "./foo.js";
```
✅ 
```
import foo from "./foo.js";
import foo, { bar } from "./foo.js";
```

### import/no-named-export
Do not named exports.
❌ 
```
export const foo = "foo";
const bar = "bar";
export { bar };
```
✅ 
```
export default 'bar';
const foo = 'foo';
export { foo as default }
```

### import/no-namespace
Enforce a convention of not using namespaced (a.k.a.
❌ 
```
import * as user from "user-lib";
import some, * as user from "./user";
```
✅ 
```
import { getUserName, isUser } from "user-lib";
import user from "user-lib";
import defaultExport, { isUser } from "./user";
```

### import/no-nodejs-modules
Do not use the use of Node.js builtin modules.
❌ 
```
import fs from "fs";
import path from "path";
var fs = require("fs");
var path = require("path");
```
✅ 
```
import _ from "lodash";
import foo from "foo";
import foo from "./foo";
var _ = require("lodash");
var foo = require("foo");
var foo = require("./foo");
…
```

### import/prefer-default-export
In exporting files, this rule checks if there is default export or not.
❌ `export const foo = "foo";`
✅ 
```
export const foo = "foo";
const bar = "bar";
export default bar;
```


## Plugin: `node`

### node/global-require
Require `require()` calls to be placed at top-level module scope.
❌ 
```
// calling require() inside of a function is not allowed
function readFile(filename, callback) {
  var fs = require("fs");
  fs.readFile(filename, callback);
}
// conditional requires like this are also not allowed
…
```
✅ 
```
// all these variations of require() are ok
require("x");
var y = require("y");
var z;
z = require("z").initialize();
// requiring a module and using it in a function is ok
…
```

### node/no-exports-assign
Do not use assignment to `exports`.
❌ `exports = {};`
✅ 
```
module.exports.foo = 1;
exports.bar = 2;
module.exports = {};
// allows `exports = {}` if along with `module.exports =`
module.exports = exports = {};
exports = module.exports = {};
```


## Plugin: `oxc`

### oxc/branches-sharing-code
If the `if` and `else` blocks contain shared code that can be moved out of the blocks.
❌ 
```
if (condition) {
  console.log("Hello");
  return 13;
} else {
  console.log("Hello");
  return 42;
…
```
✅ 
```
console.log("Hello");
if (condition) {
  return 13;
} else {
  return 42;
}
…
```


## Plugin: `promise`

### promise/avoid-new
Do not use creating promises with `new Promise()`.
❌ 
```
function foo() {
  return new Promise((resolve, reject) => {
    /* ... */
  });
}
```
✅ 
```
async function foo() {
  // ...
}
const bar = await Promise.all([baz(), bang()]);
```

### promise/no-nesting
Do not use nested `then()` or `catch()` statements.
❌ 
```
doThing().then(() => a.then());
doThing().then(function () {
  a.then();
});
doThing().then(() => {
  b.catch();
…
```
✅ 
```
doThing().then(() => 4);
doThing().then(function () {
  return 4;
});
doThing().catch(() => 4);
```

### promise/no-return-in-finally
Do not use return statements in a `finally()` callback of a promise.
❌ 
```
myPromise.finally(function (val) {
  return val;
});
```
✅ 
```
Promise.resolve(1).finally(() => {
  console.log(2);
});
```

### promise/no-return-wrap
Prevent unnecessary wrapping of return values in promises with either `Promise.resolve` or `Promise.reject`.
❌ 
```
myPromise().then(() => Promise.resolve(4));
myPromise().then(function () {
  return Promise.resolve(4);
});
myPromise().then(() => Promise.reject("err"));
myPromise().then(function () {
…
```
✅ 
```
myPromise().then(() => 4);
myPromise().then(function () {
  return 4;
});
myPromise().then(() => throw "err");
myPromise().then(function () {
…
```

### promise/param-names
Enforce standard parameter names for Promise constructors.
❌ 
```
new Promise(function (reject, resolve) {
  /* ... */
}); // incorrect order
new Promise(function (ok, fail) {
  /* ... */
}); // non-standard parameter names
```
✅ `new Promise(function (resolve, reject) {});`

### promise/prefer-await-to-callbacks
The rule encourages the use of `async/await` for handling asynchronous code instead of traditional callback functions.
❌ 
```
cb();
callback();
doSomething(arg, (err) => {});
function doSomethingElse(cb) {}
```
✅ 
```
await doSomething(arg);
async function doSomethingElse() {}
function* generator() {
  yield yieldValue((err) => {});
}
eventEmitter.on("error", (err) => {});
```

### promise/prefer-await-to-then
Prefer `await` to `then()`/`catch()`/`finally()` for reading Promise values.
❌ 
```
function foo() {
  hey.then((x) => {});
}
```
✅ 
```
async function hi() {
  await thing();
}
```

### promise/prefer-catch
Prefer `catch` to `then(a, b)` and `then(null, b)`.
❌ 
```
prom.then(fn1, fn2);
prom.then(null, fn2);
```
✅ 
```
prom.catch(fn2).then(fn1);
prom.catch(fn2);
```


## Plugin: `typescript`

### typescript/adjacent-overload-signatures
Require that function overload signatures be consecutive.
❌ 
```
declare namespace Foo {
  export function foo(s: string): void;
  export function foo(n: number): void;
  export function bar(): void;
  export function foo(sn: string | number): void;
}
…
```

### typescript/array-type
Require consistently using either `T[]` or `Array<T>` for arrays.
❌ 
```
const arr: Array<number> = new Array<number>();
const readonlyArr: ReadonlyArray<number> = [1, 2, 3];
```
✅ 
```
const arr: number[] = new Array<number>();
const readonlyArr: readonly number[] = [1, 2, 3];
```

### typescript/await-thenable
This rule disallows awaiting a value that is not a Thenable.
❌ 
```
await 12;
await (() => {});
// non-Promise values
await Math.random;
await { then() {} };
// this is not a Promise - it's a function that returns a Promise
…
```
✅ 
```
await Promise.resolve('value');
await Promise.reject(new Error());
// Promise-like values
await {
  then(onfulfilled, onrejected) {
    onfulfilled('value');
…
```

### typescript/ban-ts-comment
This rule lets you set which directive comments you want to allow in your codebase.
❌ 
```
if (false) {
  // @ts-ignore: Unreachable code error
  console.log("hello");
}
```

### typescript/ban-tslint-comment
This rule disallows `tslint:<rule-flag>` comments.
❌ 
```
// tslint:disable-next-line
someCode();
```
✅ `someCode();`

### typescript/ban-types
This rule bans specific types and can suggest alternatives.
❌ 
```
let foo: String = "foo";
let bar: Boolean = true;
```
✅ 
```
let foo: string = "foo";
let bar: boolean = true;
```

### typescript/class-literal-property-style
Enforce a consistent style for exposing literal values on classes.
❌ 
```
class C {
  get name() {
    return "oxc";
  }
}
```
✅ 
```
class C {
  readonly name = "oxc";
}
```

### typescript/consistent-generic-constructors
When constructing a generic class, you can specify the type arguments on either the left-hand side (as a type annotation) or the right-hand side (as part of the constructor call).
❌ 
```
const a: Foo<string> = new Foo();
const a = new Foo<string>(); // prefer type annotation
```
✅ 
```
const a = new Foo<string>();
const a: Foo<string> = new Foo(); // prefer type annotation
```

### typescript/consistent-indexed-object-style
Choose between requiring either `Record` type or indexed signature types.

### typescript/consistent-return
Enforce consistent return behavior in functions.
❌ 
```
function maybe(flag: boolean): number {
  if (flag) {
    return 1;
  }
  return;
}
```
✅ 
```
function maybe(flag: boolean): number {
  if (flag) {
    return 1;
  }
  return 0;
}
```

### typescript/consistent-type-assertions
Enforce consistent usage of TypeScript type assertions.
❌ `const value = <Foo>bar;`
✅ `const value = bar as Foo;`

### typescript/consistent-type-definitions
Enforce type definitions to consistently use either `interface` or `type`.
❌ `type T = { x: number };`
✅ 
```
type T = string;
type Foo = string | {};
interface T {
  x: number;
}
```

### typescript/consistent-type-exports
Enforce using `export type` for exports that are only used as types.
❌ 
```
type Foo = { bar: string };
export { Foo };
export { TypeOnly, value } from "./mod";
```
✅ 
```
type Foo = { bar: string };
export type { Foo };
export type { TypeOnly } from "./mod";
export { value } from "./mod";
```

### typescript/consistent-type-imports
Enforce consistent usage of type imports.
❌ 
```
import { Foo } from "Foo";
type T = Foo;
type S = import("Foo");
```
✅ `import type { Foo } from "Foo";`

### typescript/dot-notation
Enforce dot notation whenever property access can be written safely as `obj.prop`.
❌ 
```
obj["name"];
foo["bar"];
```
✅ 
```
obj.name;
foo.bar;
obj[key];
obj["not-an-identifier"];
```

### typescript/no-array-delete
This rule disallows using the delete operator on array values.
❌ 
```
declare const arr: number[];
delete arr[0];
```
✅ 
```
declare const arr: number[];
arr.splice(0, 1);
// or with a filter
const filteredArr = arr.filter((_, index) => index !== 0);
// delete on object is allowed
declare const obj: { a?: number };
…
```

### typescript/no-base-to-string
This rule requires `toString()` and `toLocaleString()` calls to only be called on objects which provide useful information when stringified.
❌ 
```
// These will evaluate to '[object Object]'
({}).toString();
({ foo: "bar" }).toString();
({ foo: "bar" }).toLocaleString();
// This will evaluate to 'Symbol()'
Symbol("foo").toString();
```
✅ 
```
const someString = "Hello world";
someString.toString();
const someNumber = 42;
someNumber.toString();
const someBoolean = true;
someBoolean.toString();
…
```

### typescript/no-confusing-void-expression
This rule forbids using void expressions in confusing locations such as arrow function returns.
❌ 
```
// arrow function returning void expression
const foo = () => void bar();
// conditional expression
const result = condition ? void foo() : bar();
// void in conditional
if (void foo()) {
…
```
✅ 
```
// proper use of void
void foo();
// explicit return statement
const foo = () => {
  bar();
  return;
…
```

### typescript/no-deprecated
Do not use using code marked as `@deprecated`.
❌ 
```
/** @deprecated Use apiV2 instead. */
declare function apiV1(): Promise<string>;
declare function apiV2(): Promise<string>;
await apiV1(); // Using deprecated function
import { parse } from "node:url";
// 'parse' is deprecated. Use the WHATWG URL API instead.
…
```
✅ 
```
/** @deprecated Use apiV2 instead. */
declare function apiV1(): Promise<string>;
declare function apiV2(): Promise<string>;
await apiV2(); // Using non-deprecated function
// Modern Node.js API, uses `new URL()`
const url2 = new URL("/foo", "http://www.example.com");
```

### typescript/no-duplicate-type-constituents
This rule disallows duplicate constituents of union or intersection types.
❌ 
```
type T1 = "A" | "A";
type T2 = A | A | B;
type T3 = { a: string } & { a: string };
type T4 = [A, A];
type T5 = "foo" | "bar" | "foo";
```
✅ 
```
type T1 = "A" | "B";
type T2 = A | B | C;
type T3 = { a: string } & { b: string };
type T4 = [A, B];
type T5 = "foo" | "bar" | "baz";
```

### typescript/no-empty-interface
Do not use the declaration of empty interfaces.
❌ 
```
interface Foo {}
interface Bar extends Foo {}
```
✅ 
```
interface Foo {
  member: string;
}
interface Bar extends Foo {
  member: string;
}
```

### typescript/no-floating-promises
This rule disallows "floating" Promises in TypeScript code, which is a Promise that is created without any code to handle its resolution or rejection.
❌ 
```
const promise = new Promise((resolve, reject) => resolve("value"));
promise;
async function returnsPromise() {
  return "value";
}
returnsPromise().then(() => {});
…
```
✅ 
```
const promise = new Promise((resolve, reject) => resolve("value"));
await promise;
async function returnsPromise() {
  return "value";
}
void returnsPromise();
…
```

### typescript/no-for-in-array
This rule disallows iterating over an array with a for-in loop.
❌ 
```
const arr = [1, 2, 3];
for (const i in arr) {
  console.log(arr[i]);
}
for (const i in arr) {
  console.log(i, arr[i]);
…
```
✅ 
```
const arr = [1, 2, 3];
// Use for-of to iterate over array values
for (const value of arr) {
  console.log(value);
}
// Use regular for loop with index
…
```

### typescript/no-implied-eval
This rule disallows the use of eval-like methods.
❌ 
```
setTimeout('alert("Hi!");', 100);
setInterval('alert("Hi!");', 100);
setImmediate('alert("Hi!")');
window.setTimeout("count = 5", 10);
window.setInterval("foo = bar", 10);
const fn = new Function("a", "b", "return a + b");
```
✅ 
```
setTimeout(() => {
  alert("Hi!");
}, 100);
setInterval(() => {
  alert("Hi!");
}, 100);
…
```

### typescript/no-inferrable-types
Do not use explicit type declarations for variables or parameters initialized to a number, string, or boolean.
❌ 
```
const a: number = 5;
const b: string = "foo";
const c: boolean = true;
const fn = (a: number = 5, b: boolean = true, c: string = "foo") => {};
```
✅ 
```
const a = 5;
const b = "foo";
const c = true;
const fn = (a = 5, b = true, c = "foo") => {};
```

### typescript/no-meaningless-void-operator
This rule disallows the void operator when its argument is already of type void or `undefined`.
❌ 
```
function foo(): void {
  return;
}
void foo(); // meaningless, foo() already returns void
void undefined; // meaningless, undefined is already undefined
async function bar() {
…
```
✅ 
```
function getValue(): number {
  return 42;
}
void getValue(); // meaningful, converts number to void
void console.log("hello"); // meaningful, console.log returns undefined but we want to be explicit
function processData() {
…
```

### typescript/no-misused-promises
This rule forbids providing Promises to logical locations such as if statements in places where the TypeScript compiler allows them but they are not handled properly.
❌ 
```
// Promises in conditionals:
const promise = Promise.resolve("value");
if (promise) {
  // Do something
}
// Promises where `void` return was expected:
…
```
✅ 
```
// Awaiting the Promise to get its value in a conditional:
const promise = Promise.resolve("value");
if (await promise) {
  // Do something
}
// Using a `for-of` with `await` inside (instead of `forEach`):
…
```

### typescript/no-misused-spread
This rule disallows spreading syntax in places where it doesn't make sense or could cause runtime errors.
❌ 
```
// Spreading a non-iterable value in an array
const num = 42;
const arr = [...num]; // Runtime error: num is not iterable
// Spreading a Promise in an array
const promise = Promise.resolve([1, 2, 3]);
const arr2 = [...promise]; // Runtime error: Promise is not iterable
…
```
✅ 
```
// Spreading arrays
const arr1 = [1, 2, 3];
const arr2 = [...arr1];
// Spreading objects
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1 };
…
```

### typescript/no-mixed-enums
This rule disallows enums from having both string and numeric members.
❌ 
```
enum Status {
  Open = 1,
  Closed = "closed",
}
enum Direction {
  Up = "up",
…
```
✅ 
```
// All numeric
enum Status {
  Open = 1,
  Closed = 2,
}
// All string
…
```

### typescript/no-redundant-type-constituents
This rule disallows type constituents of unions and intersections that are redundant.
❌ 
```
// unknown is redundant in unions
type T1 = string | unknown;
// any is redundant in unions
type T2 = string | any;
// never is redundant in unions
type T3 = string | never;
…
```
✅ 
```
type T1 = string | number;
type T2 = "hello" | "world";
type T3 = { a: string } | { b: number };
// unknown in intersections is meaningful
type T4 = string & unknown;
// never in intersections is meaningful
…
```

### typescript/no-unnecessary-boolean-literal-compare
This rule disallows unnecessary equality comparisons with boolean literals.
❌ 
```
declare const someCondition: boolean;
if (someCondition === true) {
  // ...
}
if (someCondition === false) {
  // ...
…
```
✅ 
```
declare const someCondition: boolean;
if (someCondition) {
  // ...
}
if (!someCondition) {
  // ...
…
```

### typescript/no-unnecessary-condition
Do not use conditions that are always truthy, always falsy, or always nullish based on TypeScript's type information.
❌ 
```
declare const value: null;
if (value) {
  doWork();
}
const items: string[] = [];
if (items) {
…
```
✅ 
```
declare const maybeUser: User | undefined;
if (maybeUser) {
  doWork(maybeUser);
}
const items: string[] = [];
if (items.length > 0) {
…
```

### typescript/no-unnecessary-qualifier
Do not use namespace qualifiers when the referenced name is already in scope.
❌ 
```
namespace A {
  export type B = number;
  const value: A.B = 1;
}
```
✅ 
```
namespace A {
  export type B = number;
  const value: B = 1;
}
```

### typescript/no-unnecessary-template-expression
Do not use unnecessary template expressions (interpolations) that can be simplified.
❌ 
```
// Static values can be incorporated into the surrounding template
const ab1 = `${"a"}${"b"}`;
const ab2 = `a${"b"}`;
const stringWithNumber = `${"1 + 1 = "}${2}`;
const stringWithBoolean = `${"true is "}${true}`;
// Expressions that are already strings can be rewritten without a template
…
```
✅ 
```
// Static values incorporated into the template
const ab1 = `ab`;
// Template with non-trivial interpolation
const name = "world";
const greeting = `Hello ${name}!`;
// Template with expression
…
```

### typescript/no-unnecessary-type-arguments
This rule disallows type arguments that are identical to the default type parameter.
❌ 
```
function identity<T = string>(arg: T): T {
  return arg;
}
// Unnecessary type argument - string is the default
const result = identity<string>("hello");
interface Container<T = number> {
…
```
✅ 
```
function identity<T = string>(arg: T): T {
  return arg;
}
// Using default type
const result1 = identity("hello");
// Using different type
…
```

### typescript/no-unnecessary-type-assertion
This rule disallows type assertions that do not change the type of an expression.
❌ 
```
const str: string = "hello";
const redundant = str as string; // unnecessary, str is already string
function getString(): string {
  return "hello";
}
const result = getString() as string; // unnecessary, getString() already returns string
…
```
✅ 
```
const unknown: unknown = "hello";
const str = unknown as string; // necessary to narrow type
const element = document.getElementById("myElement") as HTMLInputElement; // necessary for specific element type
const obj = { name: "John" };
const name = obj.name as const; // necessary for literal type
// No assertion needed
…
```

### typescript/no-unnecessary-type-conversion
Do not use unnecessary type conversion expressions.
❌ `const value = String("asdf");`
✅ `const value = "asdf";`

### typescript/no-unnecessary-type-parameters
Do not use type parameters that are declared but not meaningfully used.
❌ 
```
function parseYAML<T>(input: string): T {
  return input as any as T;
}
```
✅ 
```
function parseYAML(input: string): unknown {
  return input;
}
function identity<T>(value: T): T {
  return value;
}
```

### typescript/no-unsafe-argument
This rule disallows calling a function with an argument which is typed as `any`.
❌ 
```
declare const anyValue: any;
function takesString(str: string): void {
  console.log(str.length);
}
takesString(anyValue); // unsafe
declare function takesNumber(num: number): number;
…
```
✅ 
```
declare const stringValue: string;
declare const numberValue: number;
declare const unknownValue: unknown;
function takesString(str: string): void {
  console.log(str.length);
}
…
```

### typescript/no-unsafe-assignment
This rule disallows assigning a value with type `any` to variables and properties.
❌ 
```
declare const anyValue: any;
const str: string = anyValue; // unsafe assignment
let num: number;
num = anyValue; // unsafe assignment
const obj = {
  prop: anyValue as any, // unsafe assignment
…
```
✅ 
```
declare const stringValue: string;
declare const numberValue: number;
declare const unknownValue: unknown;
const str: string = stringValue; // safe
let num: number;
num = numberValue; // safe
…
```

### typescript/no-unsafe-call
This rule disallows calling a value with type `any`.
❌ 
```
declare const anyValue: any;
anyValue(); // unsafe call
anyValue(1, 2, 3); // unsafe call
const result = anyValue("hello"); // unsafe call
// Chained unsafe calls
anyValue().then().catch(); // unsafe
```
✅ 
```
declare const fn: () => void;
declare const fnWithParams: (a: number, b: string) => boolean;
declare const unknownValue: unknown;
fn(); // safe
const result = fnWithParams(1, "hello"); // safe
// Type guard for unknown
…
```

### typescript/no-unsafe-enum-comparison
This rule disallows comparing an enum value with a non-enum value.
❌ 
```
enum Status {
  Open = "open",
  Closed = "closed",
}
enum Color {
  Red = "red",
…
```
✅ 
```
enum Status {
  Open = "open",
  Closed = "closed",
}
declare const status: Status;
// Comparing with same enum values
…
```

### typescript/no-unsafe-function-type
Do not use using the unsafe built-in Function type.
❌ 
```
let noParametersOrReturn: Function;
noParametersOrReturn = () => {};
let stringToNumber: Function;
stringToNumber = (text: string) => text.length;
let identity: Function;
identity = (value) => value;
```
✅ 
```
let noParametersOrReturn: () => void;
noParametersOrReturn = () => {};
let stringToNumber: (text: string) => number;
stringToNumber = (text) => text.length;
let identity: <T>(value: T) => T;
identity = (value) => value;
```

### typescript/no-unsafe-member-access
This rule disallows member access on a value with type `any`.
❌ 
```
declare const anyValue: any;
anyValue.foo; // unsafe member access
anyValue.bar.baz; // unsafe nested member access
anyValue["key"]; // unsafe computed member access
const result = anyValue.method(); // unsafe method access
```
✅ 
```
declare const obj: { foo: string; bar: { baz: number } };
declare const unknownValue: unknown;
obj.foo; // safe
obj.bar.baz; // safe
obj["foo"]; // safe
// Type guard for unknown
…
```

### typescript/no-unsafe-return
This rule disallows returning a value with type `any` from a function.
❌ 
```
declare const anyValue: any;
function getString(): string {
  return anyValue; // unsafe return
}
const getNumber = (): number => anyValue; // unsafe return
function processData(): { name: string; age: number } {
…
```
✅ 
```
declare const stringValue: string;
declare const numberValue: number;
declare const unknownValue: unknown;
function getString(): string {
  return stringValue; // safe
}
…
```

### typescript/no-unsafe-type-assertion
Do not use unsafe type assertions that narrow a type.
❌ 
```
function f() {
  return Math.random() < 0.5 ? 42 : "oops";
}
const z = f() as number;
const items = [1, "2", 3, "4"];
const number = items[0] as number;
```
✅ 
```
function f() {
  return Math.random() < 0.5 ? 42 : "oops";
}
const z = f() as number | string | boolean;
const items = [1, "2", 3, "4"];
const number = items[0] as number | string | undefined;
```

### typescript/no-unsafe-unary-minus
This rule disallows using the unary minus operator on a value which is not of type 'number' | 'bigint'.
❌ 
```
declare const value: any;
const result1 = -value; // unsafe on any
declare const str: string;
const result2 = -str; // unsafe on string
declare const bool: boolean;
const result3 = -bool; // unsafe on boolean
…
```
✅ 
```
declare const num: number;
const result1 = -num; // safe
declare const bigint: bigint;
const result2 = -bigint; // safe
const literal = -42; // safe
const bigintLiteral = -42n; // safe
…
```

### typescript/no-useless-default-assignment
Do not use default assignments that can never be used.
❌ `[1, 2, 3].map((a = 0) => a + 1);`
✅ `[1, 2, 3].map((a) => a + 1);`

### typescript/non-nullable-type-assertion-style
This rule prefers a non-null assertion over an explicit type cast for non-nullable types.
❌ 
```
declare const value: string | null;
// Type assertion when non-null assertion would be clearer
const result1 = value as string;
declare const maybe: number | undefined;
const result2 = maybe as number;
// In function calls
…
```
✅ 
```
declare const value: string | null;
// Non-null assertion for non-nullable types
const result1 = value!;
declare const maybe: number | undefined;
const result2 = maybe!;
// In function calls
…
```

### typescript/only-throw-error
This rule disallows throwing non-Error values.
❌ 
```
throw "error"; // throwing string
throw 42; // throwing number
throw true; // throwing boolean
throw { message: "error" }; // throwing plain object
throw null; // throwing null
throw undefined; // throwing undefined
…
```
✅ 
```
throw new Error("Something went wrong");
throw new TypeError("Invalid type");
throw new RangeError("Value out of range");
// Custom Error subclasses
class CustomError extends Error {
  constructor(message: string) {
…
```

### typescript/parameter-properties
Require or disallows parameter properties in class constructors.

### typescript/prefer-enum-initializers
Require each enum member value to be explicitly initialized.
❌ 
```
// wrong, the value of `Close` is not constant
enum Status {
  Open = 1,
  Close,
}
```
✅ 
```
enum Status {
  Open = 1,
  Close = 2,
}
```

### typescript/prefer-find
Prefer `.find(...)` over `.filter(...)[0]` for retrieving a single element.
❌ `const first = list.filter((item) => item.active)[0];`
✅ `const first = list.find((item) => item.active);`

### typescript/prefer-for-of
Enforce the use of for-of loop instead of a for loop with a simple iteration.
❌ 
```
for (let i = 0; i < arr.length; i++) {
  console.log(arr[i]);
}
```
✅ 
```
for (const item of arr) {
  console.log(item);
}
```

### typescript/prefer-function-type
Enforce using function types instead of interfaces with call signatures.
❌ 
```
interface Example {
  (): string;
}
function foo(example: { (): number }): number {
  return example();
}
…
```
✅ 
```
type Example = () => string;
function foo(example: () => number): number {
  return example();
}
// Returns the function itself, not the `this` argument
type ReturnsSelf = (arg: string) => ReturnsSelf;
…
```

### typescript/prefer-includes
Enforce using `.includes()` instead of `.indexOf() !== -1` or `/regex/.test()`.
❌ 
```
// Using indexOf
const str = "hello world";
if (str.indexOf("world") !== -1) {
  console.log("found");
}
if (str.indexOf("world") != -1) {
…
```
✅ 
```
// Using includes for strings
const str = "hello world";
if (str.includes("world")) {
  console.log("found");
}
// Using includes for arrays
…
```

### typescript/prefer-nullish-coalescing
Enforce using the nullish coalescing operator (`??`) instead of logical OR (`||`) or conditional expressions when the left operand might be `null` or `undefined`.
❌ 
```
declare const x: string | null;
// Using || when ?? would be more appropriate
const foo = x || "default";
// Ternary that could use ??
const bar = x !== null && x !== undefined ? x : "default";
const baz = x != null ? x : "default";
…
```
✅ 
```
declare const x: string | null;
// Using nullish coalescing
const foo = x ?? "default";
// || is fine when you want falsy behavior
declare const y: string;
const bar = y || "default";
…
```

### typescript/prefer-optional-chain
Enforce using concise optional chain expressions instead of chained logical AND operators, negated logical OR operators, or empty objects.
❌ 
```
foo && foo.bar;
foo && foo.bar && foo.bar.baz;
foo && foo["bar"];
foo && foo.bar && foo.bar.baz && foo.bar.baz.buzz;
foo && foo.bar && foo.bar.baz.buzz;
foo && foo.bar.baz && foo.bar.baz.buzz;
…
```
✅ 
```
foo?.bar;
foo?.bar?.baz;
foo?.["bar"];
foo?.bar?.baz?.buzz;
foo?.bar?.baz.buzz;
foo?.bar.baz?.buzz;
…
```

### typescript/prefer-promise-reject-errors
This rule enforces passing an Error object to `Promise.reject()`.
❌ 
```
Promise.reject("error"); // rejecting with string
Promise.reject(42); // rejecting with number
Promise.reject(true); // rejecting with boolean
Promise.reject({ message: "error" }); // rejecting with plain object
Promise.reject(null); // rejecting with null
Promise.reject(); // rejecting with undefined
…
```
✅ 
```
Promise.reject(new Error("Something went wrong"));
Promise.reject(new TypeError("Invalid type"));
Promise.reject(new RangeError("Value out of range"));
// Custom Error subclasses
class CustomError extends Error {
  constructor(message: string) {
…
```

### typescript/prefer-readonly
Require class members that are never reassigned to be marked `readonly`.
❌ 
```
class Counter {
  private value = 0;
  getValue() {
    return this.value;
  }
}
```
✅ 
```
class Counter {
  private readonly value = 0;
  getValue() {
    return this.value;
  }
}
```

### typescript/prefer-readonly-parameter-types
Require function and method parameters to use readonly-compatible types.
❌ 
```
function update(items: string[]) {
  items.push("x");
}
function consume(obj: { value: string }) {
  obj.value = obj.value.trim();
}
```
✅ 
```
function update(items: readonly string[]) {
  return items.length;
}
function consume(obj: Readonly<{ value: string }>) {
  return obj.value;
}
```

### typescript/prefer-reduce-type-parameter
This rule prefers using a type parameter for the accumulator in `Array#reduce()` instead of casting.
❌ 
```
const numbers = [1, 2, 3];
// Casting the result
const sum = numbers.reduce((acc, val) => acc + val, 0) as number;
// Using type assertion on accumulator
const result = [1, 2, 3].reduce((acc: string[], curr) => {
  acc.push(curr.toString());
…
```
✅ 
```
const numbers = [1, 2, 3];
// Using type parameter
const sum = numbers.reduce<number>((acc, val) => acc + val, 0);
// Type parameter for complex types
const result = [1, 2, 3].reduce<string[]>((acc, curr) => {
  acc.push(curr.toString());
…
```

### typescript/prefer-regexp-exec
Prefer `RegExp#exec()` over `String#match()` when extracting a regex match.
❌ 
```
const text = "value";
text.match(/v/);
```
✅ 
```
const text = "value";
/v/.exec(text);
```

### typescript/prefer-return-this-type
This rule enforces using `this` types for return types when possible.
❌ 
```
class Builder {
  private value: string = "";
  setValue(value: string): Builder {
    // Should return 'this'
    this.value = value;
    return this;
…
```
✅ 
```
class Builder {
  private value: string = "";
  setValue(value: string): this {
    this.value = value;
    return this;
  }
…
```

### typescript/prefer-string-starts-ends-with
Prefer `startsWith` and `endsWith` over manual string boundary checks.
❌ 
```
value.slice(0, 3) === "foo";
value.slice(-3) === "bar";
```
✅ 
```
value.startsWith("foo");
value.endsWith("bar");
```

### typescript/prefer-ts-expect-error
Enforce using @ts-expect-error over @ts-ignore.
❌ 
```
// @ts-ignore
const str: string = 1;
/**
 * Explaining comment
 *
 * @ts-ignore */
…
```
✅ 
```
/**
 * Explaining comment
 *
 * @ts-expect-error */
const multiLine: number = "value";
```

### typescript/promise-function-async
This rule requires any function or method that returns a Promise to be marked as async.
❌ 
```
// Function returning Promise without async
function fetchData(): Promise<string> {
  return fetch("/api/data").then((res) => res.text());
}
// Method returning Promise without async
class DataService {
…
```
✅ 
```
// Async function
async function fetchData(): Promise<string> {
  const response = await fetch("/api/data");
  return response.text();
}
// Async method
…
```

### typescript/related-getter-setter-pairs
This rule enforces that getters and setters for the same property are defined together and have related types.
❌ 
```
class Example {
  // Getter and setter with incompatible types
  get value(): string {
    return this._value.toString();
  }
  set value(val: number) {
…
```
✅ 
```
class Example {
  // Getter and setter with compatible types
  get value(): string {
    return this._value;
  }
  set value(val: string) {
…
```

### typescript/require-array-sort-compare
This rule requires `Array#sort()` to be called with a comparison function.
❌ 
```
const numbers = [3, 1, 4, 1, 5];
numbers.sort(); // Lexicographic sort, not numeric
const mixedArray = ["10", "2", "1"];
mixedArray.sort(); // Might be intended, but explicit compareFn is clearer
[3, 1, 4].sort(); // Will sort as strings: ['1', '3', '4']
```
✅ 
```
const numbers = [3, 1, 4, 1, 5];
// Numeric sort
numbers.sort((a, b) => a - b);
// Reverse numeric sort
numbers.sort((a, b) => b - a);
// String sort (explicit)
…
```

### typescript/require-await
This rule disallows async functions which do not have an await expression.
❌ 
```
// Async function without await
async function fetchData() {
  return fetch("/api/data");
}
// Async arrow function without await
const processData = async () => {
…
```
✅ 
```
// Async function with await
async function fetchData() {
  const response = await fetch("/api/data");
  return response.json();
}
// Regular function returning Promise
…
```

### typescript/restrict-plus-operands
This rule requires both operands of addition to be the same type and be number, string, or any.
❌ 
```
declare const num: number;
declare const str: string;
declare const bool: boolean;
declare const obj: object;
// Mixed types
const result1 = num + str; // number + string
…
```
✅ 
```
declare const num1: number;
declare const num2: number;
declare const str1: string;
declare const str2: string;
// Same types
const sum = num1 + num2; // number + number
…
```

### typescript/restrict-template-expressions
This rule restricts the types allowed in template literal expressions.
❌ 
```
declare const obj: object;
declare const sym: symbol;
declare const fn: () => void;
declare const arr: unknown[];
// Objects become "[object Object]"
const str1 = `Value: ${obj}`;
…
```
✅ 
```
declare const str: string;
declare const num: number;
declare const bool: boolean;
declare const obj: object;
// Safe types
const result1 = `String: ${str}`;
…
```

### typescript/return-await
This rule enforces consistent returning of awaited values from async functions.
❌ 
```
// If configured to require await:
async function fetchData() {
  return fetch("/api/data"); // Should be: return await fetch('/api/data');
}
async function processData() {
  return someAsyncOperation(); // Should be: return await someAsyncOperation();
…
```
✅ 
```
// When await is required for error handling:
async function fetchData() {
  try {
    return await fetch("/api/data");
  } catch (error) {
    console.error("Fetch failed:", error);
…
```

### typescript/strict-boolean-expressions
Do not use certain types in boolean expressions.
❌ 
```
const str = "hello";
if (str) {
  console.log("string");
}
const num = 42;
if (num) {
…
```
✅ 
```
const str = "hello";
if (str !== "") {
  console.log("string");
}
const num = 42;
if (num !== 0) {
…
```

### typescript/strict-void-return
Do not use returning non-void values where a `void` return is expected.
❌ 
```
declare function run(cb: () => void): void;
run(() => "value");
run(async () => 123);
```
✅ 
```
declare function run(cb: () => void): void;
run(() => {
  doWork();
});
run(() => undefined);
```

### typescript/switch-exhaustiveness-check
This rule requires switch statements to be exhaustive when switching on union types.
❌ 
```
type Status = "pending" | "approved" | "rejected";
function handleStatus(status: Status) {
  switch (status) {
    case "pending":
      return "Waiting for approval";
    case "approved":
…
```
✅ 
```
type Status = "pending" | "approved" | "rejected";
function handleStatus(status: Status) {
  switch (status) {
    case "pending":
      return "Waiting for approval";
    case "approved":
…
```

### typescript/unbound-method
This rule enforces unbound methods are called with their expected scope.
❌ 
```
class MyClass {
  private value = 42;
  getValue() {
    return this.value;
  }
  processValue() {
…
```
✅ 
```
class MyClass {
  private value = 42;
  getValue() {
    return this.value;
  }
  processValue() {
…
```

### typescript/unified-signatures
Do not use overload signatures that can be unified into one.
❌ 
```
function f(a: number): void;
function f(a: string): void;
```
✅ `function f(a: number | string): void;`

### typescript/use-unknown-in-catch-callback-variable
This rule enforces using `unknown` for catch clause variables instead of `any`.
❌ 
```
try {
  somethingRisky();
} catch (error: any) {
  // Should use 'unknown'
  console.log(error.message); // Unsafe access
  error.someMethod(); // Unsafe call
…
```
✅ 
```
try {
  somethingRisky();
} catch (error: unknown) {
  // Type guard for Error objects
  if (error instanceof Error) {
    console.log(error.message); // Safe access
…
```


## Plugin: `unicorn`

### unicorn/catch-error-name
This rule enforces consistent and descriptive naming for error variables in `catch` statements, preventing the use of vague names like `badName` or `_` when the error is used.
❌ 
```
try {
} catch (badName) {}
// `_` is not allowed if it's used
try {
} catch (_) {
  console.log(_);
…
```
✅ 
```
try {
} catch (error) {}
// `_` is allowed if it's not used
try {
} catch (_) {
  console.log(123);
…
```

### unicorn/consistent-assert
Enforce consistent usage of the `assert` module.
❌ 
```
import assert from "node:assert";
assert(divide(10, 2) === 5);
```
✅ 
```
import assert from "node:assert";
assert.ok(divide(10, 2) === 5);
```

### unicorn/consistent-date-clone
The Date constructor can clone a `Date` object directly when passed as an argument, making timestamp conversion unnecessary.
❌ `new Date(date.getTime());`
✅ `new Date(date);`

### unicorn/consistent-empty-array-spread
When spreading a ternary in an array, we can use both `[]` and `''` as fallbacks, but it's better to have consistent types in both branches.
❌ 
```
const array = [a, ...(foo ? [b, c] : "")];
const array = [a, ...(foo ? "bc" : [])];
```
✅ 
```
const array = [a, ...(foo ? [b, c] : [])];
const array = [a, ...(foo ? "bc" : "")];
```

### unicorn/consistent-existence-index-check
Enforce consistent style for element existence checks with `indexOf()`, `lastIndexOf()`, `findIndex()`, and `findLastIndex()`.
❌ 
```
const index = foo.indexOf("bar");
if (index < 0) {
}
const index = foo.indexOf("bar");
if (index >= 0) {
}
```
✅ 
```
const index = foo.indexOf("bar");
if (index === -1) {
}
const index = foo.indexOf("bar");
if (index !== -1) {
}
```

### unicorn/consistent-template-literal-escape
Enforce consistent style for escaping ${ in template literals.
❌ `const foo = `$\{a}`;`
✅ `const foo = `\${a}`;`

### unicorn/custom-error-definition
Enforce the only valid way of Error subclassing.
❌ 
```
class CustomError extends Error {
  constructor(message) {
    super(message);
    // The `this.message` assignment is useless as it's already set via the `super()` call.
    this.message = message;
    this.name = "CustomError";
…
```
✅ 
```
class CustomError extends Error {
  constructor(message) {
    super(message);
    this.name = "CustomError";
  }
}
…
```

### unicorn/empty-brace-spaces
Removes the extra spaces or new line characters inside a pair of braces that does not contain additional code.
❌ 
```
const a = {  };
class A {
}
```
✅ 
```
const a = {};
class A {}
```

### unicorn/error-message
Enforce providing a `message` when creating built-in `Error` objects to improve readability and debugging.
❌ 
```
throw Error();
throw new TypeError();
```
✅ 
```
throw new Error("Unexpected token");
throw new TypeError("Number expected");
```

### unicorn/escape-case
Enforce defining escape sequence values with uppercase characters rather than lowercase ones.
❌ 
```
const foo = "\xa9";
const foo = "\ud834";
const foo = "\u{1d306}";
const foo = "\ca";
```
✅ 
```
const foo = "\xA9";
const foo = "\uD834";
const foo = "\u{1D306}";
const foo = "\cA";
```

### unicorn/explicit-length-check
Enforce explicitly comparing the `length` or `size` property of a value.
❌ 
```
const isEmpty = foo.length == 0;
const isEmpty = foo.length < 1;
const isEmpty = 0 === foo.length;
const isEmpty = 0 == foo.length;
const isEmpty = 1 > foo.length;
const isEmpty = !foo.length;
…
```
✅ 
```
const isEmpty = foo.length === 0;
if (foo.length > 0 || bar.length > 0) {
}
const unicorn = foo.length > 0 ? 1 : 2;
```

### unicorn/filename-case
Enforce a consistent case style for filenames to improve project organization and maintainability.

### unicorn/new-for-builtins
Enforce the use of `new` for the following builtins: `Object`, `Array`, `ArrayBuffer`, `BigInt64Array`, `BigUint64Array`, `DataView`, `Date`, `Error`, `Float32Array`, `Float64Array`, `Function`, `Int8Array`, `Int16Array`, `Int32Array`, `M…
❌ 
```
const foo = new String("hello world");
const bar = Array(1, 2, 3);
```
✅ 
```
const foo = String("hello world");
const bar = new Array(1, 2, 3);
```

### unicorn/no-array-callback-reference
Prevent passing a function reference directly to iterator methods.
❌ 
```
const foo = array.map(callback);
array.forEach(callback);
const result = array.filter(lib.method);
```
✅ 
```
const foo = array.map((element) => callback(element));
array.forEach((element) => {
  callback(element);
});
const result = array.filter((element) => lib.method(element));
// Built-in functions are allowed
…
```

### unicorn/no-array-method-this-argument
Do not use the use of the `thisArg` parameter in array iteration methods such as `map`, `filter`, `some`, `every`, and similar.
❌ 
```
array.map(function (x) {
  return x + this.y;
}, this);
array.filter(function (x) {
  return x !== this.value;
}, this);
```
✅ 
```
array.map((x) => x + this.y);
array.filter((x) => x !== this.value);
const self = this;
array.map(function (x) {
  return x + self.y;
});
```

### unicorn/no-await-expression-member
Do not use member access from `await` expressions.
❌ 
```
async function bad() {
  const secondElement = (await getArray())[1];
}
```
✅ 
```
async function good() {
  const [, secondElement] = await getArray();
}
```

### unicorn/no-console-spaces
Do not use leading/trailing space inside `console.log()` and similar methods.
❌ `console.log("abc ", "def");`
✅ `console.log("abc", "def");`

### unicorn/no-hex-escape
Enforce a convention of using Unicode escapes instead of hexadecimal escapes for consistency and clarity.
❌ 
```
const foo = "\x1B";
const foo = `\x1B${bar}`;
```
✅ 
```
const foo = "\u001B";
const foo = `\u001B${bar}`;
```

### unicorn/no-immediate-mutation
Do not use mutating a variable immediately after initialization.
❌ 
```
const array = [1, 2];
array.push(3);
const object = { foo: 1 };
object.bar = 2;
const set = new Set([1, 2]);
set.add(3);
…
```
✅ 
```
const array = [1, 2, 3];
const object = { foo: 1, bar: 2 };
const set = new Set([1, 2, 3]);
const map = new Map([
  ["foo", 1],
  ["bar", 2],
…
```

### unicorn/no-instanceof-array
Require `Array.isArray()` instead of `instanceof Array`.
❌ 
```
array instanceof Array;
[1, 2, 3] instanceof Array;
```
✅ 
```
Array.isArray(array);
Array.isArray([1, 2, 3]);
```

### unicorn/no-lonely-if
Do not use `if` statements as the only statement in `if` blocks without `else`.
❌ 
```
if (foo) {
  if (bar) {
  }
}
if (foo) if (bar) baz();
```
✅ 
```
if (foo && bar) {
}
if (foo && bar) baz();
```

### unicorn/no-negation-in-equality-check
Do not use negated expressions on the left of (in)equality checks.
❌ 
```
if (!foo === bar) {
}
if (!foo !== bar) {
}
```
✅ 
```
if (foo !== bar) {
}
if (!(foo === bar)) {
}
```

### unicorn/no-nested-ternary
This rule disallows deeply nested ternary expressions.
❌ 
```
const foo = i > 5 ? (i < 100 ? true : false) : true;
const foo = i > 5 ? true : i < 100 ? true : i < 1000 ? true : false;
```
✅ 
```
const foo = i > 5 ? (i < 100 ? true : false) : true;
const foo = i > 5 ? (i < 100 ? true : false) : i < 100 ? true : false;
```

### unicorn/no-new-buffer
Do not use the deprecated `new Buffer()` constructor.
❌ `const buffer = new Buffer(10);`
✅ `const buffer = Buffer.alloc(10);`

### unicorn/no-null
Do not use the use of the `null` literal, to encourage using `undefined` instead.
❌ `let foo = null;`
✅ `let foo;`

### unicorn/no-object-as-default-parameter
Do not use the use of an object literal as a default value for a parameter.
❌ `function foo(foo = { a: false }) {}`
✅ `function foo({ a = false } = {}) {}`

### unicorn/no-static-only-class
Do not use `class` declarations that exclusively contain `static` members.
❌ 
```
class A {
  static a() {}
}
```
✅ 
```
class A {
  static a() {}
  constructor() {}
}
```

### unicorn/no-this-assignment
Do not use assigning `this` to a variable.
❌ 
```
const foo = this;
class Bar {
  method() {
    foo.baz();
  }
}
…
```
✅ 
```
class Bar {
  constructor(fooInstance) {
    this.fooInstance = fooInstance;
  }
  method() {
    this.fooInstance.baz();
…
```

### unicorn/no-typeof-undefined
Do not use `typeof` comparisons with `undefined`.
❌ `typeof foo === "undefined";`
✅ `foo === undefined;`

### unicorn/no-unnecessary-array-flat-depth
Do not use passing `1` to `Array.prototype.flat`.
❌ `foo.flat(1);`
✅ `foo.flat();`

### unicorn/no-unnecessary-array-splice-count
Do not use passing `.length` or `Infinity` as the `deleteCount` or `skipCount` argument of `Array#splice()` or `Array#toSpliced()`.
❌ 
```
array.splice(1, array.length);
array.splice(1, Infinity);
array.splice(1, Number.POSITIVE_INFINITY);
array.toSpliced(1, array.length);
```
✅ 
```
array.splice(1);
array.toSpliced(1);
```

### unicorn/no-unnecessary-slice-end
Do not use unnecessarily passing a second argument to `slice(...)`, for cases where it would not change the result.
❌ 
```
const foo = string.slice(1, string.length);
const foo = string.slice(1, Infinity);
const foo = string.slice(1, Number.POSITIVE_INFINITY);
```
✅ `const foo = string.slice(1);`

### unicorn/no-unreadable-array-destructuring
Do not use destructuring values from an array in ways that are difficult to read.
❌ 
```
const [, , foo] = parts;
const [, , ...rest] = parts;
```
✅ 
```
const [foo] = parts;
const foo = parts[3];
const rest = parts.slice(2);
// One is fine
const [, foo] = parts;
```

### unicorn/no-unreadable-iife
This rule disallows IIFEs with a parenthesized arrow function body.
❌ 
```
const foo = ((bar) => (bar ? bar.baz : baz))(getBar());
const foo = ((bar, baz) => ({ bar, baz }))(bar, baz);
```
✅ 
```
const bar = getBar();
const foo = bar ? bar.baz : baz;
const getBaz = (bar) => (bar ? bar.baz : baz);
const foo = getBaz(getBar());
const foo = ((bar) => {
  return bar ? bar.baz : baz;
…
```

### unicorn/no-useless-collection-argument
Do not use useless values or fallbacks in `Set`, `Map`, `WeakSet`, or `WeakMap`.
❌ 
```
const set = new Set([]);
const set = new Set("");
```
✅ `const set = new Set();`

### unicorn/no-useless-iterator-to-array
Do not use unnecessary `.toArray()` on iterators.
❌ 
```
const set = new Set(iterator.toArray());
const results = await Promise.all(iterator.toArray());
for (const item of iterator.toArray());
function* foo() {
  yield* iterator.toArray();
}
…
```
✅ 
```
const set = new Set(iterator);
const results = await Promise.all(iterator);
for (const item of iterator);
function * foo() {
	yield * iterator;
}
…
```

### unicorn/no-useless-promise-resolve-reject
Do not use returning values wrapped in `Promise.resolve` or `Promise.reject` in an async function or a `Promise#then`/`catch`/`finally` callback.
❌ `async () => Promise.resolve(bar);`
✅ `async () => bar;`

### unicorn/no-useless-switch-case
Do not use useless `default` cases in `switch` statements.
❌ 
```
switch (foo) {
  case 1:
  default:
    handleDefaultCase();
    break;
}
```
✅ 
```
switch (foo) {
  case 1:
  case 2:
    handleCase1And2();
    break;
}
```

### unicorn/no-useless-undefined
Prevent usage of `undefined` in cases where it would be useless.
❌ 
```
let foo = undefined;
const noop = () => undefined;
```
✅ 
```
let foo;
const noop = () => {};
```

### unicorn/no-zero-fractions
Prevent the use of zero fractions.
❌ 
```
const foo = 1.0;
const foo = -1.0;
const foo = 123_456.000_000;
```
✅ 
```
const foo = 1;
const foo = -1;
const foo = 123456;
const foo = 1.1;
```

### unicorn/number-literal-case
This rule enforces proper case for numeric literals.
❌ 
```
const foo = 0XFF;
const foo = 0xff;
const foo = 0Xff;
const foo = 0Xffn;
const foo = 0B10;
const foo = 0B10n;
…
```
✅ 
```
const foo = 0xFF;
const foo = 0b10;
const foo = 0o76;
const foo = 0xFFn;
const foo = 2e+5;
```

### unicorn/numeric-separators-style
Enforce a convention of grouping digits using numeric separators.
❌ `const invalid = [1_23_4444, 1_234.56789, 0xab_c_d_ef, 0b10_00_1111, 0o1_0_44_21, 1_294_28771_2n];`
✅ `const valid = [1_234_567, 1_234.567_89, 0xab_cd_ef, 0b1000_1111, 0o10_4421, 1_294_287_712n];`

### unicorn/prefer-array-flat
Prefer `Array#flat()` over legacy techniques to flatten arrays.
❌ 
```
const foo = array.flatMap((x) => x);
const foo = array.reduce((a, b) => a.concat(b), []);
const foo = array.reduce((a, b) => [...a, ...b], []);
const foo = [].concat(maybeArray);
const foo = [].concat(...array);
const foo = [].concat.apply([], array);
…
```
✅ 
```
const foo = array.flat();
const foo = [maybeArray].flat();
```

### unicorn/prefer-array-index-of
Enforce using `indexOf` or `lastIndexOf` instead of `findIndex` or `findLastIndex` when the callback is a simple strict equality comparison.
❌ 
```
values.findIndex((x) => x === "foo");
values.findLastIndex((x) => x === "bar");
```
✅ 
```
values.indexOf("foo");
values.lastIndexOf("bar");
```

### unicorn/prefer-array-some
Prefer using `Array#some()` over `Array#find()`, `Array#findLast()` with comparing to `undefined`, or `Array#findIndex()`, `Array#findLastIndex()` and a non-zero length check on the result of `Array#filter()`
❌ 
```
const foo = array.find(fn) ? bar : baz;
const foo = array.findLast((elem) => hasRole(elem)) !== null;
foo.findIndex(bar) < 0;
foo.findIndex((element) => element.bar === 1) !== -1;
foo.findLastIndex((element) => element.bar === 1) !== -1;
array.filter(fn).length === 0;
```
✅ 
```
const foo = array.some(fn) ? bar : baz;
foo.some((element) => element.bar === 1);
!array.some(fn);
```

### unicorn/prefer-at
Prefer the `Array#at()` and `String#at()` methods for index access.
❌ 
```
const foo = array[array.length - 1];
const foo = array.slice(-1)[0];
const foo = string.charAt(string.length - 1);
```
✅ 
```
const foo = array.at(-1);
const foo = array.at(-5);
const foo = string.at(-1);
```

### unicorn/prefer-bigint-literals
Require using BigInt literals (e.g.
❌ 
```
BigInt(0);
BigInt(123);
BigInt(0xff);
BigInt(1e3);
BigInt("42");
BigInt("0x10");
```
✅ 
```
0n;
123n;
0xffn;
1000n;
// Non-integer, dynamic, or non-literal input:
BigInt(x);
…
```

### unicorn/prefer-blob-reading-methods
Recommends using `Blob#text()` and `Blob#arrayBuffer()` over `FileReader#readAsText()` and `FileReader#readAsArrayBuffer()`.
❌ 
```
async function bad() {
  const arrayBuffer = await new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.addEventListener("load", () => {
      resolve(fileReader.result);
    });
…
```
✅ 
```
async function good() {
  const arrayBuffer = await blob.arrayBuffer();
}
```

### unicorn/prefer-class-fields
Prefer class field declarations over `this` assignments in constructors for static values.
❌ 
```
class Foo {
  constructor() {
    this.bar = 1;
  }
}
class MyError extends Error {
…
```
✅ 
```
class Foo {
  bar = 1;
}
class MyError extends Error {
  name = "MyError";
}
…
```

### unicorn/prefer-classlist-toggle
Prefer the use of `element.classList.toggle(className, condition)` over conditional add/remove patterns.
❌ 
```
if (condition) {
  element.classList.add("className");
} else {
  element.classList.remove("className");
}
condition ? element.classList.add("className") : element.classList.remove("className");
…
```
✅ `element.classList.toggle("className", condition);`

### unicorn/prefer-code-point
Prefer usage of `String.prototype.codePointAt` over `String.prototype.charCodeAt`.
❌ 
```
"🦄".charCodeAt(0);
String.fromCharCode(0x1f984);
```
✅ 
```
"🦄".codePointAt(0);
String.fromCodePoint(0x1f984);
```

### unicorn/prefer-date-now
Prefer use of `Date.now()` over `new Date().getTime()` or `new Date().valueOf()`.
❌ 
```
const ts = new Date().getTime();
const ts = new Date().valueOf();
```
✅ `const ts = Date.now();`

### unicorn/prefer-default-parameters
Instead of reassigning a function parameter, default parameters should be used.
❌ 
```
function abc(foo) {
  foo = foo || "bar";
}
function abc(foo) {
  const bar = foo || "bar";
}
```
✅ 
```
function abc(foo = "bar") {}
function abc(bar = "bar") {}
function abc(foo) {
  foo = foo || bar();
}
```

### unicorn/prefer-dom-node-append
Enforce the use of, for example, `document.body.append(div);` over `document.body.appendChild(div);` for DOM nodes.
❌ `foo.appendChild(bar);`
✅ `foo.append(bar);`

### unicorn/prefer-dom-node-dataset
Use `.dataset` on DOM elements over `getAttribute(…)`, `.setAttribute(…)`, `.removeAttribute(…)` and `.hasAttribute(…)`.
❌ `element.setAttribute("data-unicorn", "🦄");`
✅ `element.dataset.unicorn = "🦄";`

### unicorn/prefer-dom-node-remove
Prefer the use of `child.remove()` over `parentNode.removeChild(child)`.
❌ `parentNode.removeChild(childNode);`
✅ `childNode.remove();`

### unicorn/prefer-dom-node-text-content
Enforce the use of `.textContent` over `.innerText` for DOM nodes.
❌ `const text = foo.innerText;`
✅ `const text = foo.textContent;`

### unicorn/prefer-event-target
Prefer `EventTarget` over `EventEmitter`.
❌ `class Foo extends EventEmitter {}`
✅ `class Foo extends OtherClass {}`

### unicorn/prefer-global-this
Enforce the use of `globalThis` instead of environment‑specific global object aliases (`window`, `self`, or `global`).
❌ 
```
// Browser‑only
window.alert("Hi");
// Node‑only
if (typeof global.Buffer !== "undefined") {
}
// Web Worker‑only
…
```
✅ 
```
globalThis.alert("Hi");
if (typeof globalThis.Buffer !== "undefined") {
}
globalThis.postMessage("done");
```

### unicorn/prefer-import-meta-properties
Prefer `import.meta.{dirname,filename}` over legacy techniques for getting file paths.
❌ 
```
import path from "node:path";
import { fileURLToPath } from "url";
const filename = fileURLToPath(import.meta.url);
const dirname = path.dirname(fileURLToPath(import.meta.url));
const dirname = path.dirname(import.meta.filename);
const dirname = fileURLToPath(new URL(".", import.meta.url));
```
✅ 
```
const filename = import.meta.filename;
const dirname = import.meta.dirname;
```

### unicorn/prefer-includes
Prefer `includes()` over `indexOf()` when checking for existence or non-existence.
❌ 
```
if (str.indexOf("foo") !== -1) {
}
```
✅ 
```
if (str.includes("foo")) {
}
```

### unicorn/prefer-keyboard-event-key
Enforce the use of `KeyboardEvent#key` over `KeyboardEvent#keyCode`, which is deprecated.
❌ 
```
window.addEventListener("keydown", (event) => {
  if (event.keyCode === 8) {
    console.log("Backspace was pressed");
  }
});
window.addEventListener("keydown", (event) => {
…
```
✅ 
```
window.addEventListener("keydown", (event) => {
  if (event.key === "Backspace") {
    console.log("Backspace was pressed");
  }
});
window.addEventListener("click", (event) => {
…
```

### unicorn/prefer-logical-operator-over-ternary
This rule finds ternary expressions that can be simplified to a logical operator.
❌ 
```
const foo = bar ? bar : baz;
console.log(foo ? foo : bar);
```
✅ 
```
const foo = bar || baz;
console.log(foo ?? bar);
```

### unicorn/prefer-math-min-max
Prefer use of `Math.min()` and `Math.max()` instead of ternary expressions when performing simple comparisons.
❌ 
```
height > 50 ? 50 : height;
height > 50 ? height : 50;
```
✅ 
```
Math.min(height, 50);
Math.max(height, 50);
```

### unicorn/prefer-math-trunc
Prefer use of `Math.trunc()` instead of bitwise operations for clarity and more reliable results.
❌ `const foo = 1.1 | 0;`
✅ `const foo = Math.trunc(1.1);`

### unicorn/prefer-modern-dom-apis
Enforce the use of: * `childNode.replaceWith(newNode)` over `parentNode.replaceChild(newNode, oldNode)` * `referenceNode.before(newNode)` over `parentNode.insertBefore(newNode, referenceNode)` * `referenceNode.before('text')` over `refere…
❌ `oldChildNode.replaceWith(newChildNode);`
✅ `parentNode.replaceChild(newChildNode, oldChildNode);`

### unicorn/prefer-native-coercion-functions
Prefer built in functions, over custom ones with the same functionality.
❌ 
```
const foo = (v) => String(v);
foo(1);
const foo = (v) => Number(v);
array.some((v) => /* comment */ v);
```
✅ 
```
String(1);
Number(1);
array.some(Boolean);
```

### unicorn/prefer-negative-index
Prefer using a negative index over `.length - index` when possible.
❌ 
```
foo.slice(foo.length - 2, foo.length - 1);
foo.at(foo.length - 1);
```
✅ 
```
foo.slice(-2, -1);
foo.at(-1);
```

### unicorn/prefer-object-from-entries
Encourages using `Object.fromEntries` when converting an array of key-value pairs into an object.
❌ 
```
const result = pairs.reduce((obj, [key, value]) => {
  obj[key] = value;
  return obj;
}, {});
const result = {};
pairs.forEach(([key, value]) => {
…
```
✅ `const result = Object.fromEntries(pairs);`

### unicorn/prefer-optional-catch-binding
Prefer omitting the catch binding parameter if it is unused.
❌ 
```
try {
  // ...
} catch (e) {}
```
✅ 
```
try {
  // ...
} catch {}
```

### unicorn/prefer-prototype-methods
This rule prefers borrowing methods from the prototype instead of the instance.
❌ 
```
const array = [].slice.apply(bar);
const type = {}.toString.call(foo);
Reflect.apply([].forEach, arrayLike, [callback]);
```
✅ 
```
const array = Array.prototype.slice.apply(bar);
const type = Object.prototype.toString.call(foo);
Reflect.apply(Array.prototype.forEach, arrayLike, [callback]);
const maxValue = Math.max.apply(Math, numbers);
```

### unicorn/prefer-query-selector
Prefer `.querySelector()` over `.getElementById()`.
❌ 
```
document.getElementById("foo");
document.getElementsByClassName("foo bar");
document.getElementsByTagName("main");
document.getElementsByClassName(fn());
document.getElementsByName("foo");
```
✅ 
```
document.querySelector("#foo");
document.querySelector(".bar");
document.querySelector("main #foo .bar");
document.querySelectorAll(".foo .bar");
document.querySelectorAll("li a");
document.querySelector("li").querySelectorAll("a");
```

### unicorn/prefer-reflect-apply
Do not use the use of `Function.prototype.apply()` and suggests using `Reflect.apply()` instead.
❌ `foo.apply(null, [42]);`
✅ `Reflect.apply(foo, null);`

### unicorn/prefer-regexp-test
Prefer `RegExp#test()` over `String#match()` and `String#exec()`.
❌ 
```
if (string.match(/unicorn/)) {
}
if (/unicorn/.exec(string)) {
}
```
✅ 
```
if (/unicorn/.test(string)) {
}
Boolean(string.match(/unicorn/));
```

### unicorn/prefer-response-static-json
Enforce the use of `Response.json()` over `new Response(JSON.stringify())`.
❌ 
```
const response = new Response(JSON.stringify(data));
const response = new Response(JSON.stringify(data), { status: 200 });
```
✅ 
```
const response = Response.json(data);
const response = Response.json(data, { status: 200 });
```

### unicorn/prefer-spread
Enforce the use of the spread operator (`...`) over outdated patterns.
❌ 
```
const foo = Array.from(set);
const foo = Array.from(new Set([1, 2]));
```
✅ 
```
[...set].map(() => {});
Array.from(...argumentsArray);
```

### unicorn/prefer-string-raw
Prefer use of `String.raw` to avoid escaping `\`.
❌ 
```
const file = "C:\\windows\\style\\path\\to\\file.js";
const regexp = new RegExp("foo\\.bar");
```
✅ 
```
const file = String.raw`C:\windows\style\path\to\file.js`;
const regexp = new RegExp(String.raw`foo\.bar`);
```

### unicorn/prefer-string-replace-all
Prefer `String#replaceAll()` over `String#replace()` when using a regex with the global flag.
❌ `foo.replace(/a/g, bar);`
✅ 
```
foo.replace(/a/, bar);
foo.replaceAll(/a/, bar);
const pattern = "not-a-regexp";
foo.replace(pattern, bar);
```

### unicorn/prefer-string-slice
Prefer `String#slice()` over `String#substr()` and `String#substring()`.
❌ `"foo".substr(1, 2);`
✅ `"foo".slice(1, 2);`

### unicorn/prefer-string-trim-start-end
`String#trimLeft()` and `String#trimRight()` are aliases of `String#trimStart()` and `String#trimEnd()`.
❌ 
```
str.trimLeft();
str.trimRight();
```
✅ 
```
str.trimStart();
str.trimEnd();
```

### unicorn/prefer-structured-clone
Prefer using `structuredClone` to create a deep clone.
❌ 
```
const clone = JSON.parse(JSON.stringify(foo));
const clone = _.cloneDeep(foo);
```
✅ `const clone = structuredClone(foo);`

### unicorn/prefer-ternary
Prefer ternary expressions over simple `if`/`else` statements.
❌ 
```
if (test) {
  return a;
} else {
  return b;
}
```
✅ `return test ? a : b;`

### unicorn/prefer-top-level-await
Prefer top-level await over top-level promises and async function calls.
❌ 
```
(async () => {
  await run();
})();
run().catch((error) => {
  console.error(error);
});
```
✅ 
```
await run();
try {
  await run();
} catch (error) {
  console.error(error);
}
```

### unicorn/prefer-type-error
Enforce throwing a `TypeError` instead of a generic `Error` after a type checking if-statement.
❌ 
```
if (Array.isArray(foo)) {
  throw new Error("Expected foo to be an array");
}
```
✅ 
```
if (Array.isArray(foo)) {
  throw new TypeError("Expected foo to be an array");
}
```

### unicorn/relative-url-style
Enforce consistent relative URL style.
❌ `new URL("./foo", base);`
✅ `new URL("foo", base);`

### unicorn/require-array-join-separator
Enforce using the separator argument with `Array#join()`.
❌ `foo.join();`
✅ `foo.join(",");`

### unicorn/require-module-attributes
This rule enforces non-empty attribute list in `import`/`export` statements and `import()` expressions.
❌ 
```
import foo from "foo" with {};
export { foo } from "foo" with {};
const foo = await import("foo", {});
const foo = await import("foo", { with: {} });
```
✅ 
```
import foo from "foo";
export { foo } from "foo";
const foo = await import("foo");
const foo = await import("foo");
```

### unicorn/require-number-to-fixed-digits-argument
Enforce using the digits argument with `Number#toFixed()`.
❌ `number.toFixed();`
✅ 
```
number.toFixed(0);
number.toFixed(2);
```

### unicorn/switch-case-braces
Require empty switch cases to omit braces, while non-empty cases must use braces.
❌ 
```
switch (num) {
  case 1: {
  }
  case 2:
    console.log("Case 2");
    break;
…
```
✅ 
```
switch (num) {
  case 1:
  case 2: {
    console.log("Case 2");
    break;
  }
…
```

### unicorn/switch-case-break-position
Enforce consistent `break`/`return`/`continue`/`throw` position in `case` clauses.
❌ 
```
switch (foo) {
  case 1:
    {
      doStuff();
    }
    break;
…
```
✅ 
```
switch (foo) {
  case 1: {
    doStuff();
    break;
  }
}
```

### unicorn/text-encoding-identifier-case
This rule enforces consistent casing for text encoding identifiers, specifically: * `'utf8'` instead of `'UTF-8'` or `'utf-8'` (or `'utf-8'` if `withDash` is enabled) * `'ascii'` instead of `'ASCII'`
❌ 
```
import fs from "node:fs/promises";
async function bad() {
  await fs.readFile(file, "UTF-8");
  await fs.readFile(file, "ASCII");
  const string = buffer.toString("utf-8");
}
```
✅ 
```
import fs from "node:fs/promises";
async function good() {
  await fs.readFile(file, "utf8");
  await fs.readFile(file, "ascii");
  const string = buffer.toString("utf8");
}
```

### unicorn/throw-new-error
This rule makes sure you always use `new` when throwing an error.
❌ 
```
throw Error("🦄");
throw TypeError("unicorn");
throw lib.TypeError("unicorn");
```
✅ 
```
throw new Error("🦄");
throw new TypeError("unicorn");
throw new lib.TypeError("unicorn");
```
