
### What it does

Disallow unnecessary concatenation of literals or template literals.

### Why is this bad?

It’s unnecessary to concatenate two strings together when they could
be combined into a single literal.

### Examples

Examples of **incorrect** code for this rule:

```javascript
var foo = "a" + "b";
```

```javascript
var foo = "a" + "b" + "c";
```

Examples of **correct** code for this rule:

```javascript
var foo = "a" + bar;

// When the string concatenation is multiline
var foo = "a" + "b" + "c";
```

## How to use

## References
