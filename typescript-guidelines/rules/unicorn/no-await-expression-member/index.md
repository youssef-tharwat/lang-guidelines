
### What it does

Disallows member access from `await` expressions.

### Why is this bad?

When accessing a member from an `await` expression,
the `await` expression has to be parenthesized, which is not readable.

### Examples

Examples of **incorrect** code for this rule:

```javascript
async function bad() {
  const secondElement = (await getArray())[1];
}
```

Examples of **correct** code for this rule:

```javascript
async function good() {
  const [, secondElement] = await getArray();
}
```

## How to use

## References
