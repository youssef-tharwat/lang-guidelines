
### What it does

Disallow undeclared variables in JSX.

Note that this rule is generally unnecessary if you are using TypeScript, as
TypeScript will catch undeclared variables for you.

### Why is this bad?

It is most likely a potential ReferenceError caused by a misspelling of a variable or parameter name.

### Examples

Examples of **incorrect** code for this rule:

```jsx
const A = () => <App />;
const C = <B />;
```

## How to use

## References
