
### What it does

Requires that components wrapped with `forwardRef` must have a `ref` parameter.
Omitting the `ref` argument is usually a bug,
and components not using `ref` don't need to be wrapped by `forwardRef`.

### Why is this bad?

Omitting the `ref` argument makes the `forwardRef` wrapper unnecessary,
and can lead to confusion.

### Examples

Examples of **incorrect** code for this rule:

```jsx
var React = require("react");

var Component = React.forwardRef((props) => <div />);
```

Examples of **correct** code for this rule:

```jsx
var React = require("react");

var Component = React.forwardRef((props, ref) => <div ref={ref} />);

var Component = React.forwardRef((props, ref) => <div />);

function Component(props) {
  return <div />;
}
```

## How to use

## References
