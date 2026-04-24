
### What it does

Enforce return statements in callbacks of array methods.

### Why is this bad?

Array has several methods for filtering, mapping, and folding.
If we forget to write return statement in a callback of those, it’s probably a mistake.
If you don’t want to use a return or don’t need the returned results,
consider using .forEach instead.

### Examples

Examples of **incorrect** code for this rule:

```javascript
let foo = [1, 2, 3, 4];
foo.map((a) => {
  console.log(a);
});
```

Examples of **correct** code for this rule:

```javascript
let foo = [1, 2, 3, 4];
foo.map((a) => {
  console.log(a);
  return a;
});
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowImplicit

type: `boolean`

default: `false`

When set to true, allows callbacks of methods that require a return value to
implicitly return undefined with a return statement containing no expression.

### allowVoid

type: `boolean`

default: `false`

When set to true, rule will not report the return value with a void operator.
Works only if `checkForEach` option is set to true.

### checkForEach

type: `boolean`

default: `false`

When set to true, rule will also report forEach callbacks that return a value.

## How to use

## References
