
### What it does

This rule prevents using `isMounted` in class components.

### Why is this bad?

`isMounted` is an anti-pattern, and is not available
when using classes or function components.

### Examples

Examples of **incorrect** code for this rule:

```jsx
class Hello extends React.Component {
  someMethod() {
    if (!this.isMounted()) {
      return;
    }
  }
  render() {
    return <div onClick={this.someMethod.bind(this)}>Hello</div>;
  }
}
```

## How to use

## References
