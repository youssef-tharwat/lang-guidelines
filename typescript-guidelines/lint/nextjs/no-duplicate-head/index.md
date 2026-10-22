
### What it does

Prevent duplicate usage of `<Head>` in `pages/_document.js`.

### Why is this bad?

This can cause unexpected behavior in your application.

### Examples

Examples of **incorrect** code for this rule:

```jsx
import Document, { Html, Head, Main, NextScript } from "next/document";
class MyDocument extends Document {
  static async getInitialProps(ctx) {}
  render() {
    return (
      <Html>
        <Head />
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
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
  static async getInitialProps(ctx) {}
  render() {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
export default MyDocument;
```

## How to use

## References
