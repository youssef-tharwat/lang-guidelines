
### What it does

Require for-in loops to include an if statement.

### Why is this bad?

Looping over objects with a `for in` loop will include properties that are inherited through
the prototype chain. Using a `for in` loop without filtering the results in the loop can
lead to unexpected items in your for loop which can then lead to unexpected behaviour.

### Examples

Examples of **incorrect** code for this rule:

```javascript
for (key in foo) {
  doSomething(key);
}
```

Examples of **correct** code for this rule:

```javascript
for (key in foo) {
  if (Object.hasOwn(foo, key)) {
    doSomething(key);
  }
}
```

```javascript
for (key in foo) {
  if (Object.prototype.hasOwnProperty.call(foo, key)) {
    doSomething(key);
  }
}
```

```javascript
for (key in foo) {
  if ({}.hasOwnProperty.call(foo, key)) {
    doSomething(key);
  }
}
```

## How to use

## References
