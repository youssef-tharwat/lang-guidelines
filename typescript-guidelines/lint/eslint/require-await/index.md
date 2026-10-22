
### What it does

Disallow async functions which have no `await` expression.

::: warning NOTE
This rule is inferior to the accuracy of the type-aware
`typescript/require-await` rule. If using type-aware
rules, always prefer that rule over this one.
:::

### Why is this bad?

Asynchronous functions in JavaScript behave differently than other
functions in two important ways:

1. The return value is always a `Promise`.
2. You can use the `await` operator inside of them.

The primary reason to use asynchronous functions is typically to use the
await operator, such as this:

```js
async function fetchData(processDataItem) {
  const response = await fetch(DATA_URL);
  const data = await response.json();

  return data.map(processDataItem);
}
```

Asynchronous functions that don’t use `await` might not need to be
asynchronous functions and could be the unintentional result of
refactoring.

Note: this rule ignores async generator functions. This is because
generators yield rather than return a value and async generators might
yield all the values of another async generator without ever actually
needing to use `await`.

### Examples

Examples of **incorrect** code for this rule:

```js
async function foo() {
  doSomething();
}
```

Examples of **correct** code for this rule:

```js
async function foo() {
  await doSomething();
}
```

## How to use

## References
