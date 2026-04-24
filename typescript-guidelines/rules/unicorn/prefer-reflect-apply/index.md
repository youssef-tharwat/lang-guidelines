
### What it does

Disallows the use of `Function.prototype.apply()` and suggests using `Reflect.apply()` instead.

### Why is this bad?

`Reflect.apply()` is arguably less verbose and easier to understand.
In addition, when you accept arbitrary methods,
it's not safe to assume `.apply()` exists or is not overridden.

### Examples

Examples of **incorrect** code for this rule:

```javascript
foo.apply(null, [42]);
```

Examples of **correct** code for this rule:

```javascript
Reflect.apply(foo, null);
```

## How to use

## References
