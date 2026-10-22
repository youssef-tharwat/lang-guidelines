
### What it does

Enforces that reserved DOM elements do not contain ARIA roles, states,
or properties.

### Why is this bad?

Certain reserved DOM elements do not support ARIA roles, states and
properties. This is often because they are not visible, for example
`meta`, `html`, `script`, `style`. Adding ARIA attributes to these
elements is meaningless and can create confusion for screen readers.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<meta charset="UTF-8" aria-hidden="false" />
```

Examples of **correct** code for this rule:

```jsx
<meta charset="UTF-8" />
```

## How to use

## References
