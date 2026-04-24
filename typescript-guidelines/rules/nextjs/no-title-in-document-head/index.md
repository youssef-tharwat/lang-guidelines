
### What it does

Prevent usage of `<title>` with `Head` component from `next/document`.

### Why is this bad?

A `<title>` element should only be used for any `<head>` code that is common for all pages.
Title tags should be defined at the page-level using `next/head` instead.

### Examples

Examples of **incorrect** code for this rule:

```javascript
import { Head } from "next/document";

export function Home() {
  return (
    <div>
      <Head>
        <title>My page title</title>
      </Head>
    </div>
  );
}
```

Examples of **correct** code for this rule:

```javascript
import Head from "next/head";

export function Home() {
  return (
    <div>
      <Head>
        <title>My page title</title>
      </Head>
    </div>
  );
}
```

## How to use

## References
