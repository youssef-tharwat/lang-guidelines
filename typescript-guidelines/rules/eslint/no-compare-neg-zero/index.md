
### What it does

Disallow comparing against `-0`

### Why is this bad?

The rule should warn against code that tries to compare against `-0`,
since that will not work as intended. That is, code like `x === -0` will
pass for both `+0` and `-0`. The author probably intended `Object.is(x, -0)`.

### Examples

Examples of **incorrect** code for this rule:

```javascript
if (x === -0) {
  // doSomething()...
}
```

```javascript
if (-0 > x) {
  // doSomething()...
}
```

Examples of **correct** code for this rule:

```javascript
if (x === 0) {
  // doSomething()...
}
```

```javascript
if (Object.is(x, -0)) {
  // doSomething()...
}
```

```javascript
if (0 > x) {
  // doSomething()...
}
```

## How to use

## References
