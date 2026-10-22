
### What it does

It warns when you use a non-function value as the second argument of `removeEventListener`.

### Why is this bad?

The [`removeEventListener`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener) function must be called with a reference to the same function that was passed to [`addEventListener`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener). Calling `removeEventListener` with an inline function or the result of an inline `.bind()` call is indicative of an error, and won't actually remove the listener.

### Examples

Examples of **incorrect** code for this rule:

```javascript
el.removeEventListener("click", () => {});
el.removeEventListener("click", function () {});
```

Examples of **correct** code for this rule:

```javascript
el.removeEventListener("click", handler);
el.removeEventListener("click", handler.bind(this));
```

## How to use

## References
