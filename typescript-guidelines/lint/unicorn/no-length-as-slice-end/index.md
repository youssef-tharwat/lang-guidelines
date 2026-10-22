
### What it does

Disallow using `length` as the end argument of a `slice` call.

### Why is this bad?

Passing `length` as the end argument of a `slice` call is unnecessary and can be confusing.

### Examples

Examples of **incorrect** code for this rule:

```javascript
foo.slice(1, foo.length);
```

Examples of **correct** code for this rule:

```javascript
foo.slice(1);
```

## How to use

## References
