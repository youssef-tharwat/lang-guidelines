
### What it does

Detects common typos in Next.js data fetching function names.

### Why is this bad?

Next.js will not call incorrectly named data fetching functions, causing pages to render without expected data.

### Examples

Examples of **incorrect** code for this rule:

```javascript
export default function Page() {
  return <div></div>;
}
export async function getServurSideProps() {}
```

Examples of **correct** code for this rule:

```javascript
export default function Page() {
  return <div></div>;
}
export async function getServerSideProps() {}
```

## How to use

## References
