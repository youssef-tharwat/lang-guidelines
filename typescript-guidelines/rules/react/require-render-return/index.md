
### What it does

Enforce ES5 or ES2015 class for returning value in the `render` function.

This rule is not relevant for function components, and so can potentially be
disabled for modern React codebases.

### Why is this bad?

When writing the `render` method in a component it is easy to forget to return the
JSX content. This rule will warn if the `return` statement is missing.

### Examples

Examples of **incorrect** code for this rule:

```jsx
var Hello = createReactClass({
  render() {
    <div>Hello</div>;
  },
});

class Hello extends React.Component {
  render() {
    <div>Hello</div>;
  }
}
```

Examples of **correct** code for this rule:

```jsx
var Hello = createReactClass({
  render() {
    return <div>Hello</div>;
  },
});

class Hello extends React.Component {
  render() {
    return <div>Hello</div>;
  }
}
```

## How to use

## References
