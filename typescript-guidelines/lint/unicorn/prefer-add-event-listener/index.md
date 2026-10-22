
### What it does

Enforces the use of `.addEventListener()` and `.removeEventListener()` over their `on`-function counterparts.

For example, `foo.addEventListener('click', handler);` is preferred over `foo.onclick = handler;` for HTML DOM Events.

### Why is this bad?

There are [numerous advantages of using `addEventListener`](https://stackoverflow.com/questions/6348494/addeventlistener-vs-onclick/35093997#35093997). Some of these advantages include registering unlimited event handlers and optionally having the event handler invoked only once.

### Examples

Examples of **incorrect** code for this rule:

```javascript
foo.onclick = () => {};
```

Examples of **correct** code for this rule:

```javascript
foo.addEventListener("click", () => {});
```

## How to use

## References
