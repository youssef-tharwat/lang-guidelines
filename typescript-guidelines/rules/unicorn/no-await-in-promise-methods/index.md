
### What it does

Disallow using `await` in `Promise` method parameters.

### Why is this bad?

Using `await` on promises passed as arguments to `Promise.all()`,
`Promise.allSettled()`, `Promise.any()`, or `Promise.race()` is likely a
mistake.

### Examples

Examples of **incorrect** code for this rule:

```javascript
async function foo() {
  Promise.all([await promise, anotherPromise]);
  Promise.allSettled([await promise, anotherPromise]);
  Promise.any([await promise, anotherPromise]);
  Promise.race([await promise, anotherPromise]);
}
```

Examples of **correct** code for this rule:

```javascript
async function foo() {
  Promise.all([promise, anotherPromise]);
  Promise.allSettled([promise, anotherPromise]);
  Promise.any([promise, anotherPromise]);
  Promise.race([promise, anotherPromise]);
}
```

## How to use

## References
