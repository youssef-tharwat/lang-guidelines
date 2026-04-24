
### What it does

This rule disallows the use of `findDOMNode`, which was deprecated in 2018 and removed in React 19.

### Why is this bad?

`findDOMNode` is an escape hatch used to access the underlying DOM node.
In most cases, use of this escape hatch is discouraged because it pierces the component abstraction.
It has been deprecated for years, and was
[removed from React entirely in React 19](https://react.dev/blog/2024/04/25/react-19-upgrade-guide#removed-reactdom-finddomnode).

It should not be used.

### Examples

Examples of **incorrect** code for this rule:

```jsx
class MyComponent extends Component {
  componentDidMount() {
    findDOMNode(this).scrollIntoView();
  }
  render() {
    return <div />;
  }
}
```

## How to use

## References
