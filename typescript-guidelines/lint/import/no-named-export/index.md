
### What it does

Prohibit named exports.

### Why is this bad?

Named exports require strict identifier matching and can lead to fragile imports,
while default exports enforce a single, consistent module entry point.

### Examples

Examples of **incorrect** code for this rule:

```js
export const foo = "foo";

const bar = "bar";
export { bar };
```

Examples of **correct** code for this rule:

```js
export default 'bar';

const foo = 'foo';
export { foo as default }
```

## How to use

## References
