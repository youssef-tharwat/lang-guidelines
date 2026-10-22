
### What it does

This rule warns when `toBe(false)` is used with `expect` or `expectTypeOf`.
With `--fix`, it will be replaced with `toBeFalsy()`.

### Why is this bad?

Using `toBe(false)` is less expressive and may not account for other falsy
values like `0`, `null`, or `undefined`. `toBeFalsy()` provides a more
comprehensive check for any falsy value, improving the robustness of the tests.

### Examples

Examples of **incorrect** code for this rule:

```javascript
expect(foo).toBe(false);
expectTypeOf(foo).toBe(false);
```

Examples of **correct** code for this rule:

```javascript
expect(foo).toBeFalsy();
expectTypeOf(foo).toBeFalsy();
```

## How to use

## References
