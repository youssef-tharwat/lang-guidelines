
### What it does

This rule applies when bitwise operators are used where logical operators are expected.

### Why is this bad?

Bitwise operators have different results from logical operators and a `TypeError` exception may be thrown because short-circuit evaluation is not applied.
(In short-circuit evaluation, right operand evaluation is skipped according to left operand value, e.g. `x` is `false` in `x && y`.)

It is obvious that logical operators are expected in the following code patterns:

```javascript
e && e.x;
e || {};
e || "";
```

### Examples

Examples of **incorrect** code for this rule:

```javascript
if (obj & obj.prop) {
  console.log(obj.prop);
}
options = options | {};
input |= "";
```

Examples of **correct** code for this rule:

```javascript
if (obj && obj.prop) {
  console.log(obj.prop);
}
options = options || {};
input ||= "";
```

## How to use

## References
