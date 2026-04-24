
### What it does

Disallow equal signs explicitly at the beginning of regular expressions.

### Why is this bad?

Characters /= at the beginning of a regular expression literal can be confused with a
division assignment operator.

### Examples

Examples of **incorrect** code for this rule:

```javascript
function bar() {
  return /=foo/;
}
```

Examples of **correct** code for this rule:

```javascript
function bar() {
  return /[=]foo/;
}
```

## How to use

## References
