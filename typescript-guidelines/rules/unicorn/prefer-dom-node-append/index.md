
### What it does

Enforces the use of, for example, `document.body.append(div);` over `document.body.appendChild(div);` for DOM nodes.

### Why is this bad?

There are [some advantages of using `Node#append()`](https://developer.mozilla.org/en-US/docs/Web/API/ParentNode/append), like the ability to append multiple nodes and to append both [`DOMString`](https://developer.mozilla.org/en-US/docs/Web/API/DOMString) and DOM node objects.

### Examples

Examples of **incorrect** code for this rule:

```javascript
foo.appendChild(bar);
```

Examples of **correct** code for this rule:

```javascript
foo.append(bar);
```

## How to use

## References
