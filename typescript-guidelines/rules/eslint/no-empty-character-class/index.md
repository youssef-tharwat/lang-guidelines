
### What it does

Disallow empty character classes in regular expressions.

### Why is this bad?

Because empty character classes in regular expressions do not match anything, they might be typing mistakes.

### Examples

Examples of **incorrect** code for this rule:

```javascript
var foo = /^abc[]/;
```

Examples of **correct** code for this rule:

```javascript
var foo = /^abc/;
var foo2 = /^abc[123]/;
```

## How to use

## References
