
### What it does

Warn if an element uses an Array index in its key.

### Why is this bad?

It's a bad idea to use the array index since it doesn't uniquely identify your elements.
In cases where the array is sorted or an element is added to the beginning of the array,
the index will be changed even though the element representing that index may be the same.
This results in unnecessary renders.

### Examples

Examples of **incorrect** code for this rule:

```jsx
things.map((thing, index) => <Hello key={index} />);
```

Examples of **correct** code for this rule:

```jsx
things.map((thing, index) => <Hello key={thing.id} />);
```

## How to use

## References
