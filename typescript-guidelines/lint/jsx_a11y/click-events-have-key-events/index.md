
### What it does

Enforce onClick is accompanied by at least one of the following: onKeyUp, onKeyDown, onKeyPress.

### Why is this bad?

Coding for the keyboard is important for users with physical disabilities who cannot use a mouse, AT compatibility, and screenreader users.
This does not apply for interactive or hidden elements.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<div onClick={() => void 0} />
```

Examples of **correct** code for this rule:

```jsx
<div onClick={() => void 0} onKeyDown={() => void 0} />
```

## How to use

## References
