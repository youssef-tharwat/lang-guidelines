
### What it does

Disallow magic numbers for [`Array.prototype.flat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flat)
depth.

### Why is this bad?

Magic numbers are hard to understand and maintain.
When calling `Array.prototype.flat`, it is usually called with
`1` or `Infinity`. If you are using a different number, it is
better to add a comment explaining the reason for the depth provided.

### Examples

Examples of **incorrect** code for this rule:

```javascript
array.flat(2);
array.flat(20);
```

Examples of **correct** code for this rule:

```javascript
array.flat(2 /* explanation */);
array.flat(1);
array.flat();
array.flat(Infinity);
```

## How to use

## References
