
### What it does

Prefer top-level await over top-level promises and async function calls.

### Why is this bad?

Top-level await is more readable and can prevent unhandled rejections.

### Examples

Examples of **incorrect** code for this rule:

```js
(async () => {
  await run();
})();

run().catch((error) => {
  console.error(error);
});
```

Examples of **correct** code for this rule:

```js
await run();

try {
  await run();
} catch (error) {
  console.error(error);
}
```

## How to use

## References
