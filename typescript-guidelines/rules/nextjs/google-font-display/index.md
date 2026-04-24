
### What it does

Enforce font-display behavior with Google Fonts.

### Why is this bad?

Specifying display=optional minimizes the risk of invisible text or
layout shift. If swapping to the custom font after it has loaded is
important to you, then use \`display=swap\`\` instead.

### Examples

Examples of **incorrect** code for this rule:

```jsx
import Head from "next/head";

export default Test = () => {
  return (
    <Head>
      <link href="https://fonts.googleapis.com/css2?family=Krona+One" rel="stylesheet" />
    </Head>
  );
};
```

Examples of **correct** code for this rule:

```jsx
import Head from "next/head";

export default Test = () => {
  return (
    <Head>
      <link
        href="https://fonts.googleapis.com/css2?family=Krona+One&display=optional"
        rel="stylesheet"
      />
    </Head>
  );
};
```

## How to use

## References
