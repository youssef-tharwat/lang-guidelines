
### What it does

This rule enforces proper case for numeric literals.

### Why is this bad?

When both an identifier and a numeric literal are in
lower case, it can be hard to differentiate between them.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const foo = 0XFF;
const foo = 0xff;
const foo = 0Xff;
const foo = 0Xffn;

const foo = 0B10;
const foo = 0B10n;

const foo = 0O76;
const foo = 0O76n;

const foo = 2E-5;
```

Examples of **correct** code for this rule:

```javascript
const foo = 0xFF;
const foo = 0b10;
const foo = 0o76;
const foo = 0xFFn;
const foo = 2e+5;
```

## How to use

## References
