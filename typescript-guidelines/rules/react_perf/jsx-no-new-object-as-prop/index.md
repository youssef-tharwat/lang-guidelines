
### What it does

Prevent Objects that are local to the current method from being used
as values of JSX props.

### Why is this bad?

Using locally defined Objects as values for props can lead to unintentional
re-renders and performance issues. Every time the parent component renders,
a new instance of the Object is created, causing unnecessary re-renders of
child components. This also leads to harder-to-maintain code as the
component's props are not passed consistently.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<Item config={{}} />
<Item config={new Object()} />
<Item config={Object()} />
<Item config={this.props.config || {}} />
<Item config={this.props.config ? this.props.config : {}} />
<div style={{display: 'none'}} />
```

Examples of **correct** code for this rule:

```jsx
<Item config={staticConfig} />
```

## How to use

## References
