
### What it does

Enforce using the digits argument with `Number#toFixed()`.

### Why is this bad?

It's better to make it clear what the value of the digits argument is when calling `Number#toFixed()`,
instead of relying on the default value of `0`.

### Examples

Examples of **incorrect** code for this rule:

```javascript
number.toFixed();
```

Examples of **correct** code for this rule:

```javascript
number.toFixed(0);
number.toFixed(2);
```

## How to use

## References
