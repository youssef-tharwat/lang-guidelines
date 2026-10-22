
### What it does

Prefers the use of `child.remove()` over `parentNode.removeChild(child)`.

### Why is this bad?

The DOM function [`Node#remove()`](https://developer.mozilla.org/en-US/docs/Web/API/ChildNode/remove) is preferred
over the indirect removal of an object with [`Node#removeChild()`](https://developer.mozilla.org/en-US/docs/Web/API/Node/removeChild).

### Examples

Examples of **incorrect** code for this rule:

```javascript
parentNode.removeChild(childNode);
```

Examples of **correct** code for this rule:

```javascript
childNode.remove();
```

## How to use

## References
