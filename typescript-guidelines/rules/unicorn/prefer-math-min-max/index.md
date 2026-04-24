
### What it does

Prefers use of `Math.min()` and `Math.max()` instead of ternary
expressions when performing simple comparisons.

### Why is this bad?

Using `Math.min()` and `Math.max()` for simple comparisons is more
concise, easier to understand, and less prone to errors than ternary
expressions. They clearly express the intent to find the minimum or
maximum value.

### Examples

Examples of **incorrect** code for this rule:

```javascript
height > 50 ? 50 : height;
height > 50 ? height : 50;
```

Examples of **correct** code for this rule:

```javascript
Math.min(height, 50);
Math.max(height, 50);
```

## How to use

## References
