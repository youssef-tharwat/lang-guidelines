
### What it does

Prevent usage of `next/script` in `next/head` component.

### Why is this bad?

The `next/script` component should not be used in a `next/head` component.
Instead move the `<Script />` component outside of `<Head>` instead.

### Examples

Examples of **incorrect** code for this rule:

```jsx
import Script from "next/script";
import Head from "next/head";

export default function Index() {
  return (
    <Head>
      <title>Next.js</title>
      <Script src="/my-script.js" />
    </Head>
  );
}
```

Examples of **correct** code for this rule:

```jsx
import Script from "next/script";
import Head from "next/head";

export default function Index() {
  return (
    <>
      <Head>
        <title>Next.js</title>
      </Head>
      <Script src="/my-script.js" />
    </>
  );
}
```

## How to use

## References
