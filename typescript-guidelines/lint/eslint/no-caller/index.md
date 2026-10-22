
### What it does

Disallow the use of `arguments.caller` or `arguments.callee`.

### Why is this bad?

The use of `arguments.caller` and `arguments.callee` make several code
optimizations impossible. They have been deprecated in JavaScript, and
their use is forbidden while in strict mode.

```js
function foo() {
  var callee = arguments.callee;
}
```

This rule is aimed at discouraging the use of deprecated and sub-optimal
code by disallowing the use of `arguments.caller` and `arguments.callee`. As
such, it will warn when `arguments.caller` and `arguments.callee` are used.

See [the MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/arguments/callee)
for more information.

### Examples

Examples of **incorrect** code for this rule:

```js
function foo(n) {
  if (n <= 0) {
    return;
  }

  arguments.callee(n - 1);
}

[1, 2, 3, 4, 5].map(function (n) {
  return !(n > 1) ? 1 : arguments.callee(n - 1) * n;
});
```

Examples of **correct** code for this rule:

```js
function foo(n) {
  if (n <= 0) {
    return;
  }

  foo(n - 1);
}

[1, 2, 3, 4, 5].map(function factorial(n) {
  return !(n > 1) ? 1 : factorial(n - 1) * n;
});
```

## How to use

## References
