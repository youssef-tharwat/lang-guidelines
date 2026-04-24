
### What it does

Enforces the use of:

* `childNode.replaceWith(newNode)` over `parentNode.replaceChild(newNode, oldNode)`
* `referenceNode.before(newNode)` over `parentNode.insertBefore(newNode, referenceNode)`
* `referenceNode.before('text')` over `referenceNode.insertAdjacentText('beforebegin', 'text')`
* `referenceNode.before(newNode)` over `referenceNode.insertAdjacentElement('beforebegin', newNode)`

### Why is this bad?

There are some advantages of using the newer DOM APIs, like:

* Traversing to the parent node is not necessary.
* Appending multiple nodes at once.
* Both `DOMString` and DOM node objects can be manipulated.

### Examples

Examples of **incorrect** code for this rule:

```javascript
oldChildNode.replaceWith(newChildNode);
```

Examples of **correct** code for this rule:

```javascript
parentNode.replaceChild(newChildNode, oldChildNode);
```

## How to use

## References
