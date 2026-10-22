
### What it does

Removes the extra spaces or new line characters inside a pair of braces
that does not contain additional code. This ensures that braces are clean
and do not contain unnecessary spaces or newlines.

### Why is this bad?

Extra spaces inside braces can negatively impact the readability of the code.
Keeping braces clean and free of unnecessary characters improves consistency and
makes the code easier to understand and maintain.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const a = {  };
class A {
}
```

Examples of **correct** code for this rule:

```javascript
const a = {};
class A {}
```

## How to use

## References
