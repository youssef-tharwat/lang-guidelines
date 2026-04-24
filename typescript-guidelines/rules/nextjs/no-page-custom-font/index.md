
### What it does

Prevent page-only custom fonts.

### Why is this bad?

* The custom font you're adding was added to a page - this only adds the font to the specific page and not the entire application.
* The custom font you're adding was added to a separate component within `pages/_document.js` - this disables automatic font optimization.

### Examples

Examples of **incorrect** code for this rule:

```jsx
// pages/index.jsx
import Head from "next/head";
function IndexPage() {
  return (
    <Head>
      <link
        href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap"
        rel="stylesheet"
      />
    </Head>
  );
}
export default IndexPage;
```

Examples of **correct** code for this rule:

```jsx
// pages/_document.jsx
import NextDocument, { Html, Head } from "next/document";
class Document extends NextDocument {
  render() {
    return (
      <Html>
        <Head>
          <link
            href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap"
            rel="stylesheet"
          />
        </Head>
      </Html>
    );
  }
}
export default Document;
```

## How to use

## References
