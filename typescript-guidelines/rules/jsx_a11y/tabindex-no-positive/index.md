
### What it does

Enforces that positive values for the `tabIndex` attribute are not used
in JSX.

### Why is this bad?

Using `tabIndex` values greater than `0` can make navigation and
interaction difficult for keyboard and assistive technology users,
disrupting the logical order of content.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<span tabIndex="1">foo</span>
```

Examples of **correct** code for this rule:

```jsx
<span tabIndex="0">foo</span>
<span tabIndex="-1">bar</span>
```

## How to use

## References
