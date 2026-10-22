
### What it does

Disallow 2+ consecutive spaces in regular expressions.

### Why is this bad?

In a regular expression, it is hard to tell how many spaces are
intended to be matched. It is better to use only one space and
then specify how many spaces are expected using a quantifier.

```javascript
var re = /foo {3}bar/;
```

### Examples

Examples of **incorrect** code for this rule:

```javascript
var re = /foo   bar/;
```

## How to use

## References
