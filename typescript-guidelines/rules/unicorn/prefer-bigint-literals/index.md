
### What it does

Requires using BigInt literals (e.g. `123n`) instead of calling the `BigInt()` constructor
with literal arguments such as numbers or numeric strings

### Why is this bad?

Using `BigInt(…)` with literal values is unnecessarily verbose and less idiomatic than using
a BigInt literal.

### Examples

Examples of **incorrect** code for this rule:

```js
BigInt(0);
BigInt(123);
BigInt(0xff);
BigInt(1e3);
BigInt("42");
BigInt("0x10");
```

Examples of **correct** code for this rule:

```js
0n;
123n;
0xffn;
1000n;
// Non-integer, dynamic, or non-literal input:
BigInt(x);
BigInt("not-a-number");
BigInt("1.23");
```

## How to use

## References
