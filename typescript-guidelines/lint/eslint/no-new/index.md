
### What it does

Disallow new operators outside of assignments or comparisons.

### Why is this bad?

Calling new without assigning or comparing it the reference is thrown away and in many
cases the constructor can be replaced with a function.

### Examples

Examples of **incorrect** code for this rule:

```javascript
new Person();

() => {
  new Date();
};
```

Examples of **correct** code for this rule:

```javascript
var a = new Date()(() => new Date());
```

## How to use

## References
