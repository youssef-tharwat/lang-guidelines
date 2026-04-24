
### What it does

This rule prevents characters that you may have meant as JSX escape characters from being accidentally injected as a text node in JSX statements.

### Why is this bad?

JSX escape characters are used to inject characters into JSX statements that would otherwise be interpreted as code.

### Example

Incorrect

```jsx
<div> > </div>
```

Correct

```jsx
<div> &gt; </div>
```

```jsx
<div> {">"} </div>
```

## How to use

## References
