
### What it does

This rule prevents the use of `dangerouslySetInnerHTML` prop.

### Why is this bad?

`dangerouslySetInnerHTML` is a way to inject HTML into your React
component. This is dangerous because it can easily lead to XSS
vulnerabilities.

### Examples

Examples of **incorrect** code for this rule:

```jsx
import React from "react";

const Hello = <div dangerouslySetInnerHTML={{ __html: "Hello World" }}></div>;
```

Examples of **correct** code for this rule:

```jsx
import React from "react";

const Hello = <div>Hello World</div>;
```

## How to use

## References
