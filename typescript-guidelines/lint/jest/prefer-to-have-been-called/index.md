
### What it does

Suggests using `toHaveBeenCalled()` or `not.toHaveBeenCalled()` over `toHaveBeenCalledTimes(0)` or `toBeCalledTimes(0)`.

### Why is this bad?

`toHaveBeenCalled()` is more explicit and readable than `toHaveBeenCalledTimes(0)`.

### Examples

Examples of **incorrect** code for this rule:

```js
expect(mock).toHaveBeenCalledTimes(0);
expect(mock).toBeCalledTimes(0);
expect(mock).not.toHaveBeenCalledTimes(0);
```

Examples of **correct** code for this rule:

```js
expect(mock).not.toHaveBeenCalled();
expect(mock).toHaveBeenCalled();
expect(mock).toHaveBeenCalledTimes(1);
```

## How to use

## References
