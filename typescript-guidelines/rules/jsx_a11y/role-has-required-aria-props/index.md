
### What it does

Enforces that elements with ARIA roles must have all required attributes
for that role.

### Why is this bad?

Certain ARIA roles require specific attributes to express necessary
semantics for assistive technology.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<div role="checkbox" />
```

Examples of **correct** code for this rule:

```jsx
<div role="checkbox" aria-checked="false" />
```

## How to use

## References
