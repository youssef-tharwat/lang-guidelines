
### What it does

Prevents the usage of `next/head` inside a Next.js document.

### Why is this bad?

Importing `next/head` inside `pages/_document.js` can cause
unexpected issues in your Next.js application.

### Examples

Examples of **incorrect** code for this rule:

```jsx
import Document, { Html, Main, NextScript } from "next/document";
import Head from "next/head";

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    //...
  }

  render() {
    return (
      <Html>
        <Head></Head>
      </Html>
    );
  }
}

export default MyDocument;
```

Examples of **correct** code for this rule:

```jsx
import Document, { Html, Head, Main, NextScript } from "next/document";

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    //...
  }

  render() {
    return (
      <Html>
        <Head></Head>
      </Html>
    );
  }
}

export default MyDocument;
```

## How to use

## References
