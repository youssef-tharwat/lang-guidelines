
### What it does

Enforces that an element's autocomplete attribute must be a valid value.

### Why is this bad?

Incorrectly using the autocomplete attribute may decrease the accessibility of the website for users.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<input autocomplete="invalid-value" />
```

Examples of **correct** code for this rule:

```jsx
<input autocomplete="name" />
```

## Configuration

This rule accepts a configuration object with the following properties:

### inputComponents

type: `string[]`

default: `["input"]`

List of custom component names that should be treated as input elements.

## How to use

## References
