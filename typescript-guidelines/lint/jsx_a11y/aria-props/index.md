
### What it does

Enforces that elements do not use invalid ARIA attributes.

### Why is this bad?

Using invalid ARIA attributes can mislead screen readers and other assistive technologies.
It may cause the accessibility features of the website to fail, making it difficult
for users with disabilities to use the site effectively.

This rule includes fixes for some common typos.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<input aria-labeledby="address_label" />
```

Examples of **correct** code for this rule:

```jsx
<input aria-labelledby="address_label" />
```

## How to use

## References
