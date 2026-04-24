
### What it does

Disallows the use of `async`/`await`.

This rule should generally not be used in modern JavaScript/TypeScript
codebases without good reason.

### Why is this bad?

This rule is useful for environments that don't support `async`/`await` syntax,
or when you want to enforce the use of promises or other asynchronous
patterns instead. It can also be used to maintain consistency in codebases
that use alternative async patterns.

### Examples

Examples of **incorrect** code for this rule:

```javascript
async function foo() {
  await bar();
  return baz();
}
```

## How to use

## References
