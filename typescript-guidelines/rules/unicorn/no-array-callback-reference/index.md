
### What it does

Prevents passing a function reference directly to iterator methods.

### Why is this bad?

Passing functions to iterator methods can cause issues when the function is changed
without realizing that the iterator passes 2 more parameters to it (index and array).
This can lead to unexpected behavior when the function signature changes.

### Examples

Examples of **incorrect** code for this rule:

```js
const foo = array.map(callback);
array.forEach(callback);
const result = array.filter(lib.method);
```

Examples of **correct** code for this rule:

```js
const foo = array.map((element) => callback(element));
array.forEach((element) => {
  callback(element);
});
const result = array.filter((element) => lib.method(element));

// Built-in functions are allowed
const foo = array.map(String);
const bar = array.filter(Boolean);
```

## How to use

## References
