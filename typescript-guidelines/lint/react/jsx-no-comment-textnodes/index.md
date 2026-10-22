
### What it does

This rule prevents comment strings (e.g. beginning with `//` or `/*`) from being
accidentally injected as a text node in JSX statements.

### Why is this bad?

In JSX, any text node that is not wrapped in curly braces is considered
a literal string to be rendered. This can lead to unexpected behavior
when the text contains a comment.

### Examples

Examples of **incorrect** code for this rule:

```jsx
const Hello = () => {
  return <div>// empty div</div>;
};

const Hello = () => {
  return <div>/* empty div */</div>;
};
```

Examples of **correct** code for this rule:

```jsx
const Hello = () => {
  return <div>{/* empty div */}</div>;
};
```

## How to use

## References
