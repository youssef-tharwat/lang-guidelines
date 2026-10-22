
### What it does

This rule disallows IIFEs with a parenthesized arrow function body.

### Why is this bad?

IIFEs with a parenthesized arrow function body are unreadable.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const foo = ((bar) => (bar ? bar.baz : baz))(getBar());

const foo = ((bar, baz) => ({ bar, baz }))(bar, baz);
```

Examples of **correct** code for this rule:

```javascript
const bar = getBar();
const foo = bar ? bar.baz : baz;

const getBaz = (bar) => (bar ? bar.baz : baz);
const foo = getBaz(getBar());

const foo = ((bar) => {
  return bar ? bar.baz : baz;
})(getBar());
```

## How to use

## References
