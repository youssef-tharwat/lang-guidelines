
### What it does

Prevent the usage of `<img>` element due to slower
[LCP](https://nextjs.org/learn/seo/lcp) and higher bandwidth.

### Why is this bad?

`<img>` elements are not optimized for performance and can result in
slower LCP and higher bandwidth. Using [`<Image />`](https://nextjs.org/docs/pages/api-reference/components/image)
from `next/image` will automatically optimize images and serve them as
static assets.

### Examples

Examples of **incorrect** code for this rule:

```javascript
export function MyComponent() {
  return (
    <div>
      <img src="/test.png" alt="Test picture" />
    </div>
  );
}
```

Examples of **correct** code for this rule:

```javascript
import Image from "next/image";
import testImage from "./test.png";
export function MyComponent() {
  return (
    <div>
      <Image src={testImage} alt="Test picture" />
    </div>
  );
}
```

## How to use

## References
