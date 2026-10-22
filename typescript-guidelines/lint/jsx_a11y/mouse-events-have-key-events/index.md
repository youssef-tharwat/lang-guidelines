
### What it does

Enforce `onMouseOver`/`onMouseOut` are accompanied by `onFocus`/`onBlur`.

### Why is this bad?

Coding for the keyboard is important for users with physical disabilities who cannot use a mouse,
AT compatibility, and screen reader users.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<div onMouseOver={() => void 0} />
```

Examples of **correct** code for this rule:

```jsx
<div onMouseOver={() => void 0} onFocus={() => void 0} />
```

## Configuration

This rule accepts a configuration object with the following properties:

### hoverInHandlers

type: `string[]`

default: `["onMouseOver"]`

List of hover-in mouse event handlers that require corresponding keyboard event handlers.

### hoverOutHandlers

type: `string[]`

default: `["onMouseOut"]`

List of hover-out mouse event handlers that require corresponding keyboard event handlers.

## How to use

## References
