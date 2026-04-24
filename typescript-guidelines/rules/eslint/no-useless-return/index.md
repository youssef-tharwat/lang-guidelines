
### What it does

Disallows redundant return statements.

### Why is this bad?

A `return;` statement with nothing after it is redundant, and has no effect
on the runtime behavior of a function. This can be confusing, so it's better
to disallow these redundant statements.

### Examples

Examples of **incorrect** code for this rule:

```js
function foo() {
  return;
}

function bar() {
  doSomething();
  return;
}

function baz() {
  if (condition) {
    doSomething();
    return;
  }
}
```

Examples of **correct** code for this rule:

```js
function foo() {
  return 5;
}

function bar() {
  if (condition) {
    return;
  }
  doSomething();
}

function baz() {
  return doSomething();
}
```

## How to use

## References
