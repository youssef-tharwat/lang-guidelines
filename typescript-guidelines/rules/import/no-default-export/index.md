
### What it does

Forbids a module from having default exports. This helps your editor
provide better auto-import functionality, as named exports offer more
explicit and predictable imports compared to default exports.

### Why is this bad?

Default exports can lead to confusion, as the name of the imported value
can vary based on how it's imported. This can make refactoring and
auto-imports less reliable.

### Examples

Examples of **incorrect** code for this rule:

```javascript
export default 'bar';

const foo = 'foo';
export { foo as default }
```

Examples of **correct** code for this rule:

```javascript
export const foo = "foo";
export const bar = "bar";
```

## How to use

## References
