
### What it does

Enforces the use of `.textContent` over `.innerText` for DOM nodes.

### Why is this bad?

There are some disadvantages of using .innerText.

* `.innerText` is much more performance-heavy as it requires layout information to return the result.
* `.innerText` is defined only for HTMLElement objects, while `.textContent` is defined for all Node objects.
* `.innerText` is not standard, for example, it is not present in Firefox.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const text = foo.innerText;
```

Examples of **correct** code for this rule:

```javascript
const text = foo.textContent;
```

## How to use

## References
