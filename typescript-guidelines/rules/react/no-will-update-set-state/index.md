
### What it does

Disallows using `setState` in the `componentWillUpdate` lifecycle method.

### Why is this bad?

Updating the state during the component update step can lead to indeterminate component state and is not allowed.
This can cause unexpected behavior and bugs in your React application.

### Examples

Examples of **incorrect** code for this rule:

```jsx
var Hello = createReactClass({
  componentWillUpdate: function () {
    this.setState({
      name: this.props.name.toUpperCase(),
    });
  },
  render: function () {
    return <div>Hello {this.state.name}</div>;
  },
});
```

Examples of **correct** code for this rule:

```jsx
var Hello = createReactClass({
  componentWillUpdate: function () {
    this.props.prepareHandler();
  },
  render: function () {
    return <div>Hello {this.state.name}</div>;
  },
});
```

## Configuration

This rule accepts one of the following string values:

### `"allowed"`

Forbids any call to `this.setState` in `componentWillUpdate` outside of functions.

### `"disallow-in-func"`

Makes this rule more strict by disallowing calls to \`this.setState\`\` even within functions.

## How to use

## References
