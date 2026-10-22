
### What it does

Prefer `.find(...)` over `.filter(...)[0]` for retrieving a single element.

### Why is this bad?

`.filter(...)[0]` builds an intermediate array and is less clear about intent.
`.find(...)` directly expresses that only the first matching element is needed.

### Examples

Examples of **incorrect** code for this rule:

```ts
const first = list.filter((item) => item.active)[0];
```

Examples of **correct** code for this rule:

```ts
const first = list.find((item) => item.active);
```

## How to use

## References
