
### What it does

Enforces that `aria-hidden="true"` is not set on focusable elements.

### Why is this bad?

`aria-hidden="true"` on focusable elements can lead to confusion or unexpected behavior for screen reader users.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<div aria-hidden="true" tabIndex="0" />
```

Examples of **correct** code for this rule:

```jsx
<div aria-hidden="true" />
```

## How to use

## References
