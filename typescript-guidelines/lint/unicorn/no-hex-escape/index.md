
### What it does

Enforces a convention of using [Unicode escapes](https://mathiasbynens.be/notes/javascript-escapes#unicode)
instead of [hexadecimal escapes](https://mathiasbynens.be/notes/javascript-escapes#hexadecimal) for
consistency and clarity.

### Why is this bad?

Using hexadecimal escapes can be less readable and harder to understand
when compared to Unicode escapes.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const foo = "\x1B";
const foo = `\x1B${bar}`;
```

Examples of **correct** code for this rule:

```javascript
const foo = "\u001B";
const foo = `\u001B${bar}`;
```

## How to use

## References
