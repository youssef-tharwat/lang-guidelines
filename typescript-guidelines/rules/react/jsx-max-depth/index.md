
### What it does

Enforces a maximum depth for nested JSX elements and fragments.

### Why is this bad?

Excessively nested JSX makes components harder to read and maintain.

### Examples

Examples of **incorrect** code for this rule:

```jsx
const Component = () => (
  <div>
    <div>
      <div>
        <span />
      </div>
    </div>
  </div>
);
```

Examples of **correct** code for this rule:

```jsx
const Component = () => (
  <div>
    <div>
      <span />
    </div>
  </div>
);
```

## Configuration

This rule accepts a configuration object with the following properties:

### max

type: `integer`

default: `2`

The maximum allowed depth of nested JSX elements and fragments.

## How to use

## References
