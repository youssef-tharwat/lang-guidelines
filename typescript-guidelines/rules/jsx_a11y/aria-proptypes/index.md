
### What it does

Enforces that elements do not use invalid ARIA state and property values.

### Why is this bad?

Using invalid ARIA state and property values can mislead screen readers and other assistive technologies.
It may cause the accessibility features of the website to fail, making it difficult for users with disabilities to use the site effectively.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<div aria-level="yes" />
<div aria-relevant="additions removalss" />
```

Examples of **correct** code for this rule:

```jsx
<div aria-label="foo" />
<div aria-labelledby="foo bar" />
<div aria-checked={false} />
<div aria-invalid="grammar" />
```

## How to use

## References
